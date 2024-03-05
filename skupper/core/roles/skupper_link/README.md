skupper_link
============

Creates links to other Skupper sites based on generated tokens.

Requirements
------------

* Skupper CLI
* Token generated at the same execution

Role Variables
--------------

This role processes a host variable named `skupper_link_links` which is supposed
to hold an array containing link elements with the following structure:

```yaml
skupper_link_links:
  - host: <inventory host - required when relying on generated token; must be empty when using a static token>
    name: <link name - optional when using host; required when using a static token>
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

* skupper_option
* skupper_token (when linking by host name)

Example Playbook
----------------

Using a dynamically generated token:

```yaml
---
- hosts: all
  tasks:
    - ansible.builtin.include_role:
        name: skupper.core.skupper_token
    - ansible.builtin.include_role:
        name: skupper.core.skupper_link
```

Using a static token:

```yaml
---
- hosts: all
  tasks:
    - ansible.builtin.include_role:
        name: skupper.core.skupper_link
      vars:
        skupper_link_links:
          - name: link1
            token: |
              your token as YAML
```
      
Example Inventory
-----------------

The following inventory example, demonstrates how an ansible host
can be specified. Note that it has the `links` field.

```yaml
  site-a:
  site-b:
  rhel9:
    skupper_link_links:
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
