from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import typing as t
from ansible.module_utils.basic import AnsibleModule


def run_command(module: AnsibleModule, command: list) -> t.Tuple[int, str, str]:
    module.debug("running command: %s" % (command))
    code, out, err = module.run_command(command)
    module.debug("code: %d" % (code))
    module.debug("stdout: %s" % (out))
    module.debug("stderr: %s" % (err))
    return code, out, err
