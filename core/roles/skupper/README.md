skupper
=======

The `skupper` role performs the entire Skupper network deployment,
defining links and services across all sites.

It combines the execution of all the following roles:

* skupper-init
* skupper-token
* skupper-link
* skupper-service

Requirements
------------

None.

Role Variables
--------------

See the variables for all the dependant roles.

Dependencies
------------

* role: skupper-init
* role: skupper-token
* role: skupper-link
* role: skupper-service

Example Playbook
----------------

    - hosts: servers
      roles:
         - { role: skupper }

License
-------

Apache 2.0

Author Information
------------------

Skupper team
https://skupper.io
