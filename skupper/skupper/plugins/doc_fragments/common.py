# -*- coding: utf-8 -*-

# Copyright Skupper Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

class ModuleDocFragment(object):
    # Standard documentation
    DOCUMENTATION = r'''
    options:
        platform:
            description:
                - Platform to be used (kubernetes or podman)
            type: str
            required: false
        kubeconfig:
            description:
                - KUBECONFIG file to be used (defaults to ${HOME}/.kube/config)
            type: str
            required: false
        context:
            description:
                - KUBECONFIG context to use
            type: str
            required: false
        namespace:
            description:
                - Kubernetes namespace to run the Skupper site
            type: str
            required: false
        podman_endpoint:
            description:
                - Podman endpoint to use when managing a Skupper site
            type: str
            required: false
        hostname:
            description:
                - Ansible's inventory_hostname used to represent the given Skupper site
                - This is automatically provided by the action plugin
            type: str
            required: false
    '''
