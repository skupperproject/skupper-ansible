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
    platform:
        description:
            - The platform used to run the controller for system sites
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
    platform: podman

# Uninstalls the skupper-controller
- name: Uninstalls the skupper-controller
  skupper.v2.controller:
    action: uninstall
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.skupper.v2.plugins.module_utils.command import (
    run_command
)
from ansible_collections.skupper.v2.plugins.module_utils.container import (
    container_info,
)
from ansible_collections.skupper.v2.plugins.module_utils.system import (
    base_mounts,
    env,
    runas,
    userns,
    service_exists,
    systemd_create,
    systemd_delete,
    enable_podman_socket
)
from ansible_collections.skupper.v2.plugins.module_utils.common import (
    data_home,
    service_dir
)
import shutil
import os
import pwd


def argspec():
    spec = dict()
    spec["action"] = dict(type="str", default="install",
                          choices=["install", "uninstall"])
    spec["image"] = dict(type="str",
                         default="quay.io/skupper/system-controller:v2-dev")
    spec["platform"] = dict(type="str", default="podman",
                            choices=["podman", "docker"])
    return spec


class ControllerModule:
    def __init__(self, module: AnsibleModule):
        self.module = module
        self._action = self.params.get("action")
        self._image = self.params.get("image")
        self._platform = self.params.get("platform")

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
            'install': lambda: self.install(),
            'uninstall': lambda: self.uninstall()
        }[self._action]()

        # preparing response
        result['changed'] = changed
        self.module.exit_json(**result)

    @property
    def params(self):
        return self.module.params

    def install(self) -> bool:
        if self.service_exists():
            self.module.debug("skupper-controller service already exists")
            return False

        exists, platform = self.get_container_info()
        if exists:
            self.module.debug("{} container already exists (platform: {})".format(self.container_name(), platform))
            return False

        if self._platform == "podman":
            enable_podman_socket(self.module)

        command = [
            self._platform, "run", "-d", "--pull", "always", "--name",
            self.container_name(), "--label=application=skupper-v2",
            "--network", "host", "--security-opt", "label=disable", "-u",
            runas(self._platform), "--userns=%s" % (userns(self._platform))
        ]
        requires_mounts_for = list()
        for source, dest in base_mounts(self._platform, self._platform).items():
            requires_mounts_for.append(source)
            command.extend(["-v", "%s:%s:z" % (source, dest)])
        env_dict = env(self._platform, self._platform)
        for var, val in env_dict.items():
            command.extend(["-e", "%s=%s" % (var, val)])
        command.append(self._image)

        if not os.path.exists(data_home()):
            os.makedirs(data_home())

        code, out, err = run_command(self.module, command)
        if code != 0:
            msg = "error creating container '%s': %s" % (
                self.container_name(), out or err)
            self.module.fail_json(msg)

        try:
            self.create_startup_scripts(self._platform)
        except Exception as ex:
            self.module.fail_json("unable to create startup scripts: {}".format(ex))
        try:
            self.create_service(mounts=requires_mounts_for, envs=env_dict)
        except Exception as ex:
            self.module.fail_json("unable to create systemd service: {}".format(ex))

        return True

    def uninstall(self) -> bool:
        changed = False

        if self.service_exists():
            if systemd_delete(self.module, self.service_name()):
                changed = True

        exists, platform = self.get_container_info()
        if exists and platform:
            command = [platform, "rm", "--force", self.container_name()]
            code, out, err = run_command(self.module, command)
            if code != 0:
                self.module.fail_json("error removing {} container: {}".format(self.container_name(), (err or out)))
            changed = True

        base_path = "{}/system-controller".format(data_home())
        if os.path.exists(base_path):
            try:
                shutil.rmtree(base_path)
                changed = True
            except Exception as ex:
                self.module.warn("unable to remove {}: {}".format(base_path, ex))

        return changed

    def service_name(self) -> str:
        return "skupper-controller.service"

    def service_exists(self) -> bool:
        return service_exists(self.module, self.service_name())

    def create_startup_scripts(self, engine: str):
        base_path = "{}/system-controller/internal/scripts/".format(data_home())
        if not os.path.exists(base_path):
            os.makedirs(base_path)

        def write_header(file):
            file.write("#!/usr/bin/env sh\n")
            file.write("\n")
            file.write("set -o errexit\n")
            file.write("set -o nounset\n")

        start_file = "{}/start.sh".format(base_path)
        stop_file = "{}/stop.sh".format(base_path)
        with open(start_file, "w", encoding="utf-8") as out_file:
            write_header(out_file)
            out_file.write("{} start {}\n".format(engine, self.container_name()))
        with open(stop_file, "w", encoding="utf-8") as out_file:
            write_header(out_file)
            out_file.write("{} stop -t 10 {}\n".format(engine, self.container_name()))

    def create_service(self, mounts: list, envs: dict):
        startup_scripts_path = "{}/system-controller/internal/scripts".format(data_home())
        service_file = "{}/{}".format(service_dir(), self.service_name())
        if not os.path.exists(service_dir()):
            os.makedirs(service_dir())
        with open(service_file, "w", encoding="utf-8") as out_file:
            out_file.write("[Unit]\n")
            out_file.write("Description=skupper-controller\n")
            out_file.write("After=network-online.target\n")
            out_file.write("Wants=network-online.target\n")
            for mount in mounts:
                out_file.write("RequiresMountsFor={}\n".format(mount))
            out_file.write("\n")
            out_file.write("[Service]\n")
            out_file.write("TimeoutStopSec=70\n")
            out_file.write("RemainAfterExit=yes\n")
            for var, val in envs.items():
                out_file.write("Environment={}={}\n".format(var, val))
            out_file.write("ExecStart=/bin/bash {}/start.sh\n".format(startup_scripts_path))
            out_file.write("ExecStop=/bin/bash {}/stop.sh\n".format(startup_scripts_path))
            out_file.write("Type=simple\n")
            out_file.write("\n")
            out_file.write("[Install]\n")
            out_file.write("WantedBy=default.target\n")
        return systemd_create(self.module, self.service_name(), service_file)

    def container_name(self) -> str:
        # user-skupper-controller
        container_name = "{}-skupper-controller".format(pwd.getpwuid(os.getuid())[0])
        return container_name

    def get_container_info(self) -> tuple[bool, str]:
        return container_info(self.module, self.container_name())


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
