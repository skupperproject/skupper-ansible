#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright Skupper Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)

DOCUMENTATION = r'''
---
module: services
short_description: Update services based on provided services list
description:
    - Updates the services defined by the respective site, based on the services list defined through the host variables
    - The services plugin will generate a list of services (or targets) to be created and deleted
    - If targets have changed then the create and delete lists will have just the name and respective targets (no spec)
extends_documentation_fragment:
    - skupper.core.common
requirements:
    - python >= 3.9
    - kubectl if using kubernetes platform
    - podman v4+ if using podman as the site platform
author: "Fernando Giorgetti (@fgiorgetti)"
version_added: "1.2.0"
options:
    create:
        description:
            - List of service definitions to be created
            - This list will be populated automatically by the action plugin based on the I(services) definition
            - For more information on how to define services, read the I(skupper_service) role documentation
        required: false
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - Service name
                required: true
                type: str
            spec:
                description:
                    - Service specification provided by the action plugin based on the I(services) definition
                required: true
                type: dict
                suboptions:
                    name:
                        description:
                            - Service name
                        required: false
                        type: str
                    ports:
                        description:
                            - List of ports
                        required: true
                        type: list
                        elements: int
                    protocol:
                        description:
                            - Protocol to use
                        type: str
                        choices: ["tcp", "http", "http2"]
                        default: "tcp"
                    aggregate:
                        description:
                            - Strategy to aggregate http responses
                        required: false
                        type: str
                        choices: ["json", "multipart"]
                    generate_tls_secrets:
                        description:
                            - If enabled, service communication will be encrypted using TLS
                        required: false
                        type: bool
                    event_channel:
                        description:
                            - If specified this service will be a channel for multicast events
                        required: false
                        type: bool
                    container_name:
                        description:
                            - Alternative container name to be used for proxy container
                            - This option is only relevant on podman sites
                        required: false
                        type: str
                    host_ip:
                        description:
                            - Host IP to be bound to the proxy container port(s)
                            - This option is only relevant on podman sites
                        required: false
                        type: str
                    host_ports:
                        description:
                            - List of ports to be mapped to the container port
                            - "Format for each entry is: <service-port>:<host-port>"
                            - This option is only relevant on podman sites
                        required: false
                        type: list
                        elements: str
            targets:
                description:
                    - List of targets that the respective service definition will be bound to
                required: false
                type: list
                elements: dict
                suboptions:
                    type:
                        description:
                            - Type of target to bind
                            - "Valid values for kubernetes: deployment, statefulset, service, deploymentconfig"
                            - "Valid values for podman: host"
                        required: true
                        type: str
                    name:
                        description:
                            - Name or identification of the chosen resource type
                        required: true
                        type: str
                    ports:
                        description:
                            - List of ports to be mapped to the from the service to the chosen target
                            - "Format for each entry is: <service-port>:<target-resource-port>"
                        required: false
                        type: list
                        elements: str
            labels:
                description:
                    - List of labels to be applied to the service
                    - "The format to use for each entry is: <key>=<value>"
                required: false
                type: list
                elements: str
    delete:
        description:
            - List of services, labels or targets to be removed
            - This list will be populated automatically by the action plugin based on the I(services) definition
            - It also requires that the M(skupper.core.services_load) module is invoked first
        required: false
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - Service name to be deleted
                required: true
                type: str
            targets:
                description:
                    - List of targets to unbind
                required: false
                type: list
                elements: dict
                suboptions:
                    type:
                        description:
                            - Type of target to bind
                            - "Valid values for kubernetes: deployment, statefulset, service, deploymentconfig"
                            - "Valid values for podman: host"
                        required: true
                        type: str
                    name:
                        description:
                            - Name or identification of the chosen resource type
                        required: true
                        type: str
            labels:
                description:
                    - List of labels to be removed from service
                    - "The format to use for each entry is: <key>-"
                required: false
                type: list
                elements: str
'''

EXAMPLES = r'''
- name: Updating services
  skupper.core.services:
'''

RETURN = r''' # '''

import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_native

from ..module_utils.args import common_args
from ..module_utils.skupper_cli import prepare_command
from ..module_utils.types import Result

__metaclass__ = type


class Services:
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

    def manage_labels(self, delete=False) -> Result:
        res = Result()
        param = self.delete if delete else self.create
        for service in [s for s in param if s['labels'] and len(s['labels']) > 0]:
            if self.platform == "podman":
                res.warnings.append("Labels are not yet supported on podman sites")
                return res
            command = self.command.copy()
            command.append('service')
            command.append('label')
            command.append(service['name'])
            for label in service['labels']:
                rc, stdout, stderr = self._module.run_command(command + [label])
                if rc != 0:
                    res.msgs.append("error %s label %s for service %s - %s" %
                                    ("deleting" if delete else "creating", label, service['name'], stderr))
                    res.failed = True
                else:
                    res.msgs.append("label %s for service %s has been %s" %
                                    (label, service['name'], "deleted" if delete else "created"))
                    res.changed = True
        return res

    def unbind_targets(self) -> Result:
        res = Result()
        for service in [s for s in self.delete if s['targets'] and len(s['targets']) > 0]:
            command = self.command.copy()
            command.append('service')
            command.append('unbind')
            command.append(service['name'])
            for target in service['targets']:
                target_type = target['type']
                target_name = target['name']
                rc, stdout, stderr = self._module.run_command(command + [target_type, target_name])
                if rc != 0:
                    res.msgs.append("error unbinding target %s/%s for service %s - %s" % (target_type, target_name,
                                                                                          service['name'], stderr))
                    res.failed = True
                else:
                    res.msgs.append("target %s/%s for service %s has been unbound" %
                                    (target_type, target_name, service['name']))
                    res.changed = True
        return res

    def delete_services(self) -> Result:
        res = Result()
        for service in [s for s in self.delete if not s['labels'] and not s['targets']]:
            command = self.command.copy()
            command.append('service')
            command.append('delete')
            command.append(service['name'])
            rc, stdout, stderr = self._module.run_command(command)
            if rc != 0:
                res.msgs.append("error deleting service %s - %s" % (service['name'], stderr))
                res.failed = True
            else:
                res.msgs.append("service %s has been deleted" % (service['name']))
                res.changed = True
        return res

    def bind_targets(self) -> Result:
        res = Result()
        for service in [s for s in self.create if s['targets'] and len(s['targets']) > 0]:
            command = self.command.copy()
            command.append('service')
            command.append('bind')
            command.append(service['name'])
            for target in service['targets']:
                target_type = target['type']
                target_name = target['name']
                bind_command = command + [target_type, target_name]
                for port in [port for port in target['ports'] if target['ports']]:
                    bind_command.append("--target-port")
                    bind_command.append(port)
                rc, stdout, stderr = self._module.run_command(bind_command)
                if rc != 0:
                    res.msgs.append("error binding target %s/%s for service %s - %s" % (target_type, target_name,
                                                                                        service['name'], stderr))
                    res.failed = True
                else:
                    res.msgs.append("target %s/%s for service %s has been bound" %
                                    (target_type, target_name, service['name']))
                    res.changed = True
        return res

    def create_services(self) -> Result:
        res = Result()
        for service in [s for s in self.create if s['spec']]:
            spec = service['spec']
            command = self.command.copy()
            command.append('service')
            command.append('create')
            command.append(service['name'])
            command += [str(port) for port in spec['ports']]
            if spec['protocol'] and spec['protocol'] != "":
                command += ["--protocol", spec['protocol']]
            if spec['aggregate'] and spec['aggregate'] != "":
                command += ["--aggregate", spec['aggregate']]
            if spec['generate_tls_secrets'] is not None:
                command += ["--generate-tls-secrets=%s" % spec['generate_tls_secrets']]
            if spec['event_channel'] is not None:
                command += ["--event-channel=%s" % spec['event_channel']]
            if self.platform == "podman":
                if spec['container_name'] and spec['container_name'] != "":
                    command += ["--container-name", spec['container_name']]
                if spec['host_ip'] and spec['host_ip'] != "":
                    command += ["--host-ip", spec['host_ip']]
                if spec['host_ports'] and len(spec['host_ports']) > 0:
                    for host_port in spec['host_ports']:
                        command += ["--host-port", host_port]
            rc, stdout, stderr = self._module.run_command(command)
            if rc != 0:
                res.msgs.append("error creating service %s - %s [command: %s]" % (service['name'], stderr, command))
                res.failed = True
            else:
                res.msgs.append("service %s has been created" % (service['name']))
                res.changed = True
        return res


argument_spec = dict(
    common_args(),
    create=dict(type='list', required=False, elements='dict', options=dict(
        name=dict(type='str', required=True),
        spec=dict(type='dict', required=True, options=dict(
            name=dict(type='str', required=False),
            ports=dict(type='list', required=True, elements='int'),
            protocol=dict(type='str', default="tcp", choices=["tcp", "http", "http2"]),
            aggregate=dict(type='str', required=False, choices=["json", "multipart"]),
            generate_tls_secrets=dict(type='bool', required=False),
            event_channel=dict(type='bool', required=False),
            container_name=dict(type='str', required=False),
            host_ip=dict(type='str', required=False),
            host_ports=dict(type='list', required=False, elements='str'),
        )),
        targets=dict(type='list', required=False, elements='dict', options=dict(
            type=dict(type='str', required=True),
            name=dict(type='str', required=True),
            ports=dict(type='list', required=False, elements='str'),
        )),
        labels=dict(type='list', required=False, elements='str'),
    )),
    delete=dict(type='list', required=False, elements='dict', options=dict(
        name=dict(type='str', required=True),
        targets=dict(type='list', required=False, elements='dict', options=dict(
            type=dict(type='str', required=True),
            name=dict(type='str', required=True),
        )),
        labels=dict(type='list', required=False, elements='str'),
    ))
)


def setup_module_object():
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )
    return module


def main():
    module = setup_module_object()
    result = dict(changed=False)
    # loading params
    services = Services(module)
    try:
        res = services.manage_labels(delete=True)
        res.merge(services.unbind_targets())
        res.merge(services.delete_services())
        res.merge(services.create_services())
        res.merge(services.bind_targets())
        res.merge(services.manage_labels())
        result.update(res.result())
    except Exception as ex:
        module.fail_json(msg=to_native(ex), exception=traceback.format_exc())
    module.exit_json(**result)


if __name__ == '__main__':
    main()
