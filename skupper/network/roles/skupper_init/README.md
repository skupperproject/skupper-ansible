skupper_init
============

Initializes a Skupper site using the CLI

Requirements
------------

Skupper CLI must be installed.

Role Variables
--------------

This role expects optional skupper_init parameters to be provided, using the default values in case it is not present.

Dependencies
------------

**Role**

* skupper_option

Example Playbook
----------------

```yaml
---
- hosts: all
  roles:
    - skupper.network.skupper_init
```

Example Inventory
-----------------

The following inventory example, demonstrates how an ansible host
can be specified. Note that it has the platform variable as well 
as the `init` field.

```yaml
  rhel9:
    platform: "podman"
    skupper_init_ingress_hosts:
    - 192.168.122.1
    - 192.168.15.10
```

License
-------

Apache 2.0

Author Information
------------------

Skupper Team
https://skupper.io
