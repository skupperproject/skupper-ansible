skupper-token
=============

Generates a skupper token, saving the resulting token as a runtime
host variable named `generatedToken`.

The `skupper-link` role expects that the target hosts defined as part
of the `links` object have a `generatedToken` variable defined.

Requirements
------------

* Skupper CLI

Role Variables
--------------

All flags in the token element are optinal.

```yaml
token:
  #
  # common flags
  #
  name: ""

  #
  # kube specific flags
  #
  expiry: "15m0s"
  password: ""
  type: "claim"
  uses: 1

  #
  # podman specific flags
  #
  ingress-host: ""
```

Dependencies
------------

**Role**

* skupper-common

Example Playbook
----------------

---
- hosts: all
  roles:
    - skupper-token

Example Inventory
-----------------

The following inventory example, demonstrates how an ansible host
can be specified. Note that it has the platform variable as well 
as the `token` field.

```yaml
  site-a:
    token:
      type: cert
  site-b:
    token:
      uses: 5
  rhel9:
```

License
-------

Apache 2.0

Author Information
------------------

Skupper team
https://skupper.io
