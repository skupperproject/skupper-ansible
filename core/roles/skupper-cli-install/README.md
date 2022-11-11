skupper-cli-install
=========

Installs the skupper (binary) into the target hosts from the github release tarballs.

Requirements
------------

None.

Role Variables
--------------
All the variables are optional, and if they are provided, then identified or default values will not be used.

```yaml
skupper_cli:
  version: ""  # the version to download
  os: ""       # the target operating system (one of: linux, win or mac)
  arch: ""     # the arch name used to compose the download tar ball
  location: "" # location in the remote host to save the skupper binary (default: /usr/local/bin)
```

Dependencies
------------

None.

Example Playbook
----------------

  ---
  - hosts: all
    user: root
    roles:
      - skupper-cli-install

License
-------

Apache 2.0

Author Information
------------------

Skupper team
https://skupper.io
