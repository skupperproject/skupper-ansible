from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


from .command import run_command
try:
    from ansible.module_utils.basic import AnsibleModule
except ImportError:
    pass


def has_docker(module: AnsibleModule) -> bool:
    command = ["docker", "version"]
    code, out, err = run_command(module, command)
    return code == 0


def has_podman(module: AnsibleModule) -> bool:
    command = ["podman", "version"]
    code, out, err = run_command(module, command)
    return code == 0


def container_exists(module: AnsibleModule, name: str) -> bool:
    container_engines = []
    if has_podman(module):
        container_engines.append("podman")
    if has_docker(module):
        container_engines.append("docker")
    for engine in container_engines:
        command = [engine, "inspect", name]
        code, out, err = run_command(module, command)
        if code == 0:
            return True
    return False
