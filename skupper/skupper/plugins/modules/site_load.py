#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright Skupper Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)

DOCUMENTATION = r'''
---
module: site_load
short_description: Loads site information as ansible facts into the respective host
description:
    Loads Skupper site information as a hostvar named 'site'. It contains the site name,
    site id and inventory hostname related to it. This 'site' info can be used by
    modules to map runtime information of a skupper site to an ansible host defined through
    the inventory file.

    Kubernetes options can be set through host variables (kubeconfig, context, namespace).
    Podman endpoint can be customized through init.podmanEndpoint host variable.
requirements:
    - python >= 3.9
    - kubectl if using kubernetes platform
    - podman v4+ if using podman as the site platform
version_added: "1.1.0"
author: "Fernando Giorgetti (@fgiorgetti)"
extends_documentation_fragment:
    - skupper.skupper.common
options: {}
'''

EXAMPLES = r'''
- name: Loading site information
  skupper.skupper.site_load:
'''

RETURN = r'''
site:
  description: Skupper site information
  returned: always
  type: dict
  sample:
    site:
      host: host-a
      name: site-a
      id: 53899d80-1ae6-11ee-be28-1e9341abe0db
'''

import json
import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_native
from ..module_utils.args import add_fact, common_args
from ..module_utils.types import Site

__metaclass__ = type


class SiteLoader:
    def __init__(self, module: AnsibleModule):
        self.platform = module.params['platform']
        self.kubeconfig = module.params['kubeconfig']
        self.context = module.params['context']
        self.namespace = module.params['namespace']
        self.hostname = module.params['hostname']
        self.podman_endpoint = module.params['podman_endpoint']
        self._module = module

    def load(self) -> Site:
        return self.load_podman() if self.platform == "podman" else self.load_kube()

    def load_podman(self) -> Site:
        base_cmd = ['podman']
        if len(self.podman_endpoint) > 0:
            base_cmd.append("--url=%s" % self.podman_endpoint)
        vol_info = base_cmd + ['volume', 'inspect', 'skupper-internal']
        # executing podman cli
        rc, stdout, stderr = self._module.run_command(vol_info)
        if rc != 0:
            raise RuntimeError("error inspecting volume: skupper-internal: %s" % stderr)
        vol_json = json.loads(stdout)
        path = vol_json[0]['Mountpoint']
        file = open("%s/%s" % (path, "skrouterd.json"))
        data = file.read()
        config = json.loads(data)
        router = config[0][1]
        metadata = json.loads(router['metadata'])
        site = Site()
        site.host = self.hostname
        site.name = router['id']
        site.id = metadata['id']
        return site

    def load_kube(self) -> Site:
        kubectl = ['kubectl']
        if self.kubeconfig != "":
            kubectl.append("--kubeconfig=%s" % self.kubeconfig)
        if self.context != "":
            kubectl.append("--context=%s" % self.context)
        if self.namespace != "":
            kubectl.append("--namespace=%s" % self.namespace)

        # wait for service-controller pod to be running
        kubectl_wait = kubectl + [
            "wait", "--for=condition=ready", "pod", "--selector=skupper.io/component=service-controller",
            "--timeout=120s"]
        rc, stdout, stderr = self._module.run_command(kubectl_wait)
        if rc != 0:
            raise RuntimeError("timed out waiting on service-controller to be ready - %s" % stderr)

        # retrieving skupper-site configmap
        kubectl_get_cm = kubectl + ["get", "configmap", "skupper-site", "--output=json"]
        rc, stdout, stderr = self._module.run_command(kubectl_get_cm)
        if rc != 0:
            raise RuntimeError("error retrieving skupper-site configmap - %s" % stderr)
        cm_json = json.loads(stdout)
        site = Site()
        site.host = self.hostname
        site.name = cm_json['data']['name']
        site.id = cm_json['metadata']['uid']
        return site


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
    loader = SiteLoader(module)

    # loading site info
    try:
        site = loader.load()
        add_fact(result, {"site": vars(site)})
    except Exception as ex:
        module.fail_json(msg=to_native(ex), exception=traceback.format_exc())

    module.exit_json(**result)


if __name__ == '__main__':
    main()
