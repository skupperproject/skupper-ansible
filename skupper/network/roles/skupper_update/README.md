skupper_update
==============

Updates skupper using the available skupper CLI.

Requirements
------------

* Skupper CLI with the desired version

Role Variables
--------------

```yaml
  update:
    # restart skupper daemons even when update is not performed
    forceRestart: false # boolean
```

Dependencies
------------

**Role**

* skupper_common

Example Playbook
----------------

---
- hosts: all
  roles:
    - skupper_token

Example Inventory
-----------------

The following inventory example, demonstrates how an ansible host
can be specified. Note that it has the platform variable as well 
as the `update` field.

```yaml
  site-a:
    update:
      forceRestart: true
```

License
-------

Apache 2.0

Author Information
------------------

Skupper team
https://skupper.io
