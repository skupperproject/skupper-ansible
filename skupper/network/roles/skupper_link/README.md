skupper_link
============

Creates links to other Skupper sites based on generated tokens.

Requirements
------------

* Skupper CLI
* Token generated at the same execution

Role Variables
--------------

This role processes a host variable named `links` which is supposed
to hold an array containing link elements with the following structure:

```yaml
links:
  - host: <inventory host>
    name: <optional link name>
    cost: <optional cost value>
    token: <optional static token yaml>
```

Before executing this role, make sure that the skupper_token role was also
executed as that role will save the tokens as a host variable, so the host
variable must be populated before skupper can create links to a given site.

In case you have a static token to use, then you don't need to invoke the
skupper_token role previously. But when defining links using statically
provided tokens, make sure to add a name to the link.

Dependencies
------------

**Role**

* skupper_common
* skupper_token (when linking by host name)

Example Playbook
----------------

---
- hosts: all
  roles:
    - skupper_token
    - skupper_link

Example Inventory
-----------------

The following inventory example, demonstrates how an ansible host
can be specified. Note that it has the `links` field.

```yaml
  site-a:
  site-b:
  rhel9:
    links:
      - host: site-a
      - host: site-b
        cost: 2
```

License
-------

Apache 2.0

Author Information
------------------

Skupper team
https://skupper.io
