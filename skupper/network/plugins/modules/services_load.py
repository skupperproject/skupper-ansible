#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright Skupper Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)

DOCUMENTATION = r'''
---
module: services_load
short_description: Loads existing services and targets
description:
    Loads existing Skupper services and targets. Existing services will be returned under the `existing_services` fact.
requirements:
    - python >= 3.9
    - kubectl if using kubernetes platform
    - podman v4+ if using podman as the site platform
author: "Fernando Giorgetti (@fgiorgetti)"
extends_documentation_fragment:
    - skupper.network.common
version_added: "1.2.0"
options: {}
'''

EXAMPLES = r'''
- name: Loading existing services
  skupper.network.services_load:
'''

RETURN = r'''
existing_services:
  description: List of existing services and targets
  returned: always
  type: dict
  sample:
    existing_services:
      nearestprime:
        ports:
          - 8000
        targets:
          - type: deployment
            name: nearestprime
      db:
        ports:
          - 5432
'''

import json
import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_native
from ..module_utils.args import add_fact, common_args
from ..module_utils.types import Service, ServiceTarget

__metaclass__ = type


class ServicesLoader:
    def __init__(self, module: AnsibleModule):
        self._module = module
        self.platform = module.params['platform']
        self.kubeconfig = module.params['kubeconfig']
        self.context = module.params['context']
        self.namespace = module.params['namespace']
        self.hostname = module.params['hostname']
        self.podman_endpoint = module.params['podman_endpoint']
        self.sites = dict()
        self.resource_types = ["deployment", "statefulset"]
        self.resources = dict()
        self.podman_containers = dict()

    def load(self) -> dict:
        return self.load_podman() if self.platform == "podman" else self.load_kube()

    def load_podman(self) -> dict:
        # loading podman containers info
        rc, stdout, stderr = self._module.run_command(self._podman() +
                                                      "container ls -f label=skupper.io/address --format json"
                                                      .split())
        json_data = json.loads(stdout)
        for container in json_data:
            name = container['Names'][0]
            address = container['Labels']['skupper.io/address']
            host_ip = None
            host_ports = list[str]()
            if 'Ports' in container and container['Ports'] is not None:
                for port in container['Ports']:
                    if 'host_ip' in port:
                        host_ip = port['host_ip']
                    svc_port = port['container_port'] if 'container_port' in port else None
                    ctr_port = port['host_port'] if 'host_port' in port else None
                    if svc_port is not None:
                        host_ports.append("%s:%s" % (svc_port, ctr_port if ctr_port is not None else svc_port))
            info = dict()
            info['containerName'] = name if name != address else None
            info['hostIp'] = host_ip
            info['hostPorts'] = host_ports if len(host_ports) > 0 else None
            self.podman_containers[address] = info

        vol_info = self._podman() + ['volume', 'inspect', 'skupper-services']
        # executing podman cli
        rc, stdout, stderr = self._module.run_command(vol_info)
        if rc != 0:
            raise RuntimeError("error inspecting volume %s: %s" % ("skupper-services", stderr))
        vol_json = json.loads(stdout)
        try:
            services_file = open("%s/skupper-services.json" % (vol_json[0]['Mountpoint']))
            services_json = json.load(services_file)
            services = self.load_services(services_json)
        except Exception:
            # if no services
            return dict()

        return services

    def load_kube(self) -> dict:
        resources = dict()

        # detect if deploymentconfigs are available
        kubectl_get_dc = self._kubectl() + ["api-resources", "--api-group", "apps.openshift.io", "-o", "name"]
        rc, stdout, stderr = self._module.run_command(kubectl_get_dc)
        if rc == 0 and str(stdout).__contains__("deploymentconfig"):
            self.resource_types.append("deploymentconfig")

        # loading existing resources
        for resource_type in self.resource_types:
            self.resources[resource_type] = list()
            # load all resources
            rc, stdout, stderr = self._module.run_command(self._kubectl() + ["get", resource_type, "-o", "json"])
            if rc != 0:
                raise RuntimeError("unable to load existing %s - %s" % (resource_type, stderr))
            res_json = json.loads(stdout)
            for res in res_json['items']:
                self.resources[resource_type].append(res['metadata']['name'])

        # retrieving skupper services
        kubectl_get_secret = self._kubectl() + ["get", "configmap", "skupper-services", "--output", "json"]
        rc, stdout, stderr = self._module.run_command(kubectl_get_secret)
        if rc != 0:
            raise RuntimeError("error retrieving service list - %s" % stderr)
        services_cm_json = json.loads(stdout)
        if 'data' not in services_cm_json or len(services_cm_json['data']) == 0:
            return dict()
        services_dict_json = services_cm_json['data']
        # load service definition as json dict
        for service in services_dict_json:
            info = json.loads(services_dict_json[service])
            services_dict_json[service] = info
        services = self.load_services(services_dict_json)
        return services

    def _kubectl(self):
        kubectl = ['kubectl']
        if self.kubeconfig != "":
            kubectl.append("--kubeconfig=%s" % self.kubeconfig)
        if self.context != "":
            kubectl.append("--context=%s" % self.context)
        if self.namespace != "":
            kubectl.append("--namespace=%s" % self.namespace)
        return kubectl

    def _podman(self):
        base_cmd = ['podman']
        if len(self.podman_endpoint) > 0:
            base_cmd.append("--url=%s" % self.podman_endpoint)
        return base_cmd

    def load_services(self, services_json: dict) -> dict:
        services = dict()
        for name in services_json:
            info = services_json[name]
            service = Service()
            service_targets = list()
            service.ports = info['ports']
            service.protocol = info['protocol']
            service.labels = ["%s=%s" % (k, v) for k, v in info['labels'].items()] if 'labels' in info else None
            service.aggregate = info['aggregate'] if 'aggregate' in info else None
            service.generateTlsSecrets = info['tlsCredentials'] if 'tlsCredentials' in info else None
            service.eventChannel = info['eventchannel'] if 'eventchannel' in info else None

            # retrieving podman specific settings
            if self.platform == "podman" and name in self.podman_containers:
                container_info = self.podman_containers[name]
                service.containerName = container_info['containerName']
                service.hostIp = container_info['hostIp']
                service.hostPorts = container_info['hostPorts']

            # processing (optional) targets
            if 'targets' in info and info['targets'] is not None:
                for target in info['targets']:
                    service_target = ServiceTarget()
                    if 'targetPorts' in target:
                        target_ports = list()
                        for target_port in target['targetPorts']:
                            target_ports.append("%s:%d" % (target_port, target['targetPorts'][target_port]))
                        service_target.ports = target_ports
                    if 'service' in target and len(target['service']) > 0:
                        if self.platform == "podman":
                            service_target.type = "host"
                        else:
                            service_target.type = "service"
                        service_target.name = target['service']
                    elif self.platform == "kubernetes":
                        service_target.type = self.get_resource_type(target['name'])
                        service_target.name = target['name']
                    service_targets.append({k: v for k, v in vars(service_target).items() if v})

            if len(service_targets) > 0:
                service.targets = service_targets

            services[name] = {k: v for k, v in vars(service).items() if v}

        return services

    def get_resource_type(self, name):
        for resource_type in self.resource_types:
            if name in self.resources[resource_type]:
                return resource_type
        raise RuntimeError("unable to determine resource type for: %s" % name)


argument_spec = dict(
    common_args(),
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
    loader = ServicesLoader(module)
    # loading services
    try:
        services = loader.load()
        add_fact(result, {"existing_services": services})
    except Exception as ex:
        module.fail_json(msg=to_native(ex), exception=traceback.format_exc())
    module.exit_json(**result)


if __name__ == '__main__':
    main()
