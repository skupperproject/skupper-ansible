skupper_token
=============

Generates a skupper token, saving the resulting token as a runtime
host variable named `generated_token`.

The `skupper_link` role expects that the target hosts defined as part
of the `links` object have a `generated_token` variable defined, when
links are defined using a host (from ansible inventory).

Requirements
------------

* Skupper CLI

Role Variables
--------------

All flags in the token element are optinal.

```yaml
#
# common flags
#
skupper_token_name: ""

#
# kube specific flags
#
skupper_token_expiry: "15m0s"
skupper_token_password: ""
skupper_token_type: "claim"
skupper_token_uses: 1

#
# podman specific flags
#
skupper_token_ingress_host: ""
```

Dependencies
------------

**Role**

* skupper_option

Example Playbook
----------------

---
- hosts: all
  roles:
    - skupper.network.skupper_token

Example Inventory
-----------------

The following inventory example, demonstrates how an ansible host
can be specified. Note that it has the platform variable as well 
as the `token` field.

```yaml
  site-a:
    skupper_token_type: cert
  site-b:
    skupper_token_uses: 5
  rhel9:
```

License
-------

Apache 2.0

Author Information
------------------

Skupper team
https://skupper.io
