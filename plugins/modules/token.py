#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2025, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: token

short_description: Issue or retrieve access tokens and static links

version_added: "2.0.0"

description:
    - Manages Skupper Access Tokens and static links
    - Generates an AccessGrant and return a corresponding AccessToken (kubernetes platform only)
    - Returns an AccessToken for an existing AccessGrant (kubernetes platform only)
    - Retrieves a static Link based on provided subject alternative name or host (podman, docker and linux platforms)

options:
    name:
        description:
            - Name of the AccessGrant (to be generated or consumed) and AccessToken (kubernetes platform only) when using type V(token)
            - Name of the Link and Certificate (to be generated or consumed) (kubernetes platform only) when using type V(link)
            - Name of a RouterAccess (podman, docker or linux platforms)
        type: str
    redemptions_allowed:
        description:
            - The number of claims the generated AccessGrant is valid for
            - Only used when platform is V(kubernetes) and type is V(token)
        default: 1
        type: int
    expiration_window:
        description:
            - Duration of the generated AccessGrant
            - Sample values V(10m), V(2h)
            - Only used when platform is V(kubernetes) and type is V(token)
        default: 15m
        type: str
    type:
        description:
            - Type of token to produce or consume
            - Only meaningful when platform is V(kubernetes)
            - Always set to V(link) when platform is V(podman), V(docker), V(linux)
        default: token
        type: str
        choices: ['token', 'link']
    host:
        description:
            - Static link hostname
            - Only used when platform is V(podman), V(docker), V(linux)
        type: str

extends_documentation_fragment:
    - skupper.v2.common_options

requirements:
    - "python >= 3.9"
    - "kubernetes >= 24.2.0"
    - "PyYAML >= 3.11"

author:
    - Fernando Giorgetti (@fgiorgetti)
'''

RETURN = r"""
token:
  description:
  - AccessToken resource (yaml)
  - Link and Secret (yaml)
  returned: success
  type: str
"""

EXAMPLES = r'''
# Retrieve or issue an AccessToken (if my-grant does not exist or can be redeemed)
- name: Retrieve or issue my-grant AccessToken
  skupper.v2.token:
    name: my-grant
    platform: kubernetes
    namespace: west

# Retrieve or issue a Link (if my-link does not exist)
- name: Retrieve or create my-link Link
  skupper.v2.token:
    name: my-link
    type: link
    platform: kubernetes
    namespace: west

# Retrieving or generate a static Link
- name: Retrieve token
  skupper.v2.token:
    name: west-link
    type: link
    platform: kubernetes
    namespace: west

# Retrieving an accesstoken for any valid accessgrant
- name: Retrieve token
  skupper.v2.token:
    platform: kubernetes
    namespace: west

# Retrieving a Link for any existing site client certificate
- name: Retrieve Link
  skupper.v2.token:
    platform: kubernetes
    type: link
    namespace: west

# Retrieve a static Link for host my.nonkube.host
- name: Retrieve a static link
  skupper.v2.token:
    host: my.nonkube.host
    platform: podman
'''


import datetime
import time
import os
import glob
import copy
import sys
import typing as t
from ansible_collections.skupper.v2.plugins.module_utils.k8s import (
    K8sClient,
    has_condition
)
from ansible_collections.skupper.v2.plugins.module_utils.args import (
    common_args,
    is_valid_name,
    is_valid_host_ip
)
from ansible_collections.skupper.v2.plugins.module_utils.common import (
    is_non_kube,
    namespace_home,
)
from ansible_collections.skupper.v2.plugins.module_utils.exceptions import (
    K8sException,
    RuntimeException
)
from ansible.module_utils.basic import AnsibleModule
try:
    import yaml
except ImportError:
    pass
try:
    import dateutil
except ImportError:
    dateutil_found = False
else:
    dateutil_found = True


_ISO8601 = sys.version_info >= (3, 11)


def argspec():
    spec = copy.deepcopy(common_args())
    spec["name"] = dict(type="str", default=None, required=False)
    spec["host"] = dict(type="str", default=None, required=False)
    spec["redemptions_allowed"] = dict(type="int", default=1)
    spec["expiration_window"] = dict(type="str", default="15m")
    spec["type"] = dict(type="str", default="token", choices=["token", "link"])
    return spec


def mutualexc():
    return []


class TokenModule:
    max_attempts = 30
    retry_delay = 6

    def __init__(self, module: AnsibleModule):
        self.module = module
        self.name = self.params.get("name")
        self.host = self.params.get("host")
        self.platform = self.params.get("platform", "kubernetes")
        self.kubeconfig = self.params.get("kubeconfig") or \
            os.path.join(os.getenv("HOME"), ".kube", "config")
        self.context = self.params.get("context")
        self.namespace = self.params.get("namespace")
        if self.name and not is_valid_name(self.name):
            self.module.fail_json(
                "invalid name (rfc1123): {}".format(self.name))
        if self.namespace and not is_valid_name(self.namespace):
            self.module.fail_json(
                "invalid namespace (rfc1123): {}".format(self.namespace))
        if self.host and not is_valid_host_ip(self.host):
            self.module.fail_json("invalid host: {}".format(self.host))

    def run(self):
        result = dict(
            changed=False,
        )
        if self.module.check_mode:
            result['changed'] = True
            self.module.exit_json(**result)
        # self.module._debug = True

        changed = False
        token_link = ""

        if is_non_kube(self.platform):
            token_link = self.load_static_link()
        else:
            if self.params.get("type", "token") == "token":
                changed, token_link = self.process_token()
            else:
                changed, token_link = self.process_link()

        # adding return values
        if token_link:
            result['token'] = token_link

        result['changed'] = changed

        self.module.exit_json(**result)

    def process_token(self):
        changed = False
        try:
            token_link = self.load_from_grant(self.name)
        except RuntimeException as runtime_ex:
            self.module.fail_json(runtime_ex.msg)
        except K8sException as k8s_ex:
            self.module.fail_json(k8s_ex.msg)
        if not token_link:
            grant_name = self.name or "ansible-grant-%d" % (
                int(time.time()))
            try:
                if not self.generate_grant(grant_name):
                    self.module.fail_json(
                        "unable to create AccessGrant: '%s'" % (grant_name))
            except Exception as ex:
                self.module.fail_json(
                    "error creating AccessGrant: '%s' - reason: %s" % (grant_name, ex))
            changed = True
            try:
                token_link = self.load_from_grant(grant_name)
            except RuntimeException as runtime_ex:
                self.module.fail_json(runtime_ex.msg)
            except K8sException as k8s_ex:
                self.module.fail_json(k8s_ex.msg)
        return changed, token_link

    def process_link(self):
        k8s = K8sClient(self.kubeconfig, self.context)
        try:
            site = self.wait_ready(k8s, "Site")
        except RuntimeException as runtime_ex:
            self.module.fail_json(runtime_ex.msg)
        issuer_name = site.get("status").get("defaultIssuer")
        try:
            existing_client_certs = self.get_client_certificates(k8s, issuer_name)
        except K8sException as k8s_ex:
            self.module.fail_json(k8s_ex.msg)
        if self.name and self.name in existing_client_certs:
            secret = k8s.get(self.namespace, "v1", "Secret", self.name)
            return False, self.link_from_secret(site, secret)
        if self.name:
            # Name conflict, client cert not ready or not emitted by the site issuer
            if self.resource_exists(k8s, "skupper.io/v2alpha1", "Certificate", self.name):
                self.module.fail_json("Certificate {} exists in namespace and cannot be used"
                                      .format(self.name))
            if self.resource_exists(k8s, "v1", "Secret", self.name):
                self.module.fail_json("Secret {} exists in namespace and cannot be used"
                                      .format(self.name))
        elif existing_client_certs:
            secret = k8s.get(self.namespace, "v1", "Secret", existing_client_certs[0])
            return False, self.link_from_secret(site, secret)
        cert_name = self.generate_client_certificate(k8s, issuer_name)
        secret = k8s.get(self.namespace, "v1", "Secret", cert_name)
        return True, self.link_from_secret(site, secret)

    def resource_exists(self, k8s, version, kind, name) -> bool:
        try:
            resource = k8s.get(self.namespace, version, kind, name)
            if resource:
                return True
        except K8sException as k8s_ex:
            if k8s_ex.status != 404:
                self.module.fail_json(
                    "error retrieving {}/{} {} from namespace {}".format(kind, version, name, self.namespace))
        return False

    def link_from_secret(self, site, secret):
        secret_name = secret.get("metadata").get("name")
        del secret["metadata"]
        secret["metadata"] = {
            "name": secret_name
        }
        link = {
            "apiVersion": "skupper.io/v2alpha1",
            "kind": "Link",
            "metadata": {
                "name": secret_name,
            },
            "spec": {
                "endpoints": site.get("status").get("endpoints"),
                "tlsCredentials": secret_name,
            }
        }
        return yaml.safe_dump_all([link, secret], indent=2)

    def get_client_certificates(self, k8s, issuer_name):
        valid_client_certs = []
        try:
            certificates = k8s.get(self.namespace, "skupper.io/v2alpha1", "Certificate", "")
        except K8sException as k8s_ex:
            if k8s_ex.status == 404:
                return valid_client_certs
            raise k8s_ex
        for certificate in certificates:
            if certificate.get("spec", {}).get("ca") == issuer_name \
                    and certificate.get("spec", {}).get("client", False) \
                    and has_condition(certificate, "Ready"):
                valid_client_certs.append(certificate.get("metadata").get("name"))
        return valid_client_certs

    def generate_client_certificate(self, k8s, issuer_name):
        name = self.name or "link-%d" % (int(time.time()))
        certificate = {
            "apiVersion": "skupper.io/v2alpha1",
            "kind": "Certificate",
            "metadata": {
                "name": name,
                "namespace": self.namespace,
            },
            "spec": {
                "ca": issuer_name,
                "client": True,
                "subject": "{}-client".format(self.namespace)
            }
        }
        certificate_str = yaml.safe_dump(certificate, indent=2)
        try:
            k8s.create_or_patch(self.namespace, certificate_str, False)
        except K8sException as k8s_ex:
            self.module.fail_json("error creating certificate {}/{} - {}"
                                  .format(self.namespace, name, k8s_ex.msg))
        try:
            self.wait_ready(k8s, "Certificate", name)
        except RuntimeException as runtime_ex:
            self.module.fail_json(runtime_ex.msg)
        return name

    def load_static_link(self):
        home = namespace_home(self.namespace)
        links_path = os.path.join(home, "runtime", "links")
        links_search = os.path.join(
            links_path, "link-%s-%s.yaml" % (self.name or "*", self.host or "*"))
        links_found = glob.glob(links_search)
        links_found.sort()
        for link in links_found:
            with open(link, "r", encoding='utf-8') as f:
                link_content = f.read()
                return link_content
        return ""

    def can_be_redeemed(self, access_grant: dict) -> bool:
        allowed = access_grant.get("spec", {}).get("redemptionsAllowed", 0)
        redeemed = access_grant.get("status", {}).get("redemptions", 0)
        now = datetime.datetime.now(datetime.timezone.utc)
        if _ISO8601:
            exp_time = datetime.datetime.fromisoformat(access_grant.get("status", {}).get("expirationTime", now.isoformat()))
        elif dateutil_found:
            exp_time = dateutil.parser.isoparse(access_grant.get("status", {}).get("expirationTime", now.isoformat()))
        else:
            self.module.warn("unable to parse iso8601 time, grant expiration time will not be validated")
            exp_time = datetime.datetime.now(datetime.timezone.utc)
        return redeemed < allowed and now < exp_time

    def load_from_grant(self, name: str) -> str:
        k8s = K8sClient(self.kubeconfig, self.context)
        self.wait_ready(k8s, "Site")
        access_grant = {}
        found_not_ready = False
        for attempt in range(self.max_attempts):
            self.module.debug("retrieving accessgrants attempt %d/%d"
                              % (attempt, self.max_attempts))
            access_grants = None
            try:
                access_grants = k8s.get(
                    self.namespace, "skupper.io/v2alpha1", "AccessGrant", name)
            except K8sException as ex:
                if ex.status != 404:
                    raise ex
            if not access_grants or len(access_grants) == 0:
                break
            # give them a chance to be ready
            if isinstance(access_grants, dict):
                if has_condition(access_grants, "Ready"):
                    found_not_ready = False
                    access_grant = access_grants
                    break
                found_not_ready = True
            if isinstance(access_grants, list):
                access_grant, all_ready = self._load_from_list(access_grants)
                if all_ready or access_grant:
                    break
            time.sleep(self.retry_delay)

        if found_not_ready:
            raise RuntimeException(
                msg="accessgrant '%s' is not ready" % (name))

        if len(access_grant) == 0:
            return ""

        if name:
            if not has_condition(access_grant, "Ready"):
                raise RuntimeException(
                    msg="accessgrant '%s' cannot be redeemed" % (name))
            if not self.can_be_redeemed(access_grant):
                self.module.warn(
                    "accessgrant '{}' cannot be redeemed".format(name))

        access_token_name = "token-%s" % (
            access_grant.get("metadata").get("name"))
        access_token_code = access_grant.get("status").get("code")
        access_token_url = access_grant.get("status").get("url")
        access_token_ca = access_grant.get("status").get("ca")
        access_token = {
            "apiVersion": "skupper.io/v2alpha1",
            "kind": "AccessToken",
            "metadata": {
                "name": access_token_name,
            },
            "spec": {
                "code": access_token_code,
                "url": access_token_url,
                "ca": access_token_ca,
            }
        }
        return yaml.safe_dump(access_token, indent=2)

    def wait_ready(self, k8s, kind, name=""):
        for attempt in range(self.max_attempts):
            try:
                resources = k8s.get(
                    self.namespace, "skupper.io/v2alpha1", kind, name)
                if not resources:
                    raise RuntimeException(
                        'no {} found on namespace "{}"'.
                        format(kind + (("/" + name) if name else ""), self.namespace or "default")
                    )
                if isinstance(resources, dict):
                    resources = [resources]
                for resource in resources:
                    if has_condition(resource, "Ready"):
                        return resource
            except K8sException as ex:
                if ex.status != 404:
                    raise ex
            time.sleep(self.retry_delay)
        raise RuntimeException(
            'no ready {} found on namespace "{}"'.
            format(kind + (("/" + name) if name else ""), self.namespace or "default")
        )

    def _load_from_list(self, access_grants) -> t.Tuple[dict, bool]:
        all_ready = True
        access_grant = {}
        for access_grant_it in access_grants:
            if not has_condition(access_grant_it, "Ready"):
                all_ready = False
                continue
            if not access_grant and self.can_be_redeemed(access_grant_it):
                access_grant = access_grant_it
        return access_grant, all_ready

    def generate_grant(self, name: str):
        k8s = K8sClient(self.kubeconfig, self.context)
        access_grant_dict = {
            "apiVersion": "skupper.io/v2alpha1",
            "kind": "AccessGrant",
            "metadata": {
                    "name": name,
            },
            "spec": {
                "redemptionsAllowed": self.params.get("redemptions_allowed"),
                "expirationWindow": self.params.get("expiration_window"),
            }
        }
        access_grant_def = yaml.safe_dump(access_grant_dict, indent=2)
        return k8s.create_or_patch(self.namespace, access_grant_def, False)

    @property
    def params(self):
        return self.module.params


def main():
    module = AnsibleModule(
        argument_spec=argspec(),
        mutually_exclusive=mutualexc(),
        supports_check_mode=True
    )
    resource = TokenModule(module)
    resource.run()


if __name__ == '__main__':
    main()
