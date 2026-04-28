#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2025, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r'''
---
module: resource

short_description: Place skupper resources (yaml) in the provided namespace

version_added: "2.0.0"

description:
    Place skupper resources (yaml) in the provided namespace. If platform is
    kubernetes (default) the resources are applied to the respective namespace.
    In case a different platform is used, the resources will be placed into the
    correct location for the namespace on the file system.

options:
    path:
        description:
            - Path where resources are located (yaml and yml files).
            - Path can be a directory, a file or an http URL.
            - If remote is true (default is V(false)), the resources will not be copied from the control node.
            - URLs are always fetch from the inventory host.
            - Mutually exclusive with def
        type: str
    def:
        description:
        - YAML representation of a custom resource.
        - It can contain multiple YAML documents.
        type: str
        aliases: [ definition ]
    remote:
        description:
        - Determines if the resources are located at the inventory host instead of the control node.
        default: false
        type: bool
    state:
        description:
        - V(present) means that if the resource does not exist, it will be created. If it exists, no change is made.
        - V(latest) means that if the resource does not exist it will be created or updated with the latest provided definition.
        - V(absent) means that the resource will be removed.
        type: str
        default: "present"
        choices: ["present", "latest", "absent"]
    redeem:
        description:
        - For non-kubernetes platforms (for example V(podman), V(docker), or V(linux)), redeem C(AccessToken) documents without keeping them in the namespace; only Secret and Link are applied.
        - Other documents in the same definition are applied first. With C(spec.url) and C(spec.code), uses HTTP (as C(skupper token redeem)).
        - When V(platform) is V(kubernetes), this option is ignored and a warning is issued; the Skupper V2 controller on Kubernetes already handles AccessToken resources.
        type: bool
        default: false

extends_documentation_fragment:
  - skupper.v2.common_options

requirements:
  - "python >= 3.9"
  - "kubernetes >= 24.2.0"
  - "PyYAML >= 3.11"

author:
    - Fernando Giorgetti (@fgiorgetti)
'''

EXAMPLES = r'''
# Applying resources to a kubernetes cluster
- name: Apply Skupper Resources
  skupper.v2.resource:
    path: /home/user/west/crs
    platform: kubernetes
    namespace: west

# Applying remote resources to a kubernetes cluster
- name: Apply Skupper Resources
  skupper.v2.resource:
    path: /remote/home/user/west/crs
    remote: true
    platform: kubernetes
    namespace: west

# Applying resources to a non-kube namespace
- name: Apply Skupper Resources
  skupper.v2.resource:
    path: /home/user/west/crs
    platform: podman
    namespace: west

# Define a single resource
- name: Define resources for west site
  skupper.v2.resource:
    namespace: west
    def: |
      ---
      apiVersion: skupper.io/v2alpha1
      kind: Site
      metadata:
        name: west
      spec:
        linkAccess: default
      ---
      apiVersion: skupper.io/v2alpha1
      kind: Listener
      metadata:
        name: backend
      spec:
        host: backend
        port: 8080
        routingKey: backend

- name: Redeem access token on a non-kubernetes site (apply Secret/Link only)
  skupper.v2.resource:
    namespace: east
    platform: podman
    def: "{{ access_token_yaml }}"
    redeem: true
  register: out
'''

RETURN = r'''
redeemed_links:
  description: List of YAML strings per redeemed token when C(redeem=true) on a non-kubernetes platform. Each string contains all Secret documents from the redeem response, then all Link documents (each group in server response order).
  type: list
  returned: when redeem is used on non-kubernetes and AccessToken documents were present
redeem_failures:
  description: List of dicts C(name), C(msg) for HTTP redemption failures on non-kubernetes. The module does not fail; warnings are issued so a repeat run can stay idempotent (for example unchanged with a warning).
  type: list
  returned: when one or more AccessToken redemptions failed
'''


import copy
import os
import tempfile
import traceback
import typing as t

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore
    YAML_IMPORT_ERROR = traceback.format_exc()
else:
    YAML_IMPORT_ERROR = None
HAS_YAML = yaml is not None

from ansible.module_utils.urls import fetch_url, open_url
from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible_collections.skupper.v2.plugins.module_utils.k8s import K8sClient
from ansible_collections.skupper.v2.plugins.module_utils.resource import (
    load,
    dump,
    delete as resource_delete,
)
from ansible_collections.skupper.v2.plugins.module_utils.common import is_non_kube
from ansible_collections.skupper.v2.plugins.module_utils.exceptions import RuntimeException
from ansible_collections.skupper.v2.plugins.module_utils.args import common_args, is_valid_name

def _split_access_tokens(definitions: str) -> t.Tuple[str, t.List[dict]]:
    other, tokens = [], []
    for doc in yaml.safe_load_all(definitions):
        if isinstance(doc, dict) and doc.get("kind") == "AccessToken":
            tokens.append(doc)
        elif isinstance(doc, dict):
            other.append(doc)
    return (yaml.safe_dump_all(other, indent=2) if other else ""), tokens


def argspec():
    spec = copy.deepcopy(common_args())
    spec["path"] = dict(type="str", default=None, required=False)
    spec["def"] = dict(type="str", default=None,
                       required=False, aliases=["definition"])
    spec["remote"] = dict(type="bool", default=False, required=False)
    spec["state"] = dict(type="str", default="present", required=False, choices=[
                         "present", "latest", "absent"])
    spec["redeem"] = dict(type="bool", default=False)
    return spec


def mutualexc():
    return [
        ("path", "def"),
        ("def", "remote"),
    ]


def _http_redeem_token(token_doc: dict, subject_ns: str) -> str:
    spec = token_doc.get("spec") or {}
    url, code = spec.get("url"), spec.get("code")
    if not url or not code:
        raise ValueError("AccessToken needs spec.url and spec.code for HTTP redemption")
    name = (token_doc.get("metadata") or {}).get("name")
    if not name:
        raise ValueError("AccessToken needs metadata.name")
    kwargs = dict(method="POST", data=code.encode("utf-8"),
                  headers={"name": name, "subject": subject_ns}, timeout=60)
    ca = spec.get("ca") or ""
    tmp = None
    if ca:
        fd, tmp = tempfile.mkstemp(suffix=".pem")
        try:
            with os.fdopen(fd, "w") as f:
                f.write(ca)
            kwargs["ca_path"] = tmp
        except Exception:
            if tmp:
                try:
                    os.unlink(tmp)
                except OSError:
                    pass
            raise
    try:
        raw = open_url(url, **kwargs).read()
        body = raw.decode("utf-8") if isinstance(raw, bytes) else raw
    finally:
        if tmp and os.path.isfile(tmp):
            try:
                os.unlink(tmp)
            except OSError:
                pass
    secrets, links, bad_kinds = [], [], []
    for d in yaml.safe_load_all(body):
        if not isinstance(d, dict):
            continue
        kind = d.get("kind")
        if kind == "Secret":
            secrets.append(d)
        elif kind == "Link":
            links.append(d)
        elif kind:
            bad_kinds.append(kind)
    if bad_kinds:
        raise ValueError(
            "Redeem response must only contain Secret and Link documents; found: {}".format(
                sorted(set(bad_kinds))
            )
        )
    if not secrets:
        raise ValueError("Redeem response must include at least one Secret document")
    if not links:
        raise ValueError("Redeem response must include at least one Link document")
    # Stable bundle: all Secrets (in response order), then all Links (in response order).
    out = secrets + links
    return yaml.safe_dump_all(out, indent=2)


class ResourceModule:
    def __init__(self, module: AnsibleModule):
        self.module = module

    def run(self):
        result = dict(changed=False)
        if self.module.check_mode:
            result["changed"] = True
            self.module.exit_json(**result)

        definition_found = False
        definitions = ""
        platform = self.params["platform"]
        if "path" in self.params and self.params["path"]:
            try:
                definitions, definition_found = self.load_from_path(platform)
            except RuntimeException as ex:
                self.module.fail_json(msg=ex.msg)
        elif "def" in self.params and self.params["def"]:
            definition_found = True
            definitions = self.params["def"]

        if not definition_found:
            self.module.fail_json(msg="no resource definition or path provided")

        redeem_requested = self.params.get("redeem", False)
        if redeem_requested and not is_non_kube(platform):
            self.module.warn(
                "redeem is ignored when platform is kubernetes; "
                "the Skupper V2 controller already handles AccessToken resources."
            )
        redeem = redeem_requested and is_non_kube(platform)
        if redeem and not HAS_YAML:
            self.module.fail_json(
                msg=missing_required_lib("PyYAML"),
                exception=YAML_IMPORT_ERROR,
            )

        changed = False
        state = self.params.get("state", "present")
        overwrite = state == "latest"

        try:
            if is_non_kube(platform):
                namespace = self.params["namespace"] or "default"
                if not is_valid_name(namespace):
                    self.module.fail_json(msg="invalid namespace (rfc1123): {}".format(namespace))
                if state == "absent":
                    changed = resource_delete(definitions, namespace)
                elif redeem:
                    wo, tokens = _split_access_tokens(definitions)
                    if wo.strip():
                        changed = dump(wo, namespace, overwrite)
                    redeemed, rch, redeem_fails = self._redeem_nonkube(namespace, tokens)
                    if redeemed:
                        result["redeemed_links"] = redeemed
                    if redeem_fails:
                        result["redeem_failures"] = redeem_fails
                    changed = changed or rch
                else:
                    changed = dump(definitions, namespace, overwrite)
            else:
                k8s = K8sClient(self.params.get("kubeconfig"), self.params.get("context"))
                namespace = self.params.get("namespace")
                if state == "absent":
                    changed = k8s.delete(namespace, definitions)
                else:
                    changed = k8s.create_or_patch(namespace, definitions, overwrite)
        except Exception as ex:
            self.module.fail_json(msg=str(ex))

        result["changed"] = changed
        self.module.exit_json(**result)

    def _redeem_nonkube(
        self, namespace: str, tokens: t.List[dict]
    ) -> t.Tuple[t.List[str], bool, t.List[dict]]:
        if not tokens:
            return [], False, []
        ns = namespace or "default"
        out, fails = [], []
        redeem_changed = False
        seen = set()
        for doc in tokens:
            n = (doc.get("metadata") or {}).get("name")
            if not n or n in seen:
                continue
            seen.add(n)
            try:
                bundle = _http_redeem_token(doc, ns)
                if dump(bundle, ns, True):
                    redeem_changed = True
                out.append(bundle)
            except Exception as ex:
                fails.append({"name": n, "msg": str(ex)})
        if fails:
            self.module.warn(
                "Could not redeem {} AccessToken(s) ({}). See redeem_failures in module result.".format(
                    len(fails),
                    ", ".join(f["name"] for f in fails),
                )
            )
        return out, redeem_changed, fails

    def load_from_path(self, platform) -> t.Tuple[str, bool]:
        if self.params["path"].startswith(("http://", "https://")):
            try:
                fetch_res, fetch_info = fetch_url(
                    self.module, url=self.params["path"])
                if fetch_info["status"] != 200:
                    self.module.fail_json(msg="failed to fetch url %s , error was: %s" % (
                        self.params["path"], fetch_info["msg"]))
                return fetch_res.read(), True
            except Exception as ex:
                raise RuntimeException("error fetching url %s: %s"
                                       % (self.params["path"], ex)) from ex
        return load(self.params["path"], platform), True

    @property
    def params(self):
        return self.module.params


def main():
    module = AnsibleModule(
        argument_spec=argspec(),
        mutually_exclusive=mutualexc(),
        supports_check_mode=True,
    )
    ResourceModule(module).run()


if __name__ == "__main__":
    main()
