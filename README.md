# Skupper V2 Collection for Ansible

# Description

The skupper.v2 collection provides modules to help maintain your Virtual Application Network (VAN),
in the hybrid cloud, using Skupper V2. It allows you to define your Skupper V2 resources, generate
and retrieve access tokens or links, and to manage the lifecycle of your non-kubernetes sites,
allowing you to connect your entire VAN in a simple and intuitive way.

# Requirements

The following python modules are required:

* PyYAML
* Kubernetes

You will also need one of the following container engines,
if you need to manage the lifecycle of non-kubernetes sites:

* Podman or Docker

# Installation

To install the collection, run:

```
ansible-galaxy collection install skupper.v2
```

And to install the python dependencies, you can run:

```
pip install -r requirements.txt
```

# Examples

## Hello world example using Kubernetes sites

The following tasks demonstrate how to run the Skupper Hello World example
using two namespaces in a Kubernetes cluster.

It assumes that:

* Skupper V2 is already running
* Namespaces `west` and `east` exist

```
- name: Creating Skupper resources on west namespace
  skupper.v2.resource:
    path: "{{ item }}"
    namespace: "west"
  with_items:
    - https://raw.githubusercontent.com/skupperproject/skupper-example-yaml/refs/heads/v2/west/frontend.yaml
    - https://raw.githubusercontent.com/skupperproject/skupper-example-yaml/refs/heads/v2/west/site.yaml
    - https://raw.githubusercontent.com/skupperproject/skupper-example-yaml/refs/heads/v2/west/listener.yaml

- name: Creating Skupper resources on east namespace
  skupper.v2.resource:
    path: "{{ item }}"
    namespace: "east"
  with_items:
    - https://raw.githubusercontent.com/skupperproject/skupper-example-yaml/refs/heads/v2/east/backend.yaml
    - https://raw.githubusercontent.com/skupperproject/skupper-example-yaml/refs/heads/v2/east/site.yaml
    - https://raw.githubusercontent.com/skupperproject/skupper-example-yaml/refs/heads/v2/east/connector.yaml

- name: Issue a Skupper access token from west namespace
  skupper.v2.token:
    namespace: "west"
    name: west-grant
    redemptions_allowed: 1
  register: west

- name: Apply token to east site
  skupper.v2.resource:
    def: "{{ west.token }}"
    namespace: "east"
```

## Hello world example using Podman sites

The following tasks demonstrate how to run the Skupper Hello World example
using just Podman containers.
It assumes that:

* Podman is installed
* podman.socket (systemd service is running)
* Frontend and Backend containers are running (see below)

Running the frontend and backend containers:

```
podman run --name frontend -d --rm -p 127.0.0.1:7070:8080 quay.io/skupper/hello-world-frontend --backend http://host.containers.internal:8080
podman run --name backend -d --rm -p 127.0.0.1:9090:8080 quay.io/skupper/hello-world-backend
```

Tasks to run west and east sites using podman:

(resources are available at https://github.com/fgiorgetti/skupper-example-yaml/tree/v2-nonkube-resources)

```
---
- hosts: localhost
  gather_facts: no
  tasks:
    - name: Creating Skupper resources on west namespace
      skupper.v2.resource:
        path:  /home/fgiorget/git/skupper-example-yaml/west/west-nonkube.yaml
        namespace: "west"
        platform: "podman"

    - name: Creating Skupper resources on east namespace
      skupper.v2.resource:
        path: /home/fgiorget/git/skupper-example-yaml/east/east-nonkube.yaml
        namespace: "east"
        platform: "podman"

    - name: Setup the west site and retrieve a static link
      skupper.v2.system:
        namespace: "west"
        platform: "podman"
      register: west

    - name: Apply token to east site
      skupper.v2.resource:
        def: "{{ west.links['0.0.0.0'] }}"
        namespace: "east"
        platform: "podman"

    - name: Setup the east site
      skupper.v2.system:
        namespace: "east"
        platform: "podman"
```

To clean up you can run the following commands and tasks:

Stopping frontend and backend containers:

```
podman stop frontend backend
```

Teardown both frontend and backend namespaces:

```
- name: Teardown namespace
  skupper.v2.system:
    action: teardown
    namespace: "{{ item }}"
    platform: "podman"
  with_items:
    - west
    - east
```


# Testing

If you are interested in running the integration tests locally, you can adjust
the value of `kubeconfig` on `tests/integration/integration_config.yml` so that
tests run against your specified cluster.

***WARNING***:
* Tests will deploy skupper v2 in cluster scope on the `skupper` namespace
* It will create and delete several namespaces
* Do not run it in a production cluster

Run:

```
make integration
```

# Licensing

GNU General Public License v3.0 or later

See LICENCE to see the full text.
