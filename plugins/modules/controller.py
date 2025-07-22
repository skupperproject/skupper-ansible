#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2025, Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r'''
---
module: controller
short_description: Manages the lifecycle of the skupper-controller for system sites
version_added: "2.1.0"
description:
    - Manages the lifecycle of the skupper-controller.
    - Prepares the environment and runs the skupper-controller for system sites
    - Runs with podman (default) or docker engines

options:
    action:
        description:
            - V(install) - Prepares the environment and runs the skupper-controller
            - V(uninstall) - Adjusts the local environment and removes the skupper-controller
        type: str
        choices: ["install", "uninstall"]
        default: install
    image:
        description:
            - The controller-image to use
        type: str
        default: quay.io/skupper/system-controller:v2-dev
    engine:
        description:
            - The container engine used to run the controller for system sites
        type: str
        default: podman
        choices: ["podman", "docker"]

requirements:
    - "python >= 3.9"
    - "PyYAML >= 3.11"

author:
    - Fernando Giorgetti (@fgiorgetti)
'''

RETURN = r"""
"""

EXAMPLES = r'''
# Installs the skupper-controller using podman
- name: Installs the skupper-controller using podman
  skupper.v2.controller:
    action: install
    engine: podman

# Uninstalls the skupper-controller
- name: Installs the skupper-controller
  skupper.v2.controller:
    action: uninstall

'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.skupper.v2.plugins.module_utils.command import (
    run_command
)
from ansible_collections.skupper.v2.plugins.module_utils.container import (
    container_exists,
)
from ansible_collections.skupper.v2.plugins.module_utils.system import (
    base_mounts,
    mounts,
    env,
    runas,
    userns,
    create_service,
    delete_service,
    service_exists,
    systemd_create
)
from ansible_collections.skupper.v2.plugins.module_utils.resource import (
    load,
    version_kind
)
from ansible_collections.skupper.v2.plugins.module_utils.common import (
    is_non_kube,
    data_home,
    namespace_home,
    resources_home,
    service_dir
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
    spec = dict()
    spec["action"] = dict(type="str", default="install",
                          choices=["install", "uninstall"])
    spec["image"] = dict(type="str",
                         default="quay.io/skupper/cli:v2-dev")
    spec["engine"] = dict(type="str", default="podman",
                          choices=["podman", "docker"])
    return spec


class ControllerModule:
    def __init__(self, module: AnsibleModule):
        self.module = module
        self._action = self.params.get("action")
        self._image = self.params.get("image")
        self._engine = self.params.get("engine")

    def run(self):
        result = dict(
            changed=False,
        )
        if self.module.check_mode:
            result['changed'] = True
            self.module.exit_json(**result)

        # self.module._debug = True

        changed = False
        # pylint: disable=unnecessary-lambda
        changed = {
            'install': lambda: self.install(strategy="install"),
            'uninstall': lambda: self.uninstall(strategy="uninstall")
        }[self._action]()

        # preparing response
        result['changed'] = changed
        self.module.exit_json(**result)

    @property
    def params(self):
        return self.module.params

    def install(self) -> bool:
        self.module.debug("installing on namespace: %s" % (self.namespace))

        if self.platform == "linux":
            self.module.fail_json("controller is not yet supported with the selected " \
            "platform: 'linux' - you can still use 'podman' or 'docker'")

        if self.service_exists():
            self.module.debug("skupper-controller service already exists")
            return False
        
        if self.container_already_exists():
            self.module.debug("{} container already exists".format(self.container_name()))
            return False

        command = [
            self._engine, "run", "--pull", "always", "--name",
            self.container_name(),
            "--network", "host", "--security-opt", "label=disable", "-u",
            runas(self._engine), "--userns=%s" % (userns(self._engine))
        ]
        requires_mounts_for = list()
        for source, dest in base_mounts(self.platform, self._engine).items():
            requires_mounts_for.append(source)
            command.extend(["-v", "%s:%s:z" % (source, dest)])
        env_dict = env(self.platform, self._engine)
        for var, val in env_dict.items():
            command.extend(["-e", "%s=%s" % (var, val)])
        command.append(self._image)

        code, out, err = run_command(self.module, command)
        if code != 0:
            msg = "error creating container '%s': %s" % (
                self.container_name(), out or err)
            self.module.fail_json(msg)
            return False

        try:
            self.create_startup_scripts(self.module, self._engine)
        except Exception as ex:
            self.module.fail_json("unable to create startup scripts: {}".format(ex))
        try:
            self.create_service(self.module, mounts=requires_mounts_for, envs=env_dict)
        except Exception as ex:
            self.module.fail_json("unable to create systemd service: {}".format(ex))

        return True

    def uninstall(self) -> bool:
        return False 
    
    def service_name(self) -> str:
        return "skupper-controller.service"

    def service_exists(self) -> bool:
        return service_exists(self.module, self.service_name())

    def create_startup_scripts(self, engine: str):
        base_path = "{}/system-controller/internal/scripts/".format(data_home())
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        def write_header(file):
            file.write("#!/usr/bin/env sh")
            file.write("")
            file.write("set -o errexit")
            file.write("set -o nounset")
        start_file = "{}/start.sh".format(base_path)
        stop_file = "{}/stop.sh".format(base_path)
        with open(start_file, "w", encoding="utf-8") as out_file:
            write_header(out_file)
            out_file.write("{} start {}".format(engine, self.container_name()))
        with open(stop_file, "w", encoding="utf-8") as out_file:
            write_header(out_file)
            out_file.write("{} stop -t 10 {}".format(engine, self.container_name()))

    def create_service(self, mounts=list(), envs=dict()):
        startup_scripts_path = "{}/system-controller/internal/scripts/".format(data_home())
        service_file = "{}/{}".format(service_dir(), self.service_name())
        with open(service_file, "w", encoding="utf-8") as out_file:
            out_file.write("[Unit]")
            out_file.write("Description=skupper-controller")
            out_file.write("After=network-online.target")
            out_file.write("Wants=network-online.target")
            for mount in mounts:          
                out_file.write("RequiresMountsFor={}".format(mount))
            out_file.write("")
            out_file.write("[Service]")
            out_file.write("TimeoutStopSec=70")
            out_file.write("RemainAfterExit=yes")
            for var, val in envs.items():
                out_file.write("Environment={}={}".format(var, val))
            out_file.write("ExecStart=/bin/bash {}/start.sh".format(startup_scripts_path))
            out_file.write("ExecStop=/bin/bash {}/stop.sh".format(startup_scripts_path))
            out_file.write("Type=simple")
            out_file.write("")
            out_file.write("[Install]")
            out_file.write("WantedBy=default.target")
        return systemd_create(self.module, self.service_name(), service_file)
    
    def container_name(self) -> str:
        # user-skupper-controller
        container_name = "{}-skupper-controller".format(os.getlogin())
        return container_name

    def container_already_exists(self) -> bool:
        return container_exists(self.module, self.container_name)


def main():
    module = AnsibleModule(
        argument_spec=argspec(),
        mutually_exclusive=[],
        supports_check_mode=True
    )
    resource = ControllerModule(module)
    resource.run()


if __name__ == '__main__':
    main()
