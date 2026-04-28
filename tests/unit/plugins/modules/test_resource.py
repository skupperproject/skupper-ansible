import io
import os
import shutil
import tempfile
import typing as t

import yaml
from unittest import TestCase
from unittest.mock import patch
from kubernetes import config
from kubernetes.dynamic.exceptions import ApiException
from ansible.module_utils import basic
from ansible_collections.skupper.v2.plugins.module_utils.k8s import K8sClient
from ansible_collections.skupper.v2.plugins.module_utils.resource import (
    version_kind
)
from ansible_collections.skupper.v2.tests.unit.utils.ansible_module_mock import (
    set_module_args,
    AnsibleExitJson,
    AnsibleFailJson,
    exit_json,
    fail_json,
    get_bin_path,
)

sample_site_def = """---
apiVersion: skupper.io/v2alpha1
kind: Site
metadata:
  name: my-site
spec:
  linkAccess: default
  settings:
    name: my-site
---
apiVersion: skupper.io/v2alpha1
kind: RouterAccess
metadata:
  name: access-my-site
spec:
  roles:
    - port: 55671
      name: inter-router
    - port: 45671
      name: edge
  bindHost: 0.0.0.0
  subjectAlternativeNames:
    - my.site.hostname
---
apiVersion: skupper.io/v2alpha1
kind: Listener
metadata:
  name: backend
spec:
  host: 0.0.0.0
  port: 8080
  routingKey: backend
---

"""

# Minimal AccessToken YAML (used with kubernetes default platform to assert normal apply)
sample_access_token_def = """---
apiVersion: skupper.io/v2alpha1
kind: AccessToken
metadata:
  name: my-token
spec: {}
"""

# AccessToken with url/code for system-site HTTP redeem (Skupper non-kube)
sample_access_token_system = """---
apiVersion: skupper.io/v2alpha1
kind: AccessToken
metadata:
  name: sys-tok
spec:
  url: https://claims.example.test/redeem
  code: my-secret-code
"""

sample_redeem_http_response = """apiVersion: v1
kind: Secret
metadata:
  name: link-secret-sys-tok
data:
  tls.crt: eQ==
---
apiVersion: skupper.io/v2alpha1
kind: Link
metadata:
  name: sys-tok
spec:
  tlsCredentials: link-secret-sys-tok
"""

# Same documents as sample_redeem_http_response but Link before Secret (order must not matter).
sample_redeem_http_response_link_first = """apiVersion: skupper.io/v2alpha1
kind: Link
metadata:
  name: sys-tok
spec:
  tlsCredentials: link-secret-sys-tok
---
apiVersion: v1
kind: Secret
metadata:
  name: link-secret-sys-tok
data:
  tls.crt: eQ==
"""


class K8sMock():
    def __init__(self, *args, **kwargs) -> None:
        self._kind = None
        pass

    def load_kube_config(self, *args, **kwargs):
        pass

    def client_resources_get(self, api_version: str, kind: str):
        self._kind = kind
        return self

    def create(self, **kwargs):
        pass

    def get(self, **kwargs):
        pass

    def patch(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass


class _DictLike:
    """Wrapper so mock get() return value has to_dict() as K8sClient.get() expects."""
    def __init__(self, d):
        self._d = d

    def to_dict(self):
        return self._d


class TestResourceModule(TestCase):

    def tearDown(self):
        for d in self.tempDirs:
            shutil.rmtree(d)

    def setUp(self):
        self.tempDirs = []
        self.store = {}
        self.k8s = K8sMock()
        self.module_warnings = []

        def _capture_warn(*args, **kwargs):
            msg = args[1] if len(args) > 1 else kwargs.get("message", "")
            self.module_warnings.append(msg)

        self.mock_module = patch.multiple(basic.AnsibleModule,
                                          exit_json=exit_json,
                                          fail_json=fail_json,
                                          get_bin_path=get_bin_path,
                                          warn=_capture_warn)
        self.mock_k8s_config = patch.multiple(
            config, load_kube_config=self.k8s.load_kube_config)
        self.mock_k8s_client = patch.multiple(K8sClient, __init__=self.k8s.__init__,
                                              api=self.k8s.client_resources_get, create=True)
        self.mock_fetch_url = patch(
            'ansible.module_utils.urls.fetch_url', new=self.fetch_url)
        self.mock_module.start()
        self.mock_k8s_config.start()
        self.mock_k8s_client.start()
        self.mock_fetch_url.start()
        self.addCleanup(self.mock_module.stop)
        self.addCleanup(self.mock_k8s_config.stop)
        self.addCleanup(self.mock_k8s_client.stop)
        self.addCleanup(self.mock_fetch_url.stop)

        self.k8s.create = self.k8s_create
        self.k8s.patch = self.k8s_patch
        self.k8s.delete = self.k8s_delete
        self.k8s.get = self.k8s_get

        # do not use real namespace path
        self.temphome = tempfile.mkdtemp()
        resources_home_mock = lambda ns: os.path.join(self.temphome, ns, "input", "resources")
        self.mock_resources_home = patch(
            'ansible_collections.skupper.v2.plugins.module_utils.common.resources_home', new=resources_home_mock)
        self.mock_resources_home.start()
        self.addCleanup(self.mock_resources_home.stop)

        # resource module must be imported at last, otherwise fetch_url won't be patched
        try:
            from ansible_collections.skupper.v2.plugins.module_utils.common import resources_home
            from ansible_collections.skupper.v2.plugins.modules import resource
            self.module = resource
            self.resources_home = resources_home
        except ImportError:
            pass

    def test_mutually_exclusive_args(self):
        inputs = [
            {"path": "file.yaml", "def": "resource definition"},
            {"def": "resource definition", "remote": True},
        ]
        for input in inputs:
            with self.assertRaises(AnsibleFailJson) as ex:
                with set_module_args(input):
                    self.module.main()

    def test_module_fail_when_required_args_missing(self):
        with self.assertRaises(AnsibleFailJson):
            with set_module_args({}):
                self.module.main()

    def test_module_fail_bad_args(self):
        with self.assertRaises(AnsibleFailJson):
            with set_module_args({"namespace": "invalid.name"}):
                self.module.main()

    def test_nonkube_path_local_directory(self):

        test_cases = [
            {
                "name": "create new entry using state present",
                "expectChanged": True,
                "storedObjects": 3,
                "state": "present",
            }, {
                "name": "create existing entry using state present",
                "expectChanged": False,
                "storedObjects": 3,
                "state": "present",
            }, {
                "name": "create existing entry using state latest",
                "state": "latest",
                "storedObjects": 3,
                "expectChanged": True,
            }, {
                "name": "deleting all entries using state absent",
                "state": "absent",
                "storedObjects": 0,
                "expectChanged": True,
            }, {
                "name": "no changes on empty store using state absent",
                "state": "absent",
                "storedObjects": 0,
                "expectChanged": False,
            }
        ]
        for subdir in [False, True]:
            path = tempfile.mkdtemp()
            self.tempDirs.append(path)
            path_param = path
            store_path = path
            if subdir:
                store_path = os.path.join(path, "subdir")
                os.mkdir(store_path)
            filename = os.path.join(store_path, "resources.yaml")
            with open(filename, "w", encoding='utf-8') as f:
                f.write(sample_site_def)
            for test_case in test_cases:
                with set_module_args({
                    'path': path_param,
                    'state': test_case.get("state", ""),
                    'platform': 'podman',
                }):
                    with self.assertRaises(AnsibleExitJson) as result:
                        self.module.main()
                    self.assertTrue(
                        result.exception.args[0]['changed'] == test_case.get(
                            "expectChanged", False),
                        "{} - {}".format(test_case.get("name"), result.exception)
                    )
                    storedObjects = 0
                    for file in ["Site-my-site", "RouterAccess-access-my-site", "Listener-backend"]:
                        filename = os.path.join(
                            self.temphome, "default/input/resources/{}.yaml".format(file))
                        if os.path.isfile(filename):
                            storedObjects += 1
                    self.assertEqual(test_case.get("storedObjects"), storedObjects,
                                    "{} - {}".format(test_case.get("name"), result.exception))

    def test_kube_path_local_file(self):

        test_cases = [
            {
                "name": "create new entry using state present",
                "expectChanged": True,
                "storedObjects": 3,
                "state": "present",
            }, {
                "name": "create existing entry using state present",
                "expectChanged": False,
                "storedObjects": 3,
                "state": "present",
            }, {
                "name": "create existing entry using state latest",
                "state": "latest",
                "storedObjects": 3,
                "expectChanged": True,
            }, {
                "name": "deleting all entries using state absent",
                "state": "absent",
                "storedObjects": 0,
                "expectChanged": True,
            }, {
                "name": "no changes on empty store using state absent",
                "state": "absent",
                "storedObjects": 0,
                "expectChanged": False,
            }
        ]
        fd, fn = tempfile.mkstemp(suffix=".yaml")
        with os.fdopen(fd, "w", encoding='utf-8') as f:
            f.write(sample_site_def)
        for test_case in test_cases:
            with set_module_args({
                'path': fn,
                'state': test_case.get("state", "")
            }):

                with self.assertRaises(AnsibleExitJson) as result:
                    self.module.main()
                self.assertTrue(
                    result.exception.args[0]['changed'] == test_case.get(
                        "expectChanged", False),
                    "{} - {}".format(test_case.get("name"), result.exception)
                )
                self.assertEqual(test_case.get("storedObjects"), len(
                    self.store), "incorrect amount of objects stored")

    def test_kube_path_http_file(self):

        test_cases = [
            {
                "name": "create new entry using state present",
                "expectChanged": True,
                "storedObjects": 3,
                "state": "present",
                "path": "https://my.fake.domain/data.yaml"
            }, {
                "name": "create existing entry using state present",
                "expectChanged": False,
                "storedObjects": 3,
                "state": "present",
                "path": "https://my.fake.domain/data.yaml"
            }, {
                "name": "create existing entry using state latest",
                "state": "latest",
                "storedObjects": 3,
                "expectChanged": True,
                "path": "https://my.fake.domain/data.yaml"
            }, {
                "name": "deleting all entries using state absent",
                "state": "absent",
                "storedObjects": 0,
                "expectChanged": True,
                "path": "https://my.fake.domain/data.yaml"
            }, {
                "name": "no changes on empty store using state absent",
                "state": "absent",
                "storedObjects": 0,
                "expectChanged": False,
                "path": "https://my.fake.domain/data.yaml"
            }, {
                "name": "invalid url",
                "state": "present",
                "storedObjects": 0,
                "expectChanged": False,
                "expectFail": True,
                "path": "https://my.fake.domain/data.yaml.bad"
            }
        ]
        for test_case in test_cases:
            with set_module_args({
                'path': test_case.get("path", ""),
                'state': test_case.get("state", "")
            }):
                expectFailed = test_case.get("expectFail", False)
                if not expectFailed:
                    with self.assertRaises(AnsibleExitJson) as result:
                        self.module.main()
                else:
                    with self.assertRaises(AnsibleFailJson) as result:
                        self.module.main()
                changed = 'changed' in result.exception.args[0] and result.exception.args[0]['changed']
                self.assertTrue(changed == test_case.get("expectChanged", False),
                                "{} - {}".format(test_case.get("name"),
                                                result.exception)
                                )
                failed = 'failed' in result.exception.args[0] and result.exception.args[0]['failed']
                self.assertTrue(failed == expectFailed,
                                "{} - {}".format(test_case.get("name"), result.exception))
                self.assertEqual(test_case.get("storedObjects"), len(
                    self.store), "incorrect amount of objects stored")

    def test_kube_def(self):

        test_cases = [
            {
                "name": "create new entry using state present",
                "expectChanged": True,
                "storedObjects": 3,
                "state": "present",
            }, {
                "name": "create existing entry using state present",
                "expectChanged": False,
                "storedObjects": 3,
                "state": "present",
            }, {
                "name": "create existing entry using state latest",
                "state": "latest",
                "storedObjects": 3,
                "expectChanged": True,
            }, {
                "name": "deleting all entries using state absent",
                "state": "absent",
                "storedObjects": 0,
                "expectChanged": True,
            }, {
                "name": "no changes on empty store using state absent",
                "state": "absent",
                "storedObjects": 0,
                "expectChanged": False,
            }
        ]
        for test_case in test_cases:
            with set_module_args({
                'def': sample_site_def,
                'state': test_case.get("state", "")
            }):

                with self.assertRaises(AnsibleExitJson) as result:
                    self.module.main()
                self.assertTrue(
                    result.exception.args[0]['changed'] == test_case.get(
                        "expectChanged", False),
                    "{} - {}".format(test_case.get("name"), result.exception)
                )
                self.assertEqual(test_case.get("storedObjects"), len(
                    self.store), "incorrect amount of objects stored")

    def test_redeem_kubernetes_warns_and_applies_access_token(self):
        """redeem=true on kubernetes is ignored; controller owns tokens; warn and apply CR as usual."""
        with set_module_args({
            "def": sample_access_token_def,
            "namespace": "test",
            "redeem": True,
        }):
            with self.assertRaises(AnsibleExitJson) as result:
                self.module.main()
        out = result.exception.args[0]
        self.assertNotIn("redeemed_links", out)
        self.assertIn("AccessToken-my-token", self.store)
        self.assertEqual(len(self.module_warnings), 1)
        self.assertIn("kubernetes", self.module_warnings[0].lower())

    def test_redeem_system_site_http_returns_link_and_secret(self):
        """podman/docker/linux: POST spec.url with spec.code; apply Secret+Link; drop AccessToken."""
        calls = []

        def fake_open_url(url, **kwargs):
            calls.append(
                {
                    "url": url,
                    "method": kwargs.get("method"),
                    "data": kwargs.get("data"),
                    "headers": kwargs.get("headers"),
                }
            )

            class _Resp:
                def read(self):
                    return sample_redeem_http_response.encode("utf-8")

            return _Resp()

        with patch(
            "ansible_collections.skupper.v2.plugins.modules.resource.open_url",
            side_effect=fake_open_url,
        ):
            with set_module_args({
                "def": sample_access_token_system,
                "namespace": "east",
                "platform": "podman",
                "redeem": True,
            }):
                with self.assertRaises(AnsibleExitJson) as result:
                    self.module.main()
        out = result.exception.args[0]
        self.assertIn("redeemed_links", out)
        self.assertTrue(out.get("changed"), "redeem writes Link/Secret and removes token")
        redeemed = out["redeemed_links"]
        self.assertEqual(len(redeemed), 1)
        self.assertIn("kind: Secret", redeemed[0])
        self.assertIn("kind: Link", redeemed[0])
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0]["url"], "https://claims.example.test/redeem")
        self.assertEqual(calls[0]["method"], "POST")
        self.assertEqual(calls[0]["data"], b"my-secret-code")
        self.assertEqual(calls[0]["headers"].get("name"), "sys-tok")
        self.assertEqual(calls[0]["headers"].get("subject"), "east")
        # AccessToken file removed from namespace resources
        at_path = os.path.join(
            self.temphome, "east", "input", "resources", "AccessToken-sys-tok.yaml"
        )
        self.assertFalse(
            os.path.isfile(at_path),
            "AccessToken yaml should never be written when redeem is true",
        )

    def test_redeem_http_accepts_link_before_secret_in_response(self):
        """Redeem HTTP body may list Link before Secret; bundle is normalized to Secret(s) then Link(s)."""

        def fake_open_url(url, **kwargs):
            class _Resp:
                def read(self):
                    return sample_redeem_http_response_link_first.encode("utf-8")

            return _Resp()

        with patch(
            "ansible_collections.skupper.v2.plugins.modules.resource.open_url",
            side_effect=fake_open_url,
        ):
            with set_module_args({
                "def": sample_access_token_system,
                "namespace": "east",
                "platform": "podman",
                "redeem": True,
            }):
                with self.assertRaises(AnsibleExitJson) as result:
                    self.module.main()
        redeemed = result.exception.args[0]["redeemed_links"][0]
        kinds = [
            d.get("kind")
            for d in yaml.safe_load_all(redeemed)
            if isinstance(d, dict) and d.get("kind")
        ]
        self.assertEqual(kinds, ["Secret", "Link"])

    def test_redeem_skips_when_link_exists_and_state_present(self):
        """Do not HTTP-redeem if Link-{name}.yaml already exists and state is present."""
        link_path = os.path.join(
            self.temphome, "east", "input", "resources", "Link-sys-tok.yaml"
        )
        os.makedirs(os.path.dirname(link_path), exist_ok=True)
        with open(link_path, "w", encoding="utf-8") as f:
            f.write("kind: Link\nmetadata:\n  name: sys-tok\n")

        calls = []

        def fake_open_url(url, **kwargs):
            calls.append(url)
            class _Resp:
                def read(self):
                    return sample_redeem_http_response.encode("utf-8")
            return _Resp()

        with patch(
            "ansible_collections.skupper.v2.plugins.modules.resource.open_url",
            side_effect=fake_open_url,
        ):
            with set_module_args({
                "def": sample_access_token_system,
                "namespace": "east",
                "platform": "podman",
                "redeem": True,
                "state": "present",
            }):
                with self.assertRaises(AnsibleExitJson) as result:
                    self.module.main()
        out = result.exception.args[0]
        self.assertEqual(len(calls), 0)
        self.assertNotIn("redeemed_links", out)
        self.assertFalse(out.get("changed", False))
        skip_warns = [w for w in self.module_warnings if "Skipping redeem" in w]
        self.assertEqual(len(skip_warns), 1)
        self.assertIn("sys-tok", skip_warns[0])

    def test_redeem_runs_when_link_exists_and_state_latest(self):
        """state=latest sets overwrite; redeem runs even if Link-{name}.yaml exists."""
        link_path = os.path.join(
            self.temphome, "east", "input", "resources", "Link-sys-tok.yaml"
        )
        os.makedirs(os.path.dirname(link_path), exist_ok=True)
        with open(link_path, "w", encoding="utf-8") as f:
            f.write("kind: Link\nmetadata:\n  name: sys-tok\n")

        calls = []

        def fake_open_url(url, **kwargs):
            calls.append(url)
            class _Resp:
                def read(self):
                    return sample_redeem_http_response.encode("utf-8")
            return _Resp()

        with patch(
            "ansible_collections.skupper.v2.plugins.modules.resource.open_url",
            side_effect=fake_open_url,
        ):
            with set_module_args({
                "def": sample_access_token_system,
                "namespace": "east",
                "platform": "podman",
                "redeem": True,
                "state": "latest",
            }):
                with self.assertRaises(AnsibleExitJson) as result:
                    self.module.main()
        out = result.exception.args[0]
        self.assertEqual(len(calls), 1)
        self.assertIn("redeemed_links", out)

    def test_redeem_http_failure_warns_without_failing_module(self):
        """Redeem HTTP errors warn and set redeem_failures; module exits successfully (idempotent re-runs)."""

        def fake_open_url(url, **kwargs):
            raise OSError("claims endpoint unreachable")

        with patch(
            "ansible_collections.skupper.v2.plugins.modules.resource.open_url",
            side_effect=fake_open_url,
        ):
            with set_module_args({
                "def": sample_access_token_system,
                "namespace": "east",
                "platform": "podman",
                "redeem": True,
            }):
                with self.assertRaises(AnsibleExitJson) as result:
                    self.module.main()
        out = result.exception.args[0]
        self.assertFalse(out.get("failed", False))
        self.assertIn("redeem_failures", out)
        self.assertEqual(len(out["redeem_failures"]), 1)
        self.assertEqual(out["redeem_failures"][0]["name"], "sys-tok")
        self.assertIn("unreachable", out["redeem_failures"][0]["msg"])
        self.assertNotIn("redeemed_links", out)
        self.assertEqual(len(self.module_warnings), 1)
        self.assertIn("sys-tok", self.module_warnings[0])

    def test_redeem_kubernetes_warns_no_http_redeem(self):
        """Kubernetes ignores redeem; open_url not used; AccessToken CR applied to cluster."""
        calls = []

        def fake_open_url(url, **kwargs):
            calls.append(url)
            class _Resp:
                def read(self):
                    return sample_redeem_http_response.encode("utf-8")
            return _Resp()

        with patch(
            "ansible_collections.skupper.v2.plugins.modules.resource.open_url",
            side_effect=fake_open_url,
        ):
            with set_module_args({
                "def": sample_access_token_system,
                "namespace": "east",
                "platform": "kubernetes",
                "redeem": True,
            }):
                with self.assertRaises(AnsibleExitJson) as result:
                    self.module.main()
        out = result.exception.args[0]
        self.assertNotIn("redeemed_links", out)
        self.assertIn("AccessToken-sys-tok", self.store)
        self.assertEqual(len(calls), 0)
        self.assertEqual(len(self.module_warnings), 1)
        self.assertIn("kubernetes", self.module_warnings[0].lower())

    def k8s_create(self, **kwargs):
        if "body" not in kwargs:
            return
        obj = kwargs.get("body", {})
        version, kind = version_kind(obj)
        name = obj.get("metadata", {}).get("name")
        if not name:
            self.fail("bad name")
        key = "{}-{}".format(kind, name)
        overwrite = True if "overwrite" in kwargs and kwargs.get(
            "overwrite", False) else False
        if key in self.store:
            if not overwrite:
                raise ApiException(reason="Conflict")
        self.store[key] = obj

    def k8s_patch(self, **kwargs):
        self.k8s_create(body=kwargs.get("body"), overwrite=True)

    def k8s_delete(self, **kwargs):
        if "name" not in kwargs:
            return
        name = kwargs.get("name", "")
        kind = self.k8s._kind
        if not name:
            self.fail("bad name")
        key = "{}-{}".format(kind, name)
        if key in self.store:
            del self.store[key]
        else:
            raise ApiException(status=404)

    def k8s_get(self, **kwargs):
        """Mock get() for redeem flow: return AccessToken with Redeemed, Link, or Secret.
        K8sClient.get() calls res.to_dict(), so return a wrapper that has to_dict()."""
        name = kwargs.get("name", "")
        kind = self.k8s._kind
        if kind == "AccessToken":
            d = {"status": {"conditions": [{"type": "Redeemed", "status": "True"}]}}
        elif kind == "Link":
            d = {
                "metadata": {"name": name},
                "spec": {"tlsCredentials": "link-secret-" + name},
                "apiVersion": "skupper.io/v2alpha1",
                "kind": "Link",
            }
        elif kind == "Secret":
            d = {
                "metadata": {"name": name},
                "data": {"tls.crt": "YQ=="},
                "kind": "Secret",
                "apiVersion": "v1",
            }
        else:
            d = {}
        return _DictLike(d)

    def fetch_url(self, *args, **kwargs) -> t.Tuple[io.IOBase, dict]:
        url = kwargs.get("url", "")
        if not url or not str(url).endswith(".yaml"):
            return None, {"status": 404, "msg": "resource not found"}
        fd, fn = tempfile.mkstemp(suffix=".yaml")
        with os.fdopen(fd, "w", encoding='utf-8') as f:
            f.write(sample_site_def)
        return open(fn, "r", encoding='utf-8'), {"status": 200}
