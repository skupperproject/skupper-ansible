skupper_common
=========

This role is meant to be used as a dependency by other skupper roles.
It provides default variables and generic validations.

Requirements
------------

None.

Role Variables
--------------

The following variables can be defined for each host as they will be used to help
composing the skupper command line.

* platform: kubernetes or podman (kubernetes is the default if not provided)

The following variables are just relevant to kubernetes platform:

* kubeconfig: the kubeconfig file to use
* context: the context in the kubeconfig file to use
* namespace: the namespace to use

Dependencies
------------

None.

Example Playbook
----------------

This role is not meant to be used in a playbook.

License
-------

Apache 2.0

Author Information
------------------

Skupper team
https://skupper.io