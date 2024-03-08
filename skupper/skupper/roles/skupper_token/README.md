skupper_token
=============

Generates a skupper token, saving the resulting token as a runtime
host variable named `generated_token`.

The `skupper_link` role expects that the target hosts defined as part
of the `links` object have a `generated_token` fact defined, when
links are defined using a host (from ansible inventory).

Requirements
------------

* Skupper CLI

Dependencies
------------

**Role**

* skupper_option

Example Playbook
----------------

---
- hosts: all
  roles:
    - skupper.skupper.skupper_token

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
