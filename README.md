# skupper-ansible

Ansible collection and roles for skupper

[![.github/workflows/publish.yml](https://github.com/skupperproject/skupper-ansible/actions/workflows/publish.yml/badge.svg)](https://github.com/skupperproject/skupper-ansible/actions/workflows/publish.yml)

## Collection name

skupper.skupper

## Roles

* [skupper_setup](https://github.com/skupperproject/skupper-ansible/tree/v1/skupper/skupper/roles/skupper_setup)
* [skupper_cli_install](https://github.com/skupperproject/skupper-ansible/tree/v1/skupper/skupper/roles/skupper_cli_install)
* [skupper_option (internal - should not be used directly)](https://github.com/skupperproject/skupper-ansible/tree/v1/skupper/skupper/roles/skupper_option)
* [skupper_init](https://github.com/skupperproject/skupper-ansible/tree/v1/skupper/skupper/roles/skupper_init)
* [skupper_teardown](https://github.com/skupperproject/skupper-ansible/tree/v1/skupper/skupper/roles/skupper_teardown)
* [skupper_token](https://github.com/skupperproject/skupper-ansible/tree/v1/skupper/skupper/roles/skupper_token)
* [skupper_link](https://github.com/skupperproject/skupper-ansible/tree/v1/skupper/skupper/roles/skupper_link)
* [skupper_service](https://github.com/skupperproject/skupper-ansible/tree/v1/skupper/skupper/roles/skupper_service)
* [skupper_update](https://github.com/skupperproject/skupper-ansible/tree/v1/skupper/skupper/roles/skupper_update)

## Requirements

* python >= 3.9
* ansible >= 2.1
* kubectl binary on target hosts
* podman binary on target hosts
