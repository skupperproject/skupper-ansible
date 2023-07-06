#!/usr/bin/python
import tempfile
import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_native

from ..module_utils.args import *
from ..module_utils.skupper_cli import prepare_command
from ..module_utils.types import Result

__metaclass__ = type

DOCUMENTATION = r'''
---
module: links
short_description: Update links based on provided links list 
description:
    - Updates the links defined by the respective site, based on the links list defined through the host variables.
    - Existing links that cannot be mapped to an inventory host will be deleted.
    - Links with a corresponding token (provided by skupper_token role) or manually through the token property will be created.
    - If a corresponding token cannot be found for a requested link, it will fail.
requirements:
    - kubectl if using kubernetes platform
    - podman v4+ if using podman as the site platform 
version_added: "1.1.0"
options: {}
'''

EXAMPLES = r'''
- name: Updating links
  skupper.network.links:
'''

RETURN = r''' # '''


class Links:
    def __init__(self, module: AnsibleModule):
        self._module = module
        self.platform = module.params['platform']
        self.kubeconfig = module.params['kubeconfig']
        self.context = module.params['context']
        self.namespace = module.params['namespace']
        self.hostname = module.params['hostname']
        self.podman_endpoint = module.params['podman_endpoint']
        self.create = module.params['create']
        self.delete = module.params['delete']
        self.command = prepare_command(module.params)

    def delete_links(self):
        res = Result()
        command = self.command.copy()
        command.append("link")
        command.append("delete")
        for link in self.delete:
            rc, stdout, stderr = self._module.run_command(command + [link['name']])
            if rc != 0:
                res.msgs.append("error deleting link %s - %s" % (link['name'], stderr))
                res.failed = True
            else:
                res.msgs.append("link has been deleted: %s" % link['name'])
                res.changed = True
        return res

    def create_links(self):
        res = Result()
        command = self.command.copy()
        command.append("link")
        command.append("create")
        for link in self.create:
            if link['token'] in (None, ""):
                res.failed = True
                res.warnings.append("No token defined for %s" % link['host'])
                continue

            # creating temporary file to store token definition
            tf = tempfile.NamedTemporaryFile()
            tf.write(bytes(link['token'], encoding='utf-8'))
            tf.flush()

            # defining link options
            create_command = command.copy()
            if 'name' in link and link['name'] not in (None, ""):
                create_command.append("--name")
                create_command.append(link['name'])
            if 'cost' in link and link['cost'] is not None and int(link['cost']) > 1:
                create_command.append("--cost")
                create_command.append(str(link['cost']))

            # running
            create_command.append(tf.name)
            rc, stdout, stderr = self._module.run_command(create_command)
            tf.close()

            # validating results
            if rc != 0:
                res.msgs.append("error creating link to %s - %s" % (link['host'], stderr))
                res.failed = True
            else:
                res.msgs.append("link created - host: %s" % link['host'])
                res.changed = True
        return res


def run_module():
    module_args = dict(
        common_args(),
        create=dict(type='list', required=False, elements='dict', options=dict(
            host=dict(type='str', required=True),
            name=dict(type='str', required=False),
            cost=dict(type='int', required=False),
            token=dict(type='str', required=False),
        )),
        delete=dict(type='list', required=False, elements='dict', options=dict(
            host=dict(type='str', required=False),
            name=dict(type='str', required=True),
            cost=dict(type='int', required=False),
            token=dict(type='str', required=False),
        )),
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    result = dict(changed=False)
    # loading params
    links = Links(module)
    # loading links
    try:
        res = links.delete_links()
        res.merge(links.create_links())
        result |= res.result()
    except Exception as ex:
        module.fail_json(msg=to_native(ex), exception=traceback.format_exc())
    module.exit_json(**result)


if __name__ == '__main__':
    run_module()
