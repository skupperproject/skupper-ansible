#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright Skupper Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)

DOCUMENTATION = r'''
---
module: links_load
short_description: Loads existing links to other sites
description:
    Loads existing Skupper links to other sites, using the same format expected for links,
    referring other ansible hosts. The mapping of existing links to ansible hosts defined
    in the inventory file, depends on previous execution of site_load module, which loads
    site ids for each site defined in the inventory. Without it, links will be considered
    as unmapped and might be removed if links module is invoked.

requirements:
    - kubectl if using kubernetes platform
    - podman v4+ if using podman as the site platform
author: "Fernando Giorgetti (@fgiorgetti)"
extends_documentation_fragment:
    - skupper.network.common
version_added: "1.1.0"
options:
    sites:
        description:
            - List of sites used to correlate existing links to Ansible's inventory_hostname entries
            - This module expects that site_load module has been invoked previously
        type: list
        required: false
        elements: dict
        suboptions:
            host:
                description:
                    - The Ansible's inventory_hostname value that represent a given site entry (provided by site_load module)
                required: true
                type: str
            id:
                description:
                    - The Skupper site id (provided by site_load module)
                required: true
                type: str
            name:
                description:
                    - The Skupper site name (provided by site_load module)
                required: true
                type: str
'''

EXAMPLES = r'''
- name: Loading existing links
  skupper.network.links_load:
'''

RETURN = r'''
existing_links:
  description: List of existing links mapped to the corresponding ansible inventory hostname
  returned: always
  type: dict
  sample:
    existing_links:
      - host: host-a
        name: site-a
        cost: 1
      - host: host-b
        name: site-b
        cost: 1
'''

import json
import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_native
from ..module_utils.args import add_fact, common_args
from ..module_utils.types import Link

__metaclass__ = type


class LinksLoader:
    def __init__(self, module: AnsibleModule):
        self._module = module
        self.platform = module.params['platform']
        self.kubeconfig = module.params['kubeconfig']
        self.context = module.params['context']
        self.namespace = module.params['namespace']
        self.hostname = module.params['hostname']
        self.podman_endpoint = module.params['podman_endpoint']
        self.sites = dict()
        for site in module.params['sites']:
            self.sites[site['id']] = site

    def load(self) -> list[dict]:
        return self.load_podman() if self.platform == "podman" else self.load_kube()

    def load_podman(self) -> list[dict]:
        base_cmd = ['podman']
        if len(self.podman_endpoint) > 0:
            base_cmd.append("--url=%s" % self.podman_endpoint)
        vol_info = base_cmd + ['volume', 'inspect', '--all']
        # executing podman cli
        rc, stdout, stderr = self._module.run_command(vol_info)
        if rc != 0:
            raise RuntimeError("error inspecting volumes: %s" % stderr)
        vol_json = json.loads(stdout)

        links = list[dict]()
        for volume in vol_json:
            if 'skupper.io/type' not in volume['Labels'] or volume['Labels']['skupper.io/type'] not in \
                    ("connection-token", "token-claim"):
                continue
            # retrieving site-id and cost from token
            link = Link()
            metadata_json = volume['Labels']['internal.skupper.io/metadata']
            metadata = json.loads(metadata_json)
            site_id = metadata['annotations']['skupper.io/generated-by']
            link.name = volume['Name']
            # if site id is mapped, set the host
            if site_id in self.sites:
                link.host = self.sites[site_id]['host']
            link.cost = int(metadata['annotations']['skupper.io/cost']) if 'skupper.io/cost' \
                                                                           in metadata['annotations'] else 1
            links.append(vars(link))
        return links

    def load_kube(self) -> list[dict]:
        kubectl = ['kubectl']
        if self.kubeconfig != "":
            kubectl.append("--kubeconfig=%s" % self.kubeconfig)
        if self.context != "":
            kubectl.append("--context=%s" % self.context)
        if self.namespace != "":
            kubectl.append("--namespace=%s" % self.namespace)

        # retrieving skupper tokens (secrets)
        kubectl_get_secret = kubectl + ["get", "secret",
                                        "--selector", "skupper.io/type in (token-claim, connection-token)",
                                        "--output", "json"]
        rc, stdout, stderr = self._module.run_command(kubectl_get_secret)
        if rc != 0:
            raise RuntimeError("error retrieving secrets - %s" % stderr)
        secret_list_json = json.loads(stdout)
        links = list[dict]()
        for item in secret_list_json['items']:
            site_id = item['metadata']['annotations']['skupper.io/generated-by']
            link = Link()
            # if site id is mapped, set the host
            if site_id in self.sites:
                link.host = self.sites[site_id]['host']
            link.name = item['metadata']['name']
            link.cost = int(item['metadata']['annotations']['skupper.io/cost']) \
                if 'skupper.io/cost' in item['metadata']['annotations'] else 1
            links.append(vars(link))
        return links


argument_spec = dict(
    common_args(),
    sites=dict(type='list', required=False, elements='dict', options=dict(
        host=dict(type='str', required=True),
        name=dict(type='str', required=True),
        id=dict(type='str', required=True)
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
    loader = LinksLoader(module)
    # loading links
    try:
        links = loader.load()
        add_fact(result, {"existing_links": links})
    except Exception as ex:
        module.fail_json(msg=to_native(ex), exception=traceback.format_exc())
    module.exit_json(**result)


if __name__ == '__main__':
    main()
