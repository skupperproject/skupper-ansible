# Copyright Skupper Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import unittest

from ansible.module_utils import basic
from io import TextIOWrapper, BytesIO
from unittest.mock import patch

from ansible_collections.skupper.network.plugins.modules import services_load
from ansible_collections.skupper.network.tests.unit.plugins.modules.utils import exit_json, fail_json, \
    AnsibleExitJson, set_module_args


class TestServicesLoad(unittest.TestCase):

    def setUp(self):
        # Mocking AnsibleModule
        self.mock_module = patch.multiple(basic.AnsibleModule,
                                          exit_json=exit_json,
                                          fail_json=fail_json,
                                          run_command=self.run_command_mock)
        self.mock_module.start()
        self.addCleanup(self.mock_module.stop)

        self.mock_open_ctrl = patch('builtins.open', side_effect=self.open_side_effect)
        self.mock_open_ctrl.start()
        self.addCleanup(self.mock_open_ctrl.stop)

    def run_command_mock(self, args, **kwargs):
        if args == ['kubectl', '--kubeconfig=/home/user/.kube/config', '--context=my-context',
                    '--namespace=my-namespace', 'api-resources', '--api-group', 'apps.openshift.io', '-o', 'name']:
            return 0, 'deploymentconfigs.apps.openshift.io', ''

        elif args == ['kubectl', '--kubeconfig=/home/user/.kube/config', '--context=my-context',
                      '--namespace=my-namespace', 'get', 'deployment', '-o', 'json']:
            return 0, deployments_json, ''
        elif args == ['kubectl', '--kubeconfig=/home/user/.kube/config', '--context=my-context',
                      '--namespace=my-namespace', 'get', 'statefulset', '-o', 'json']:
            return 0, statefulsets_json, ''
        elif args == ['kubectl', '--kubeconfig=/home/user/.kube/config', '--context=my-context',
                      '--namespace=my-namespace', 'get', 'deploymentconfig', '-o', 'json']:
            return 0, deploymentconfigs_json, ''
        elif args == ['kubectl', '--kubeconfig=/home/user/.kube/config', '--context=my-context',
                      '--namespace=my-namespace', 'get', 'configmap', 'skupper-services', '--output', 'json']:
            return 0, skupper_services_kube, ''
        elif args == ['podman', '--url=/tmp/podman.socket', 'container', 'ls', '-f', 'label=skupper.io/address',
                      '--format', 'json']:
            return 0, container_ls_json, ''
        elif args == ['podman', '--url=/tmp/podman.socket', 'volume', 'inspect', 'skupper-services']:
            return 0, volume_inspect_json, ''
        return 1, '', 'unexpected request - args = %s' % args

    def open_side_effect(self, *args, **kwargs):
        mount_point = '/home/my_user/.local/share/containers/storage/volumes/skupper-services/_data'
        if args[0] == '%s/skupper-services.json' % mount_point:
            return TextIOWrapper(BytesIO(bytes(skupper_services_podman, 'utf-8')))
        return TextIOWrapper(BytesIO(bytes('algo inesperado', 'utf-8')))

    def test_services_load_kube(self):
        set_module_args({
            "kubeconfig": "/home/user/.kube/config",
            "context": "my-context",
            "namespace": "my-namespace",
            "hostname": "my-hostname-1",
            "platform": "kubernetes",
        })
        with self.assertRaises(AnsibleExitJson) as ex:
            services_load.main()

        result = ex.exception.args[0]
        self.assertEqual(True, result['changed'])
        self.assertIsNotNone(result['ansible_facts']['existing_services'])

        services = result['ansible_facts']['existing_services']
        self.assertEqual(4, len(services))
        for name, service in services.items():
            if name == "my-service-a":
                self.assertEqual([8080, 9090], service['ports'])
                self.assertEqual('http', service['protocol'])
                self.assertEqual(2, len(service['labels']))
                self.assertEqual(['label1=value1', 'label2=value2'], service['labels'])
                self.assertEqual(1, len(service['targets']))
                self.assertEqual('deployment', service['targets'][0]['type'])
                self.assertEqual('nginx', service['targets'][0]['name'])
                self.assertEqual(2, len(service['targets'][0]['ports']))
                self.assertEqual(['8080:8080', '9090:8080'], service['targets'][0]['ports'])
            elif name == "nginx-dc":
                self.assertEqual([8080], service['ports'])
                self.assertEqual('tcp', service['protocol'])
                self.assertEqual(1, len(service['targets']))
                self.assertEqual('deploymentconfig', service['targets'][0]['type'])
                self.assertEqual('nginx-dc', service['targets'][0]['name'])
                self.assertEqual(1, len(service['targets'][0]['ports']))
                self.assertEqual(['8080:8080'], service['targets'][0]['ports'])
            elif name == "nginx-skupper":
                self.assertEqual([8080], service['ports'])
                self.assertEqual('tcp', service['protocol'])
                self.assertEqual(1, len(service['targets']))
                self.assertEqual('service', service['targets'][0]['type'])
                self.assertEqual('nginx.my-namespace', service['targets'][0]['name'])
            elif name == "postgres":
                self.assertEqual([5432], service['ports'])
                self.assertEqual('tcp', service['protocol'])
                self.assertEqual(1, len(service['targets']))
                self.assertEqual('statefulset', service['targets'][0]['type'])
                self.assertEqual('postgres', service['targets'][0]['name'])

    def test_site_load_podman(self):
        set_module_args({
            "platform": "podman",
            "podman_endpoint": "/tmp/podman.socket",
            "hostname": "my-hostname-1",
        })
        with self.assertRaises(AnsibleExitJson) as ex:
            services_load.main()
        result = ex.exception.args[0]
        self.assertEqual(True, result['changed'])
        self.assertIsNotNone(result['ansible_facts']['existing_services'])

        services = result['ansible_facts']['existing_services']
        self.assertEqual(2, len(services))
        for name, service in services.items():
            if name == "my-service-a":
                self.assertEqual([8080, 9090], service['ports'])
                self.assertEqual('http', service['protocol'])
                self.assertEqual(1, len(service['targets']))
                self.assertEqual('host', service['targets'][0]['type'])
                self.assertEqual('10.0.0.1', service['targets'][0]['name'])
                self.assertEqual(2, len(service['targets'][0]['ports']))
                self.assertEqual(['8080:8080', '9090:8080'], service['targets'][0]['ports'])
            elif name == "postgres":
                self.assertEqual([5432], service['ports'])
                self.assertEqual('tcp', service['protocol'])
                self.assertEqual(2, len(service['targets']))
                self.assertEqual('host', service['targets'][0]['type'])
                self.assertEqual('10.0.0.2', service['targets'][0]['name'])
                self.assertEqual(['5432:5432'], service['targets'][0]['ports'])
                self.assertEqual('host', service['targets'][1]['type'])
                self.assertEqual('10.0.0.3', service['targets'][1]['name'])
                self.assertEqual(['5432:2345'], service['targets'][1]['ports'])


deployments_json = """{
  "apiVersion": "v1",
  "items": [
    {
      "apiVersion": "apps/v1",
      "kind": "Deployment",
      "metadata": {
        "labels": {
          "app": "nginx"
        },
        "name": "nginx",
        "namespace": "my-namespace"
      },
      "spec": {
        "selector": {
          "matchLabels": {
            "app": "nginx"
          }
        },
        "template": {
          "metadata": {
            "labels": {
              "app": "nginx"
            }
          },
          "spec": {
            "containers": [
              {
                "image": "nginxinc/nginx-unprivileged:stable-alpine",
                "imagePullPolicy": "IfNotPresent",
                "name": "nginx",
                "ports": [
                  {
                    "containerPort": 8080,
                    "name": "web",
                    "protocol": "TCP"
                  }
                ]
              }
            ],
            "restartPolicy": "Always"
          }
        }
      }
    }
  ],
  "kind": "List",
  "metadata": {
    "resourceVersion": ""
  }
}
"""

statefulsets_json = """{
  "apiVersion": "v1",
  "items": [
    {
      "apiVersion": "apps/v1",
      "kind": "StatefulSet",
      "metadata": {
        "generation": 1,
        "name": "postgres",
        "namespace": "my-namespace"
      },
      "spec": {
        "replicas": 3,
        "revisionHistoryLimit": 10,
        "selector": {
          "matchLabels": {
            "app": "postgres"
          }
        },
        "serviceName": "postgres",
        "template": {
          "metadata": {
            "creationTimestamp": null,
            "labels": {
              "app": "postgres"
            }
          },
          "spec": {
            "containers": [
              {
                "image": "registry.redhat.io/rhel9/postgresql-15",
                "imagePullPolicy": "Always",
                "name": "postgres",
                "ports": [
                  {
                    "containerPort": 5432,
                    "name": "postgres",
                    "protocol": "TCP"
                  }
                ]
              }
            ]
          }
        }
      }
    },
    {
      "apiVersion": "apps/v1",
      "kind": "StatefulSet",
      "metadata": {
        "annotations": {
          "internal.skupper.io/service": "postgres"
        },
        "labels": {
          "app.kubernetes.io/name": "skupper-router",
          "app.kubernetes.io/part-of": "skupper",
          "application": "skupper-router",
          "internal.skupper.io/type": "proxy",
          "skupper.io/component": "router"
        },
        "name": "postgres-proxy",
        "namespace": "my-namespace",
        "ownerReferences": [
          {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "name": "skupper-router",
            "uid": "e312c6e1-c6c8-4675-ba06-0bd0ad63003b"
          }
        ]
      },
      "spec": {
        "podManagementPolicy": "OrderedReady",
        "replicas": 3,
        "revisionHistoryLimit": 10,
        "selector": {
          "matchLabels": {
            "internal.skupper.io/service": "postgres"
          }
        },
        "serviceName": "postgres-proxy",
        "template": {
          "metadata": {
            "labels": {
              "internal.skupper.io/service": "postgres"
            }
          },
          "spec": {
            "containers": [
              {
                "image": "quay.io/skupper/skupper-router:2.4.2",
                "imagePullPolicy": "Always",
                "name": "proxy"
              }
            ],
            "restartPolicy": "Always",
            "serviceAccount": "skupper-router",
            "serviceAccountName": "skupper-router"
          }
        }
      }
    }
  ],
  "kind": "List",
  "metadata": {
    "resourceVersion": ""
  }
}
"""

deploymentconfigs_json = """{
  "apiVersion": "v1",
  "items": [
    {
      "apiVersion": "apps.openshift.io/v1",
      "kind": "DeploymentConfig",
      "metadata": {
        "name": "nginx-dc",
        "namespace": "my-namespace"
      },
      "spec": {
        "replicas": 1,
        "selector": {
          "deployment-config.name": "nginx-dc"
        },
        "template": {
          "metadata": {
            "labels": {
              "deployment-config.name": "nginx-dc"
            }
          },
          "spec": {
            "containers": [
              {
                "image": "nginxinc/nginx-unprivileged:stable-alpine",
                "imagePullPolicy": "IfNotPresent",
                "name": "nginx"
              }
            ],
            "restartPolicy": "Always"
          }
        }
      }
    }
  ],
  "kind": "List",
  "metadata": {
    "resourceVersion": ""
  }
}
"""

skupper_services_kube = """{
  "apiVersion": "v1",
  "data": {
    "my-service-a": "{\\"address\\":\\"my-service-a\\",\\"protocol\\":\\"http\\",\\"ports\\":[8080,9090],\
    \\"exposeIngress\\":\\"\\",\\"labels\\":{\\"label1\\":\\"value1\\",\\"label2\\":\\"value2\\"},\
    \\"targets\\":[{\\"name\\":\\"nginx\\",\\"selector\\":\\"app=nginx\\",\
    \\"targetPorts\\":{\\"8080\\":8080,\\"9090\\":8080},\\"namespace\\":\\"my-namespace\\"}]}",
    "nginx-dc": "{\\"address\\":\\"nginx-dc\\",\\"protocol\\":\\"tcp\\",\\"ports\\":[8080],\
    \\"exposeIngress\\":\\"\\",\\"targets\\":[{\\"name\\":\\"nginx-dc\\",\
    \\"selector\\":\\"deployment-config.name=nginx-dc\\",\\"targetPorts\\":{\\"8080\\":8080}}]}",
    "nginx-skupper": "{\\"address\\":\\"nginx-skupper\\",\\"protocol\\":\\"tcp\\",\\"ports\\":[8080],\
    \\"exposeIngress\\":\\"\\",\\"targets\\":[{\\"name\\":\\"nginx.my-namespace\\",\
    \\"service\\":\\"nginx.my-namespace\\",\\"namespace\\":\\"my-namespace\\"}]}",
    "postgres": "{\\"address\\":\\"postgres\\",\\"protocol\\":\\"tcp\\",\\"ports\\":[5432],\
    \\"exposeIngress\\":\\"\\",\\"headless\\":{\\"name\\":\\"postgres\\",\\"size\\":3},\
    \\"targets\\":[{\\"name\\":\\"postgres\\",\\"selector\\":\\"app=postgres\\",\\"namespace\\":\\"my-namespace\\"}]}"
  },
  "kind": "ConfigMap",
  "metadata": {
    "name": "skupper-services",
    "namespace": "my-namespace",
    "ownerReferences": [
      {
        "apiVersion": "v1",
        "kind": "ConfigMap",
        "name": "skupper-site",
        "uid": "ec72fd67-65c0-43c8-9244-c8da8a67b12a"
      }
    ]
  }
}
"""

container_ls_json = """[
  {
    "Labels": {
      "application": "skupper",
      "skupper.io/address": "my-service-a"
    },
    "Names": [
      "my-service-a"
    ],
    "Networks": [
      "skupper"
    ],
    "Ports": [
      {
        "host_ip": "192.168.124.1",
        "container_port": 8080,
        "host_port": 8888,
        "range": 1,
        "protocol": "tcp"
      },
      {
        "host_ip": "192.168.124.1",
        "container_port": 9090,
        "host_port": 9999,
        "range": 1,
        "protocol": "tcp"
      }
    ],
    "State": "running",
    "Status": "Up About a minute",
    "Created": 1690300422
  },
  {
    "Labels": {
      "application": "skupper",
      "skupper.io/address": "postgres"
    },
    "Names": [
      "postgres"
    ],
    "Networks": [
      "skupper"
    ],
    "Ports": null,
    "State": "running",
    "Status": "Up About a minute",
    "Created": 1690300445
  }
]
"""

volume_inspect_json = """[
     {
          "Name": "skupper-services",
          "Driver": "local",
          "Mountpoint": "/home/my_user/.local/share/containers/storage/volumes/skupper-services/_data",
          "Labels": {
               "application": "skupper"
          }
     }
]
"""

skupper_services_podman = """{
  "my-service-a": {
    "address": "my-service-a",
    "protocol": "http",
    "ports": [
      8080,
      9090
    ],
    "exposeIngress": "",
    "targets": [
      {
        "name": "*domain.EgressResolverHost={\\"host\\":\\"10.0.0.1\\",\\"ports\\":{\\"8080\\":8080,\\"9090\\":8080}}",
        "targetPorts": {
          "8080": 8080,
          "9090": 8080
        },
        "service": "10.0.0.1"
      }
    ]
  },
  "postgres": {
    "address": "postgres",
    "protocol": "tcp",
    "ports": [
      5432
    ],
    "exposeIngress": "",
    "targets": [
      {
        "name": "*domain.EgressResolverHost={\\"host\\":\\"10.0.0.2\\",\\"ports\\":{\\"5432\\":5432}}",
        "targetPorts": {
          "5432": 5432
        },
        "service": "10.0.0.2"
      },
      {
        "name": "*domain.EgressResolverHost={\\"host\\":\\"10.0.0.3\\",\\"ports\\":{\\"5432\\":2345}}",
        "targetPorts": {
          "5432": 2345
        },
        "service": "10.0.0.3"
      }
    ]
  }
}
"""
