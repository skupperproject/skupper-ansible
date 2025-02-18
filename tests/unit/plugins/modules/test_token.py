import datetime
import os
import tempfile
import yaml
from unittest import TestCase
from unittest.mock import patch
from ansible.module_utils import basic
from ansible_collections.skupper.v2.plugins.module_utils.k8s import K8sClient
from ansible_collections.skupper.v2.plugins.module_utils.exceptions import K8sException
from ansible_collections.skupper.v2.tests.unit.utils.ansible_module_mock import (
    set_module_args,
    AnsibleExitJson,
    AnsibleFailJson,
    exit_json,
    fail_json,
    get_bin_path,
)


class K8sClientMock:
    # all resources
    resources = []
    # resources that will throw a 500 error when trying to get them
    get_exception = []
    # resources that will throw a 500 error when trying to create them
    create_exception = []
    # resources created indirectly that are not put in ready state
    new_resources_not_ready = []
    # hook functions called after create_or_patch adds or replaces a resource
    new_resources_hook_fns = []

    def __init__(self, *args):
        pass

    @classmethod
    def clean(cls):
        cls.resources = []
        cls.get_exception = []
        cls.create_exception = []
        cls.new_resources_not_ready = []

    @classmethod
    def get(cls, namespace, group_version, kind, name, ignore_not_found=False):
        for ex_res in cls.get_exception:
            if namespace and ex_res.get['metadata']['namespace'] != namespace:
                continue
            if ex_res['apiVersion'] == group_version and \
                    ex_res['kind'] == kind:
                if not name or name == ex_res['metadata']['name']:
                    raise K8sException(status=500, msg="forced exception")
        response = []
        for res in cls.resources:
            if res['apiVersion'] != group_version:
                continue
            if res['kind'] != kind:
                continue
            if namespace and res['metadata']['namespace'] != namespace:
                continue
            if name and res['metadata']['name'] == name:
                return res
            if not name:
                response.append(res)
        if not ignore_not_found and name and not response:
            raise K8sException(status=404)
        return response

    @classmethod
    def delete(cls, namespace, definitions: str) -> bool:
        for definition in yaml.safe_load_all(definitions):
            group_version = definition['apiVersion']
            kind = definition['kind']
            name = definition['metadata']['name']
            for i in range(len(cls.resources)):
                res = cls.resources[i]
                if res['apiVersion'] != group_version:
                    continue
                if res['kind'] != kind:
                    continue
                if namespace and res['metadata']['namespace'] != namespace:
                    continue
                if res['metadata']['name'] == name:
                    cls.resources.pop(i)
                    return True
        return True

    @classmethod
    def create_or_patch(cls, namespace, definitions, overwrite) -> bool:
        for definition in yaml.safe_load_all(definitions):
            group_version = definition['apiVersion']
            kind = definition['kind']
            name = definition['metadata']['name']
            for ex_res in cls.create_exception:
                if namespace and ex_res.get['metadata']['namespace'] != namespace:
                    continue
                if ex_res['apiVersion'] == group_version and \
                        ex_res['kind'] == kind:
                    if (name or None) == ex_res['metadata']['name']:
                        raise K8sException(status=500, msg="forced exception")
            resources = cls.get(namespace, group_version,
                                kind, name, ignore_not_found=True)
            ready = True
            for not_ready_res in cls.new_resources_not_ready:
                if namespace and not_ready_res.get['metadata']['namespace'] != namespace:
                    continue
                if not_ready_res['apiVersion'] == group_version and \
                        not_ready_res['kind'] == kind:
                    if name == not_ready_res['metadata']['name']:
                        ready = False
                        break
            if ready:
                add_ready_condition(definition)
            if not resources:
                cls.resources.append(definition)
                for create_hook in cls.new_resources_hook_fns:
                    create_hook(definition)
                return True
            if len(resources) > 0 and overwrite:
                cls.delete(namespace, yaml.safe_dump(definition))
                cls.resources.append(definition)
                for create_hook in cls.new_resources_hook_fns:
                    create_hook(definition)
                return True
            raise Exception(resources)
        return False


class TestTokenModule(TestCase):

    def setUp(self):
        K8sClientMock.clean()
        self.mock_module = patch.multiple(basic.AnsibleModule,
                                          exit_json=exit_json,
                                          fail_json=fail_json,
                                          get_bin_path=get_bin_path)
        self.mock_module.start()
        self.addCleanup(self.mock_module.stop)

        # do not use real namespace path
        self.temphome = tempfile.mkdtemp()

        def namespace_home_mock(ns):
            return os.path.join(self.temphome, ns or "default")
        self.mock_namespace_home = patch(
            'ansible_collections.skupper.v2.plugins.module_utils.common.namespace_home', new=namespace_home_mock)
        self.mock_namespace_home.start()
        self.addCleanup(self.mock_namespace_home.stop)

        self.mock_k8s_client = patch.multiple(K8sClient,
                                              __init__=K8sClientMock.__init__,
                                              get=K8sClientMock.get,
                                              create_or_patch=K8sClientMock.create_or_patch,
                                              delete=K8sClientMock.delete)
        self.mock_k8s_client.start()
        self.addCleanup(self.mock_k8s_client.stop)

        # token module must be imported at last
        try:
            from ansible_collections.skupper.v2.plugins.module_utils.common import resources_home
            from ansible_collections.skupper.v2.plugins.modules import token
            self.module = token
            self.module.TokenModule.retry_delay = 0
            self.resources_home = resources_home
        except ImportError:
            pass

    def test_module_accepts_no_args(self):
        with self.assertRaises(AnsibleExitJson):
            set_module_args({'_ansible_check_mode': True})
            self.module.main()

    def test_module_fail_bad_args(self):
        args_list = [
            {"namespace": "invalid.name"},
            {"name": "invalid.name"},
            {"host": "/invalid/host"},
        ]
        for args in args_list:
            with self.assertRaises(AnsibleFailJson):
                set_module_args(args)
                self.module.main()

    def test_nonkube_load_links_none(self):
        with self.assertRaises(AnsibleExitJson):
            set_module_args({'platform': 'podman'})
            self.module.main()

    def test_nonkube_load_links(self):
        self._create_static_links()
        test_cases = [
            {
                "name": "first-available",
                "expected_token": "0.0.0.0",
            },
            {
                "name": "first-available-west-ns",
                "namespace": "west",
                "expected_token": "0.0.0.0",
            },
            {
                "name": "first-for-ra-name-1",
                "router_access": "ra-name-1",
                "expected_token": "0.0.0.0",
            },
            {
                "name": "specific-host-for-ra-name-1",
                "router_access": "ra-name-1",
                "host": "my.router.access",
                "expected_token": "my.router.access",
            },
            {
                "name": "first-for-ra-name-2",
                "router_access": "ra-name-2",
                "expected_token": "10.0.0.1",
            },
        ]
        for tc in test_cases:
            with self.assertRaises(AnsibleExitJson) as exit:
                set_module_args({
                    'platform': 'podman',
                    'namespace': tc.get('namespace'),
                    'name': tc.get('router_access'),
                    'host': tc.get('host'),
                })
                self.module.main()
            self.assertFalse(exit.exception.changed)
            self.assertEqual(exit.exception.token, tc.get("expected_token"))

    def _create_static_links(self):
        namespaces = ["default", "west"]
        router_access_names_hosts = {
            "ra-name-1": ["0.0.0.0", "127.0.0.1", "my.router.access"],
            "ra-name-2": ["10.0.0.1"],
        }
        for ns in namespaces:
            base_path = os.path.join(self.temphome, ns, "runtime", "links")
            os.makedirs(base_path)
            for ra_name in router_access_names_hosts:
                hosts = router_access_names_hosts[ra_name]
                for host in hosts:
                    with open(os.path.join(base_path, "link-{}-{}.yaml".format(ra_name, host)), "w") as f:
                        f.write(host)

    def test_kube_no_site_found(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            self.module.main()

    def test_kube_site_not_ready(self):
        K8sClientMock.resources.append(fake_site('default', 'my-site', False))
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            self.module.main()

    def test_kube_site_get_exception(self):
        my_site = fake_site('default', 'my-site', True)
        K8sClientMock.resources.append(my_site)
        my_site['metadata']['name'] = ''
        K8sClientMock.get_exception.append(my_site)
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            self.module.main()

    def test_kube_site_ready_grant_generated(self):
        K8sClientMock.resources.append(fake_site('default', 'my-site', True))
        self.assertEqual(1, len(K8sClientMock.resources))
        def create_hook(definition: dict):
            if definition['kind'] == 'AccessGrant':
                now = datetime.datetime.now(datetime.timezone.utc)
                expiration = now + datetime.timedelta(minutes=15)
                definition['status']['expirationTime'] = expiration.isoformat()
        K8sClientMock.new_resources_hook_fns.append(create_hook)
        with self.assertRaises(AnsibleExitJson) as exit:
            set_module_args({})
            self.module.main()
        self.assertTrue(exit.exception.changed)
        self.assertEqual(2, len(K8sClientMock.resources))
        self.assertTrue(
            str(K8sClientMock.resources[1]['metadata']['name']).startswith('ansible-grant-'))

    def test_kube_site_ready_grant_expired_generated(self):
        K8sClientMock.resources.append(fake_site('default', 'my-site', True))
        grant = fake_grant(ns='default', name='my-grant')
        now = datetime.datetime.now(datetime.timezone.utc)
        expiration = now - datetime.timedelta(seconds=1)
        grant['status']['expirationTime'] = expiration.isoformat()
        K8sClientMock.resources.append(grant)
        self.assertEqual(2, len(K8sClientMock.resources))
        def create_hook(definition: dict):
            if definition['kind'] == 'AccessGrant':
                now = datetime.datetime.now(datetime.timezone.utc)
                expiration = now + datetime.timedelta(minutes=15)
                definition['status']['expirationTime'] = expiration.isoformat()
        K8sClientMock.new_resources_hook_fns.append(create_hook)
        with self.assertRaises(AnsibleExitJson) as exit:
            set_module_args({})
            self.module.main()
        self.assertTrue(exit.exception.changed)
        self.assertEqual(3, len(K8sClientMock.resources))
        self.assertTrue(
            str(K8sClientMock.resources[2]['metadata']['name']).startswith('ansible-grant-'))

    def test_kube_site_ready_new_named_grant(self):
        K8sClientMock.resources.append(fake_site('default', 'my-site', True))
        self.assertEqual(1, len(K8sClientMock.resources))
        with self.assertRaises(AnsibleExitJson) as exit:
            set_module_args({'name': 'new-grant'})
            self.module.main()
        self.assertTrue(exit.exception.changed)
        self.assertEqual(2, len(K8sClientMock.resources))
        self.assertEqual(
            K8sClientMock.resources[1]['metadata']['name'], 'new-grant')

    def test_kube_site_ready_new_named_grant_exception(self):
        K8sClientMock.resources.append(fake_site('default', 'my-site', True))
        K8sClientMock.create_exception.append(fake_grant('default', 'my-grant'))
        self.assertEqual(1, len(K8sClientMock.resources))
        with self.assertRaises(AnsibleFailJson) as fail:
            set_module_args({'name': 'my-grant'})
            self.module.main()
        self.assertEqual(1, len(K8sClientMock.resources))

    def test_kube_site_ready_new_named_grant_not_ready(self):
        K8sClientMock.resources.append(fake_site('default', 'my-site', True))
        K8sClientMock.new_resources_not_ready.append(fake_grant('default', 'my-grant'))
        self.assertEqual(1, len(K8sClientMock.resources))
        with self.assertRaises(AnsibleFailJson) as fail:
            set_module_args({'name': 'my-grant'})
            self.module.main()
        self.assertEqual(2, len(K8sClientMock.resources))

    def test_kube_site_ready_grant_not_ready(self):
        K8sClientMock.resources.append(fake_site('default', 'my-site', True))
        my_grant = fake_grant('default', 'my-grant', ready=False)
        K8sClientMock.resources.append(my_grant)
        K8sClientMock.new_resources_not_ready.append(my_grant)
        self.assertEqual(2, len(K8sClientMock.resources))
        with self.assertRaises(AnsibleFailJson):
            set_module_args({'name': 'my-grant'})
            self.module.main()
        self.assertEqual(2, len(K8sClientMock.resources))

    def test_kube_site_ready_grants_ready(self):
        K8sClientMock.resources.append(fake_site('default', 'my-site', True))
        K8sClientMock.resources.append(fake_grant('default', 'my-grant-1'))
        K8sClientMock.resources.append(fake_grant('default', 'my-grant-2'))
        self.assertEqual(3, len(K8sClientMock.resources))
        with self.assertRaises(AnsibleExitJson):
            set_module_args({})
            self.module.main()
        self.assertEqual(3, len(K8sClientMock.resources))

    def test_kube_site_ready_grants_not_ready(self):
        K8sClientMock.resources.append(fake_site('default', 'my-site', True))
        my_grant_1 = fake_grant('default', 'my-grant-1', ready=False)
        my_grant_2 = fake_grant('default', 'my-grant-2', ready=False)
        K8sClientMock.resources.append(my_grant_1)
        K8sClientMock.resources.append(my_grant_2)
        K8sClientMock.new_resources_not_ready.append(my_grant_1)
        K8sClientMock.new_resources_not_ready.append(my_grant_2)
        self.assertEqual(3, len(K8sClientMock.resources))
        with self.assertRaises(AnsibleExitJson):
            set_module_args({})
            self.module.main()
        self.assertEqual(4, len(K8sClientMock.resources))

    def test_kube_site_ready_grant_get_exception(self):
        K8sClientMock.resources.append(fake_site('default', 'my-site', True))
        my_grant = fake_grant('default', 'my-grant', True)
        K8sClientMock.resources.append(my_grant)
        K8sClientMock.get_exception.append(my_grant)
        self.assertEqual(2, len(K8sClientMock.resources))
        with self.assertRaises(AnsibleFailJson):
            set_module_args({'name': 'my-grant'})
            self.module.main()
        self.assertEqual(2, len(K8sClientMock.resources))

    def test_kube_site_ready_generated_grant_get_exception(self):
        K8sClientMock.resources.append(fake_site('default', 'my-site', True))
        my_grant = fake_grant('default', 'my-grant')
        def create_hook(definition: dict):
            if definition['kind'] == 'AccessGrant':
                K8sClientMock.get_exception.append(my_grant)
        K8sClientMock.new_resources_hook_fns.append(create_hook)
        self.assertEqual(1, len(K8sClientMock.resources))
        with self.assertRaises(AnsibleFailJson) as fail:
            set_module_args({'name': 'my-grant'})
            self.module.main()
        self.assertEqual(2, len(K8sClientMock.resources), K8sClientMock.resources)

    def test_kube_site_ready_grant_cannot_be_redeemed(self):
        K8sClientMock.resources.append(fake_site('default', 'my-site', True))
        my_grant = fake_grant('default', 'my-grant', ready=True)
        my_grant['status']['redemptions'] = 1
        K8sClientMock.resources.append(my_grant)
        self.assertEqual(2, len(K8sClientMock.resources))
        with patch.object(basic.AnsibleModule, "warn") as mock_warn:
            with self.assertRaises(AnsibleExitJson) as exit:
                set_module_args({'name': 'my-grant'})
                self.module.main()
        mock_warn.assert_called_once_with("accessgrant 'my-grant' cannot be redeemed")
        self.assertEqual(2, len(K8sClientMock.resources))

    def test_kube_site_ready_grant_ready(self):
        K8sClientMock.resources.append(fake_site('default', 'my-site', True))
        K8sClientMock.resources.append(fake_grant('default', 'my-grant'))
        self.assertEqual(2, len(K8sClientMock.resources))
        with self.assertRaises(AnsibleExitJson) as exit:
            set_module_args({'name': 'my-grant'})
            self.module.main()
        self.assertFalse(exit.exception.changed)
        self.assertEqual(2, len(K8sClientMock.resources))

    def test_kube_site_existing_links_site_not_ready(self):
        K8sClientMock.resources.append(fake_site('default', 'my-site', False))
        self.assertEqual(1, len(K8sClientMock.resources))
        with self.assertRaises(AnsibleFailJson):
            set_module_args({'type': 'link'})
            self.module.main()
        self.assertEqual(1, len(K8sClientMock.resources))

    def test_kube_site_existing_links_cert_get_exception(self):
        site = fake_site('default', 'my-site', True)
        default_issuer = site['status']['defaultIssuer']
        K8sClientMock.resources.append(site)
        K8sClientMock.get_exception.append(fake_cert('default', 'link-1', default_issuer, True))
        self.assertEqual(1, len(K8sClientMock.resources))
        with self.assertRaises(AnsibleFailJson):
            set_module_args({'type': 'link'})
            self.module.main()
        self.assertEqual(1, len(K8sClientMock.resources))

    def test_kube_existing_links_ready(self):
        site = fake_site('default', 'my-site', True)
        K8sClientMock.resources.append(site)
        K8sClientMock.resources.append(fake_cert('default', 'link-1', site['status']['defaultIssuer'], True))
        K8sClientMock.resources.append(fake_secret('default', 'link-1'))
        self.assertEqual(3, len(K8sClientMock.resources))
        with self.assertRaises(AnsibleExitJson) as exit:
            set_module_args({'type': 'link'})
            self.module.main()
        self.assertEqual(3, len(K8sClientMock.resources))
        self.assertFalse(exit.exception.changed)
        self.assertTrue(exit.exception.token)
        self.assertEqual(2, len(list(yaml.safe_load_all(exit.exception.token))))

    def test_kube_existing_links_not_ready(self):
        site = fake_site('default', 'my-site', True)
        K8sClientMock.resources.append(site)
        K8sClientMock.resources.append(fake_cert('default', 'link-1', site['status']['defaultIssuer'], True, ready=False))
        K8sClientMock.resources.append(fake_secret('default', 'link-1'))
        K8sClientMock.new_resources_hook_fns.append(create_secret_hook)
        self.assertEqual(3, len(K8sClientMock.resources))
        with self.assertRaises(AnsibleExitJson) as exit:
            set_module_args({'type': 'link'})
            self.module.main()
        self.assertEqual(5, len(K8sClientMock.resources))
        self.assertTrue(exit.exception.changed)
        self.assertTrue(exit.exception.token)
        self.assertEqual(2, len(list(yaml.safe_load_all(exit.exception.token))))

    def test_kube_generate_link(self):
        site = fake_site('default', 'my-site', True)
        K8sClientMock.resources.append(site)
        K8sClientMock.new_resources_hook_fns.append(create_secret_hook)
        self.assertEqual(1, len(K8sClientMock.resources))
        with self.assertRaises(AnsibleExitJson) as exit:
            set_module_args({'type': 'link'})
            self.module.main()
        self.assertEqual(3, len(K8sClientMock.resources))
        self.assertTrue(exit.exception.changed)
        self.assertTrue(exit.exception.token)
        self.assertEqual(2, len(list(yaml.safe_load_all(exit.exception.token))))

    def test_kube_generate_named_link_create_exception(self):
        site = fake_site('default', 'my-site', True)
        K8sClientMock.resources.append(site)
        K8sClientMock.create_exception.append(fake_cert('default', 'my-link', site['status']['defaultIssuer'], True))
        self.assertEqual(1, len(K8sClientMock.resources))
        with self.assertRaises(AnsibleFailJson) as fail:
            set_module_args({'name': 'my-link', 'type': 'link'})
            self.module.main()
        self.assertEqual(1, len(K8sClientMock.resources))
        self.assertTrue(fail.exception.failed)
        self.assertTrue(fail.exception.msg)

    def test_kube_generate_named_link_create_not_ready(self):
        site = fake_site('default', 'my-site', True)
        K8sClientMock.resources.append(site)
        K8sClientMock.new_resources_not_ready.append(fake_cert('default', 'my-link', site['status']['defaultIssuer'], True))
        self.assertEqual(1, len(K8sClientMock.resources))
        with self.assertRaises(AnsibleFailJson) as fail:
            set_module_args({'name': 'my-link', 'type': 'link'})
            self.module.main()
        self.assertEqual(2, len(K8sClientMock.resources))
        self.assertTrue(fail.exception.failed)
        self.assertTrue(fail.exception.msg)

    def test_kube_generate_named_link(self):
        site = fake_site('default', 'my-site', True)
        K8sClientMock.resources.append(site)
        K8sClientMock.new_resources_hook_fns.append(create_secret_hook)
        self.assertEqual(1, len(K8sClientMock.resources))
        with self.assertRaises(AnsibleExitJson) as exit:
            set_module_args({'name': 'my-link', 'type': 'link'})
            self.module.main()
        self.assertEqual(3, len(K8sClientMock.resources))
        self.assertTrue(exit.exception.changed)
        self.assertTrue(exit.exception.token)
        token = list(yaml.safe_load_all(exit.exception.token))
        self.assertEqual(2, len(token))
        secret = token[0]
        cert = token[1]
        self.assertEqual('my-link', secret['metadata']['name'])
        self.assertEqual('my-link', cert['metadata']['name'])

    def test_kube_named_link_ready(self):
        site = fake_site('default', 'my-site', True)
        K8sClientMock.resources.append(site)
        K8sClientMock.resources.append(fake_cert('default', 'my-link', site['status']['defaultIssuer'], True, ready=True))
        K8sClientMock.resources.append(fake_secret('default', 'my-link'))
        self.assertEqual(3, len(K8sClientMock.resources))
        with self.assertRaises(AnsibleExitJson) as exit:
            set_module_args({'name': 'my-link', 'type': 'link'})
            self.module.main()
        self.assertEqual(3, len(K8sClientMock.resources))
        self.assertFalse(exit.exception.changed)
        self.assertTrue(exit.exception.token)
        token = list(yaml.safe_load_all(exit.exception.token))
        self.assertEqual(2, len(token))
        secret = token[0]
        cert = token[1]
        self.assertEqual('my-link', secret['metadata']['name'])
        self.assertEqual('my-link', cert['metadata']['name'])

    def test_kube_named_link_not_ready(self):
        site = fake_site('default', 'my-site', True)
        K8sClientMock.resources.append(site)
        K8sClientMock.resources.append(fake_cert('default', 'my-link', site['status']['defaultIssuer'], True, ready=False))
        K8sClientMock.resources.append(fake_secret('default', 'my-link'))
        self.assertEqual(3, len(K8sClientMock.resources))
        with self.assertRaises(AnsibleFailJson) as fail:
            set_module_args({'name': 'my-link', 'type': 'link'})
            self.module.main()
        self.assertEqual(3, len(K8sClientMock.resources))
        self.assertEqual('Certificate my-link exists in namespace and cannot be used', fail.exception.msg[1])

    def test_kube_named_link_no_client_cert_conflict(self):
        site = fake_site('default', 'my-site', True)
        K8sClientMock.resources.append(site)
        K8sClientMock.resources.append(fake_cert('default', 'my-server-cert', site['status']['defaultIssuer'], False, ready=True))
        K8sClientMock.resources.append(fake_secret('default', 'my-server-cert'))
        self.assertEqual(3, len(K8sClientMock.resources))
        with self.assertRaises(AnsibleFailJson) as fail:
            set_module_args({'name': 'my-server-cert', 'type': 'link'})
            self.module.main()
        self.assertEqual(3, len(K8sClientMock.resources))
        self.assertEqual('Certificate my-server-cert exists in namespace and cannot be used', fail.exception.msg[1])

    def test_kube_named_link_client_cert_other_issuer_conflict(self):
        site = fake_site('default', 'my-site', True)
        K8sClientMock.resources.append(site)
        K8sClientMock.resources.append(fake_cert('default', 'my-server-cert', 'some-other-issuer', False, ready=True))
        K8sClientMock.resources.append(fake_secret('default', 'my-server-cert'))
        self.assertEqual(3, len(K8sClientMock.resources))
        with self.assertRaises(AnsibleFailJson) as fail:
            set_module_args({'name': 'my-server-cert', 'type': 'link'})
            self.module.main()
        self.assertEqual(3, len(K8sClientMock.resources))
        self.assertEqual('Certificate my-server-cert exists in namespace and cannot be used', fail.exception.msg[1])

    def test_kube_named_link_secret_conflict(self):
        site = fake_site('default', 'my-site', True)
        K8sClientMock.resources.append(site)
        K8sClientMock.resources.append(fake_secret('default', 'my-link'))
        self.assertEqual(2, len(K8sClientMock.resources))
        with self.assertRaises(AnsibleFailJson) as fail:
            set_module_args({'name': 'my-link', 'type': 'link'})
            self.module.main()
        self.assertEqual(2, len(K8sClientMock.resources))
        self.assertEqual('Secret my-link exists in namespace and cannot be used', fail.exception.msg[1])


def fake_site(ns, name, ready):
    site = {
        "apiVersion": "skupper.io/v2alpha1",
        "kind": "Site",
        "metadata": {
            "name": name,
            "namespace": ns,
        }
    }
    if ready:
        add_ready_condition(site)
        site['status']['defaultIssuer'] = "skupper-site-ca"
        site['status']['endpoints'] = [{
            "group": "skupper-router",
            "host": "10.0.0.1",
            "name": "inter-router",
            "port": "55671",
        },
            {
            "group": "skupper-router",
            "host": "10.0.0.1",
            "name": "edge",
            "port": "45671"
        }]

    return site


def fake_grant(ns, name, redemptions=1, ready=True):
    grant = {
        "apiVersion": "skupper.io/v2alpha1",
        "kind": "AccessGrant",
        "metadata": {
            "name": name,
            "namespace": ns,
        },
        "spec": {
            "redemptionsAllowed": redemptions,
            "expirationWindow": "15m",
        },
    }
    if ready:
        add_ready_condition(grant)
        now = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=15)
        grant['status']['expirationTime'] = now.isoformat()
    return grant


def fake_cert(ns, name, issuer_name: str, client: bool, ready=True):
    cert = {
        "apiVersion": "skupper.io/v2alpha1",
        "kind": "Certificate",
        "metadata": {
            "name": name,
            "namespace": ns,
        },
        "spec": {
            "ca": issuer_name,
            "client": client,
            "subject": "subject"
        },
    }
    if ready:
        add_ready_condition(cert)
    return cert


def fake_secret(ns, name):
    secret = {
        "apiVersion": "v1",
        "kind": "Secret",
        "metadata": {
            "name": name,
            "namespace": ns,
        },
        "data": {
            "ca.crt": "ca",
            "tls.crt": "crt",
            "tls.key": "key"
        },
    }
    return secret


def add_ready_condition(resource):
    resource['status'] = {
        'conditions': [{
            'lastTransitionTime': datetime.datetime.now().isoformat(),
            'message': 'OK',
            'reason': 'Ready',
            'status': 'True',
            'type': 'Ready',
        }],
        'message': 'OK',
        'status': 'Ready',
    }


def has_ready_condition(resource: dict) -> bool:
    conditions = resource.get('status', {}).get('conditions', [])
    for condition in conditions:
        if condition.get("type", "") == "Ready" and condition.get("status", False):
            return True
    return False


def create_secret_hook(definition: dict):
    if definition.get("kind") != "Certificate" or not has_ready_condition(definition):
        return
    ns = definition.get("metadata", {}).get("namespace")
    name = definition.get("metadata", {}).get("name")
    K8sClientMock.resources.append(fake_secret(ns, name))
    return definition
