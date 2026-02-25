===================================
Skupper V2 collection Release Notes
===================================

.. contents:: Topics

v2.1.3
======

Release Summary
---------------

Update components to 2.1.3

Major Changes
-------------

- Add a retry multiplier to integration tests (#86)
- Fix unhandled exception when a running a command that does not exist (#83)
- Increased retry count on token integration test (#73)
- Mount and uses the REGISTRY_AUTH_FILE when starting a system site (#74)
- Updated cli image to 2.1.3
- Updated skupper-controller image to 2.1.3

v2.1.1
======

Release Summary
---------------

Introducing the controller module for system sites

Major Changes
-------------

- New module skupper.v2.controller for system sites
- Refactored skupper.v2.system actions to match the Skupper CLI actions for system sites

New Modules
-----------

- skupper.v2.controller - Manages the lifecycle of the skupper-controller for system sites

v2.0.0
======

Release Summary
---------------

Initial release of the skupper.v2 collection

Major Changes
-------------

- Introducing new modules resource, token and system (https://github.com/skupperproject/skupper-ansible/issues/35)

New Modules
-----------

- skupper.v2.resource - Place skupper resources (yaml) in the provided namespace
- skupper.v2.system - Manages the lifecycle of non-kube namespaces
- skupper.v2.token - Issue or retrieve access tokens and static links
