skupper_service
===============

Creates all services defined through the `skupper_service_services` variable for the
related ansible host.

It creates the service, binding it to all (optional) targets.

Requirements
------------

* Skupper CLI

Role Variables
--------------

A `skupper_service_services` array element must be defined at the host, so that the role
can iterate through each service, creating and binding it to the defined
target.

```yaml
skupper_service_services:
  # Sample service definition (indexed by name)
  - name:                        # name of the service
    ports: []                    # int array
    protocol: ""                 # choice tcp, http, http2
    labels: []                   # label and value separated by equal sign
    aggregate: ""                # choice: json, multiplart
    generate_tls_secrets: false  # boolean
    event_channel: false         # boolean
    targets:                     # array of type and name
    - type: ""                   # type of target to bind (values vary based on selected platform)
      name: ""                   # value that represents the selected target type
      ports: []                  # array mapping service ports to target ports

    #
    # kubernetes flags
    #
    # valid targetType values: "deployment", "statefulset", "pods", "service"
    #

    #
    # podman flags
    #
    # valid targetType values: "host"
    container_name: ""   # optinal alternative name for service container
    host_ip: ""          # optional host ip address used to bind to the service ports
    host_ports: []       # array mapping service ports to a host port

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
    - skupper.skupper.skupper_service

Example Inventory
-----------------

The following inventory example, demonstrates how an ansible host
can be specified. Note that it has the `services` field.

```yaml
  site-a:
    skupper_service_services:
      - name: nginx
        ports:
          - 8080
        labels:
          - label1=value1
          - label2=value2
  site-b:
    skupper_service_services:
      - name: nginx
        ports:
          - 8080
        targets:
          - type: deployment
            name: nginx
  rhel9:
    skupper_service_services:
      - name: nginx
        ports: [8080]
        targets:
          - type: "host"
            name: "192.168.122.1"
        host_ip: "192.168.122.1"
        host_ports:
          - 8080:8888
```

License
-------

Apache 2.0

Author Information
------------------

Skupper team
https://skupper.io
