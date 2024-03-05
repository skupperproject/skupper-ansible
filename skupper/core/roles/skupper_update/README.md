skupper_update
==============

Updates skupper using the available skupper CLI.

Requirements
------------

* Skupper CLI with the desired version

Role Variables
--------------

```yaml
  # restart skupper daemons even when update is not performed
  skupper_update_force_restart: false
```

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
    - skupper.core.skupper_update
```

Example Inventory
-----------------

The following inventory example, demonstrates how an ansible host
can be specified. Note that it has the platform variable as well 
as the `update` field.

```yaml
  site-a:
    skupper_update_force_restart: true
```

License
-------

Apache 2.0

Author Information
------------------

Skupper team
https://skupper.io
