# Copyright Skupper Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json
import unittest

from ansible.module_utils import basic
from unittest.mock import patch, mock_open

from ansible_collections.skupper.skupper.plugins.modules import site_load
from ansible_collections.skupper.skupper.tests.unit.plugins.modules.utils import exit_json, fail_json, \
    AnsibleExitJson, set_module_args


class TestSiteLoad(unittest.TestCase):

    def setUp(self):
        # Mocking AnsibleModule
        self.mock_module = patch.multiple(basic.AnsibleModule,
                                          exit_json=exit_json,
                                          fail_json=fail_json,
                                          run_command=self.run_command_mock)
        self.mock_module.start()
        self.addCleanup(self.mock_module.stop)

        # mocking builtins.open for skrouterd.json
        skrouterd_data = [
            [
                "router",
                {
                    "id": "my_podman_name",
                    "mode": "interior",
                    "helloMaxAgeSeconds": "3",
                    "metadata": "{\"id\":\"my_podman_id\",\"version\":\"manual\",\"platform\":\"podman\"}"
                },
            ],
        ]
        self.mock_open = patch('builtins.open', mock_open(read_data=json.dumps(skrouterd_data)))
        self.mock_open_state = self.mock_open.start()
        self.addCleanup(self.mock_open.stop)

    def run_command_mock(self, args, **kwargs):
        if args == ['kubectl', '--kubeconfig=/home/user/.kube/config', '--context=my-context',
                    '--namespace=my-namespace', 'wait', '--for=condition=ready', 'pod',
                    '--selector=skupper.io/component=service-controller', '--timeout=120s']:
            return 0, '{}', ''
        elif args == ['kubectl', '--kubeconfig=/home/user/.kube/config', '--context=my-context',
                      '--namespace=my-namespace', 'get', 'configmap', 'skupper-site', '--output=json']:
            resp = {
                "data": {
                    "name": "my_name",
                },
                "metadata": {
                    "uid": "my_id",
                }
            }
            return 0, json.dumps(resp), ''
        elif args == ['podman', '--url=/tmp/podman.socket', 'volume', 'inspect', 'skupper-internal']:
            resp = [
                {
                    "Mountpoint": "/my-volume/mountpoint",
                }
            ]
            return 0, json.dumps(resp), ''
        return 1, '', 'unexpected request - args = %s' % args

    def test_site_load_kube(self):
        set_module_args({
            "kubeconfig": "/home/user/.kube/config",
            "context": "my-context",
            "namespace": "my-namespace",
            "hostname": "my-hostname",
        })
        with self.assertRaises(AnsibleExitJson) as ex:
            site_load.main()

        result = ex.exception.args[0]
        self.assertEqual(True, result['changed'])
        self.assertIsNotNone(result['ansible_facts']['site'])

        site = result['ansible_facts']['site']
        self.assertEqual(site['host'], 'my-hostname')
        self.assertEqual(site['name'], 'my_name')
        self.assertEqual(site['id'], 'my_id')

    def test_site_load_podman(self):
        set_module_args({
            "hostname": "my-podman-hostname",
            "platform": "podman",
            "podman_endpoint": "/tmp/podman.socket",
        })
        with self.assertRaises(AnsibleExitJson) as ex:
            site_load.main()

        result = ex.exception.args[0]
        self.assertEqual(True, result['changed'])
        self.assertIsNotNone(result['ansible_facts']['site'])

        site = result['ansible_facts']['site']
        self.mock_open_state.assert_called_with('/my-volume/mountpoint/skrouterd.json')
        self.assertEqual(site['host'], 'my-podman-hostname')
        self.assertEqual(site['name'], 'my_podman_name')
        self.assertEqual(site['id'], 'my_podman_id')
