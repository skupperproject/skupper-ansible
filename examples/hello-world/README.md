# Skupper - Hello World example using Ansible

This demo deploys the Skupper [hello world example](https://github.com/skupperproject/skupper-example-hello-world)
in two namespaces: west and east. 

We use Ansible to deploy the workloads and set up the Skupper network.

# Pre-requisites

* Ansible >= 2.9.0
* Skupper (binary)
* KUBECONFIG set to a cluster with appropriate permissions to create and remove namespaces

# Running the demo

## Install the required collections

```
ansible-galaxy collection install -r requirements.yml
```

## Deploying the demo

The inventory file describes the whole Skupper network, with host variables
providing the necessary information for all skupper roles.

The `setup.yml` playbook will prepare the Kubernetes namespaces with
workloads used by the hello world example, and later it will invoke the
`skupper` role, which will set up the entire skupper.core.

This role is idempotent, so as long as your host variables describe your desired
skupper.core state, calling the `skupper` role again should only update the
modified resources.

Looking at the variables on the `west` host on the `inventory.yml` file, we see:

```yaml
        west:
          ansible_connection: local # ansible will use your current session
          namespace: west # the namespace to use for all skupper commands
          init: # arguments to be passed to the init command
            siteName: west
            enableServiceSync: 'false'
            enableFlowCollector: 'true'
            enableConsole: 'true'
            consolePassword: 'admin'
          services: # list of services to be maintained
            frontend:
              ports:
                - 8080
              targets:
                - type: "deployment"
                  name: "frontend"
            backend:
              ports:
                - 8080
        east:
          ansible_connection: local
          namespace: east
          init:
            siteName: east
            enableServiceSync: 'false'
          links: # create a link to the "west" site
            - host: west
          services:
            backend:
              ports:
                - 8080
              targets:
                - type: "deployment"
                  name: "backend"
```

When the `skupper` role is invoked, it will try to initialize the skupper site,
maintain the services according to the inventory, generate a token to the respective site (ansible host)
and go through the requested links. If you specify a link to a given site (by ansible host name), the skupper_link
role will expect that the skupper_token role was executed for that host, otherwise it will expect that a token is
manually provided as part of the link definition (as a YAML entry).

To deploy it, run:

```
ansible-playbook -i inventory.yml setup.yml
```

## Teardown

The teardown playbook will remove the namespaces created earlier.

```
ansible-playbook -i inventory.yml teardown.yml
```
