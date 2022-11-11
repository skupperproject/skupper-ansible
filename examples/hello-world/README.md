# Skupper - Hello World example using Ansible

This demo deploys the Skupper [hello world example](https://github.com/skupperproject/skupper-example-hello-world)
in two namespaces: west and east. 

We use Ansible to deploy the workloads and setup the Skupper network.

# Pre-requisites

* Ansible >= 2.9.0

# Running the demo

## Install the required collections

```
ansible-galaxy collection install -r requirements.yml
```

## Deploying the demo

```
ansible-playbook -i inventory.yml setup.yml
```

## Teardown

```
ansible-playbook -i inventory.yml teardown.yml
```
