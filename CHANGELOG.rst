===================================
Skupper V2 collection Release Notes
===================================

.. contents:: Topics

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
