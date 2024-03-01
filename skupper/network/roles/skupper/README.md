skupper
=======

The `skupper` role performs the entire Skupper network deployment,
defining links and services across all sites.

It combines the execution of all the following roles:

* skupper_init
* skupper_token
* skupper_link
* skupper_service

Requirements
------------

None.

Role Variables
--------------

See the variables for all the dependant roles.

Dependencies
------------

* role: skupper_init
* role: skupper_token
* role: skupper_link
* role: skupper_service

Example Playbook
----------------

```yaml
    - hosts: all
      roles:
         - skupper.network.skupper
```

License
-------

Apache 2.0

Author Information
------------------

Skupper team
https://skupper.io
