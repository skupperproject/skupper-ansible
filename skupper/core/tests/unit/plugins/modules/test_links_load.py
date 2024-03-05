# Copyright Skupper Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import unittest

from ansible.module_utils import basic
from unittest.mock import patch

from ansible_collections.skupper.core.plugins.modules import links_load
from ansible_collections.skupper.core.tests.unit.plugins.modules.utils import exit_json, fail_json, \
    AnsibleExitJson, set_module_args


class TestLinksLoad(unittest.TestCase):

    def setUp(self):
        # Mocking AnsibleModule
        self.mock_module = patch.multiple(basic.AnsibleModule,
                                          exit_json=exit_json,
                                          fail_json=fail_json,
                                          run_command=self.run_command_mock)
        self.mock_module.start()
        self.addCleanup(self.mock_module.stop)

    def run_command_mock(self, args, **kwargs):
        if args == ['kubectl', '--kubeconfig=/home/user/.kube/config', '--context=my-context',
                    '--namespace=my-namespace', 'get', 'secret',
                    '--selector', 'skupper.io/type in (token-claim, connection-token)', '--output', 'json']:
            return 0, kube_secrets, ''
        elif args == ['podman', '--url=/tmp/podman.socket', 'volume', 'inspect', '--all']:
            return 0, podman_secrets, ''
        return 1, '', 'unexpected request - args = %s' % args

    def test_links_load_kube(self):
        set_module_args({
            "kubeconfig": "/home/user/.kube/config",
            "context": "my-context",
            "namespace": "my-namespace",
            "hostname": "my-hostname-1",
            "sites": sites,
        })
        with self.assertRaises(AnsibleExitJson) as ex:
            links_load.main()

        result = ex.exception.args[0]
        self.assert_links(result)

    def test_site_load_podman(self):
        set_module_args({
            "platform": "podman",
            "podman_endpoint": "/tmp/podman.socket",
            "hostname": "my-hostname-1",
            "sites": sites,
        })
        with self.assertRaises(AnsibleExitJson) as ex:
            links_load.main()

        result = ex.exception.args[0]
        self.assert_links(result)

    def assert_links(self, result):
        self.assertEqual(True, result['changed'])
        self.assertIsNotNone(result['ansible_facts']['existing_links'])

        links = result['ansible_facts']['existing_links']
        self.assertEqual(2, len(links))
        idx = 1
        for link in links:
            linkid = idx
            idx += 1
            self.assertIn({'host': 'hostname-%d' % idx, 'name': 'link%d' % linkid, 'cost': idx, 'token': ''}, links)


sites = [{
    "host": "hostname-1",
    "name": "my-name-1",
    "id": "my-id-1",
}, {
    "host": "hostname-2",
    "name": "my-name-2",
    "id": "my-id-2",
}, {
    "host": "hostname-3",
    "name": "my-name-3",
    "id": "my-id-3",
}]

kube_secrets = """{
    "apiVersion": "v1",
    "items": [
        {
            "apiVersion": "v1",
            "data": {
                "ca.crt": "data",
                "tls.crt": "data",
                "tls.key": "data"
            },
            "kind": "Secret",
            "metadata": {
                "annotations": {
                    "edge-host": "10.0.0.1",
                    "edge-port": "45671",
                    "inter-router-host": "10.0.0.1",
                    "inter-router-port": "55671",
                    "skupper.io/cost": "2",
                    "skupper.io/generated-by": "my-id-2",
                    "skupper.io/site-version": "1.4.2"
                },
                "creationTimestamp": "2023-07-21T12:30:43Z",
                "labels": {
                    "skupper.io/type": "connection-token"
                },
                "name": "link1",
                "namespace": "my-namespace",
                "ownerReferences": [
                    {
                        "apiVersion": "apps/v1",
                        "kind": "Deployment",
                        "name": "skupper-router",
                        "uid": "7cc3f896-f1e2-4cff-9d3e-607bb10da8ad"
                    }
                ],
                "resourceVersion": "139324",
                "uid": "9021ce4c-8839-41c0-95f3-5a588cb0766d"
            },
            "type": "kubernetes.io/tls"
        },
        {
            "apiVersion": "v1",
            "data": {
                "ca.crt": "data",
                "tls.crt": "data",
                "tls.key": "data"
            },
            "kind": "Secret",
            "metadata": {
                "annotations": {
                    "edge-host": "10.0.0.2",
                    "edge-port": "45671",
                    "inter-router-host": "10.0.0.2",
                    "inter-router-port": "55671",
                    "skupper.io/cost": "3",
                    "skupper.io/generated-by": "my-id-3",
                    "skupper.io/site-version": "manual",
                    "skupper.io/url": "https://10.0.0.2:8081/"
                },
                "creationTimestamp": "2023-07-21T12:30:43Z",
                "labels": {
                    "skupper.io/type": "connection-token"
                },
                "name": "link2",
                "namespace": "my-namespace",
                "ownerReferences": [
                    {
                        "apiVersion": "apps/v1",
                        "kind": "Deployment",
                        "name": "skupper-router",
                        "uid": "7cc3f896-f1e2-4cff-9d3e-607bb10da8ad"
                    }
                ],
                "resourceVersion": "139329",
                "uid": "12167ad4-397a-4888-b040-6a37acabaf32"
            },
            "type": "Opaque"
        }
    ],
    "kind": "List",
    "metadata": {
        "resourceVersion": ""
    }
}
"""

podman_secrets = """[
     {
          "Name": "link1",
          "Driver": "local",
          "Mountpoint": "/home/fgiorget/.local/share/containers/storage/volumes/link1/_data",
          "CreatedAt": "2023-07-21T09:30:43.92102414-03:00",
          "Labels": {
               "application": "skupper",
               "internal.skupper.io/metadata": "{\\"name\\":\\"link1\\",\\"creationTimestamp\\":null,\\"labels\\":\
               {\\"skupper.io/type\\":\\"connection-token\\"},\\"annotations\\":{\\"edge-host\\":\\"10.105.3.187\\",\
               \\"edge-port\\":\\"45671\\",\\"inter-router-host\\":\\"10.105.3.187\\",\
               \\"inter-router-port\\":\\"55671\\",\\"skupper.io/generated-by\\":\\"my-id-2\\",\
               \\"skupper.io/cost\\":\\"2\\",\
               \\"skupper.io/url\\":\\"https://10.110.231.48:8081/681edc45-27c2-11ee-aad3-047bcb64f0f2\\"}}",
               "skupper.io/type": "connection-token"
          },
          "Scope": "local",
          "Options": {},
          "MountCount": 0,
          "NeedsCopyUp": true,
          "NeedsChown": true
     },
     {
          "Name": "link2",
          "Driver": "local",
          "Mountpoint": "/home/fgiorget/.local/share/containers/storage/volumes/link2/_data",
          "CreatedAt": "2023-07-21T09:30:44.410553295-03:00",
          "Labels": {
               "application": "skupper",
               "internal.skupper.io/metadata": "{\\"name\\":\\"link2\\",\\"creationTimestamp\\":null,\\"labels\\":\
               {\\"skupper.io/type\\":\\"connection-token\\"},\\"annotations\\":{\\"edge-host\\":\\"10.100.97.179\\",\
               \\"edge-port\\":\\"45671\\",\\"inter-router-host\\":\\"10.100.97.179\\",\
               \\"inter-router-port\\":\\"55671\\",\\"skupper.io/generated-by\\":\\"my-id-3\\",\
               \\"skupper.io/cost\\":\\"3\\",\\"skupper.io/site-version\\":\\"manual\\"}}",
               "skupper.io/type": "connection-token"
          },
          "Scope": "local",
          "Options": {},
          "MountCount": 0,
          "NeedsCopyUp": true,
          "NeedsChown": true
     }
]
"""
