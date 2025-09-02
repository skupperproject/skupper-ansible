#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2025, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r'''
---
module: system
short_description: Manages the lifecycle of non-kube namespaces
version_added: "2.0.0"
description:
    - Manages the lifecycle of non-kube namespaces.
    - Executes the provided action for a non-kube site definition on a given namespace
    - It can be used to setup, reload, start, stop and teardown a namespace definition
    - It has the ability to produce a self-extracting or a tarball bundle
    - Runs with podman (default) or docker binaries
    - Only valid for platforms "podman", "docker" and "linux"

options:
    action:
        description:
            - The action to perform against a given namespace definition
            - V(setup) - a new site is initialized and started (no-op if namespace is already initialized)
            - V(reload) - a site is created or re-initialized (Certificate Authorities are preserved)
            - V(start) - components are started
            - V(stop) - components are stopped
            - V(teardown) - stops and removes a site definition
            - V(bundle) - generates a self-extracting bundle
            - V(tarball) - generates a tarball bundle
        type: str
        choices: ["setup", "reload", "start", "stop", "teardown", "bundle", "tarball"]
        default: setup
    image:
        description:
            - The image used to initialize your site or bundle
        type: str
        default: quay.io/skupper/cli:2.0.1
    engine:
        description:
            - The container engine used to manage a namespace or produce a bundle
            - The default value is podman, but if platform is set to docker, it will use docker as the engine as well
            - It is also used when the platform is set to systemd or when action is bundle or tarball (otherwise the platform value is used)
        type: str
        default: podman
        choices: ["podman", "docker"]
extends_documentation_fragment:
    - skupper.v2.common_options

requirements:
    - "python >= 3.9"
    - "PyYAML >= 3.11"

author:
    - Fernando Giorgetti (@fgiorgetti)
'''

RETURN = r"""
path:
    description:
        - Path to the generated namespace or to a produced site bundle
    returned: success
    type: str
bundle:
    description:
        - Base 64 encoded content of the generated bundle or tarball
        - Only populated when action is bundle or tarball
    returned: success
    type: str
links:
    description:
        - Static links generated for non-kube sites with a RouterAccess
        - Dictionary keys are the target hostname or ip of the link
        - Each value has a valid link that can be applied to another site
    returned: when platform in ('podman', 'docker', 'linux') and a RouterAccess is defined
    type: dict
    sample: {'my.host': '---\napiVersion: skupper.io/v2alpha1...'}
"""

EXAMPLES = r'''
# Initializes the default namespace based on existing resources
- name: Initialize the default namespace using podman
  skupper.v2.system:

# Initializes the west namespace using docker
- name: Initialize the west namespace using docker
  skupper.v2.system:
    platform: docker
    namespace: west

# Reloads the definitions for the west namespace
- name: Initialize the west namespace
  skupper.v2.system:
    action: reload
    namespace: west

# Removes a site definition from the west namespace
- name: Removes the west namespace
  skupper.v2.system:
    action: teardown
    namespace: west

# Stops the skupper components on a given namespace
- name: Stops the components on the east namespace
  skupper.v2.system:
    action: stop
    namespace: east

# Starts the skupper components on a given namespace
- name: Starts the components on the east namespace
  skupper.v2.system:
    action: start
    namespace: east

# Produces a self-extracting site bundle based on the default namespace definitions
- name: Generate a self-extracting site bundle
  skupper.v2.system:
    action: bundle
    register: result

# Produces a tarball bundle based on the west namespace definitions
- name: Generate a tarball bundle based on west namespace definitions
  skupper.v2.system:
    action: tarball
    namespace: west
    register: result
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.skupper.v2.plugins.module_utils.command import (
    run_command
)
from ansible_collections.skupper.v2.plugins.module_utils.system import (
    mounts,
    env,
    runas,
    userns,
    create_service,
    delete_service,
    start_service,
    stop_service
)
from ansible_collections.skupper.v2.plugins.module_utils.resource import (
    load,
    version_kind
)
from ansible_collections.skupper.v2.plugins.module_utils.common import (
    is_non_kube,
    data_home,
    namespace_home,
    resources_home
)
from ansible_collections.skupper.v2.plugins.module_utils.args import (
    common_args,
    is_valid_name
)
import copy
import base64
import shutil
import os
import time
import glob
try:
    import yaml
except ImportError:
    pass


def argspec():
    spec = copy.deepcopy(common_args())
    spec["action"] = dict(type="str", default="setup",
                          choices=["setup", "reload", "teardown",
                                   "stop", "start", "bundle", "tarball"])
    spec["image"] = dict(type="str",
                         default="quay.io/skupper/cli:2.0.1")
    spec["engine"] = dict(type="str", default="podman",
                          choices=["podman", "docker"])
    return spec


class SystemModule:
    def __init__(self, module: AnsibleModule):
        self.module = module
        self._action = self.params.get("action")
        self._image = self.params.get("image")
        self._engine = self.params.get("engine")
        self.platform = self.params.get("platform") or "podman"
        if self.platform == "docker":
            self._engine = "docker"
        self.namespace = self.params.get("namespace") or "default"
        if not is_non_kube(self.platform):
            self.platform = "podman"
        if self.namespace and not is_valid_name(self.namespace):
            self.module.fail_json(
                "invalid namespace (rfc1123): {}".format(self.namespace))

    def run(self):
        result = dict(
            changed=False,
        )
        if self.module.check_mode:
            result['changed'] = True
            self.module.exit_json(**result)

        # self.module._debug = True

        changed = False
        path = namespace_home(self.namespace)
        # pylint: disable=unnecessary-lambda
        changed = {
            'setup': lambda: self.setup(),
            'reload': lambda: self.setup(force=True),
            'teardown': lambda: self.teardown(self.namespace),
            'start': lambda: start_service(self.module, self.namespace),
            'stop': lambda: stop_service(self.module, self.namespace),
            'bundle': lambda: self.setup(strategy="bundle"),
            'tarball': lambda: self.setup(strategy="tarball")
        }[self._action]()

        # handling bundle return
        if changed and self._action in ("bundle", "tarball"):
            site_name = self._read_site_name()
            path = ""
            if site_name:
                ext = "sh" if self._action == "bundle" else "tar.gz"
                file_name = "skupper-install-%s.%s" % (site_name, ext)
                path = os.path.join(data_home(), "bundles", file_name)
                with open(path, 'rb') as bundle:
                    bundle_encoded = base64.b64encode(bundle.read())
                    result['bundle'] = bundle_encoded.decode('utf-8')
        if self._action in ("setup", "reload"):
            result["links"] = self.load_static_links()

        # preparing response
        result["path"] = path
        result['changed'] = changed
        self.module.exit_json(**result)

    @property
    def params(self):
        return self.module.params

    def setup(self, force: bool = False, strategy: str = "") -> bool:
        self.module.debug("namespace: %s" % (self.namespace))
        runtime_dir = os.path.join(namespace_home(self.namespace), "runtime")
        if not strategy and os.path.isdir(runtime_dir) and not force:
            self.module.warn("namespace '%s' already exists" %
                             (self.namespace))
            return False
        resources_home_dir = resources_home(self.namespace)
        if not os.path.isdir(resources_home_dir):
            self.module.fail_json(
                "no resources found at: {}".format(resources_home_dir))

        command = [
            self._engine, "run", "--rm", "--name",
            "skupper-setup-%d" % (int(time.time())),
            "--network", "host", "--security-opt", "label=disable", "-u",
            runas(self._engine), "--userns=%s" % (userns(self._engine))
        ]
        for source, dest in mounts(self.namespace, self.platform, self._engine).items():
            command.extend(["-v", "%s:%s:z" % (source, dest)])
        for var, val in env(self.platform, self._engine).items():
            command.extend(["-e", "%s=%s" % (var, val)])
        self.module.debug("SKUPPER_ROUTER_IMAGE: {}".format(os.environ.get("SKUPPER_ROUTER_IMAGE")))
        command.append(self._image)
        command.extend(["-n", self.namespace, "system", "setup"])
        if strategy:
            command.extend(["-b", strategy])
        elif force:
            command.append("-f")

        code, out, err = run_command(self.module, command)
        if code != 0:
            msg = "error setting up '%s' namespace: %s" % (
                self.namespace, out or err)
            self.module.fail_json(msg)
            return False

        if not strategy:
            create_service(self.module, self.namespace)

        return True

    def teardown(self, namespace: str = "default") -> bool:
        internal_dir = os.path.join(namespace_home(namespace), "internal")
        changed = False
        if not os.path.isdir(internal_dir):
            return changed
        changed = delete_service(self.module, namespace)
        platform_file_name = os.path.join(internal_dir, "platform.yaml")
        with open(platform_file_name, "r", encoding='utf-8') as platform_file:
            platform_obj = yaml.safe_load(platform_file)
            platform = platform_obj.get("platform", "")
            if platform in ("podman", "docker"):
                container = "%s-skupper-router" % (namespace)
                remove_cmd = [platform, "rm", "-f", container]
                code, out, err = run_command(self.module, remove_cmd)
                if code == 0:
                    changed = True
                else:
                    self.module.warn(
                        "error removing container '%s': %s" % (container, err))
        try:
            shutil.rmtree(namespace_home(namespace))
            changed = True
        except Exception as ex:
            self.module.fail_json(
                "unable to remove '%s' namespace definition: %s" % (namespace, ex))
        return changed

    def load_static_links(self) -> dict:
        links = dict()
        home = namespace_home(self.namespace)
        links_path = os.path.join(home, "runtime", "links")
        links_search = os.path.join(links_path, "*.yaml")
        links_found = glob.glob(links_search)
        links_found.sort()
        for link in links_found:
            with open(link, 'r', encoding='utf-8') as f:
                link_content = f.read()
                for obj in yaml.safe_load_all(link_content):
                    if not isinstance(obj, dict) or obj.get("kind", "") != "Link":
                        continue
                    for endpoint in obj.get("spec", {}).get("endpoints", []):
                        host = endpoint.get("host", "")
                        if host:
                            links[host] = link_content
        return links

    def _read_site_name(self) -> str:
        home = namespace_home(self.namespace)
        resources_path = os.path.join(home, "input", "resources")
        resources_str = load(resources_path, self.platform)
        site_name = ""
        for res in yaml.safe_load_all(resources_str):
            if not res or not isinstance(res, dict):
                continue
            kind = version_kind(res)[1]
            if kind != "Site":
                continue
            site_name = res.get("metadata", {}).get("name", "")
            break
        if not site_name:
            self.module.warn(
                "unable to identify site name on namespace: '%s'" % (self.namespace))
        return site_name


def main():
    module = AnsibleModule(
        argument_spec=argspec(),
        mutually_exclusive=[],
        supports_check_mode=True
    )
    resource = SystemModule(module)
    resource.run()


if __name__ == '__main__':
    main()
