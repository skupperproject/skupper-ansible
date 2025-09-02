===================================
Skupper V2 collection Release Notes
===================================

.. contents:: Topics

v2.0.1
======

Release Summary
---------------

Fixes minor issues

Major Changes
-------------

- Allow customization of router image on system module - backport from 2.0 (https://github.com/skupperproject/skupper-ansible/pull/61)
- Fixed parsing of optional skupper router image env var (https://github.com/skupperproject/skupper-ansible/pull/63)

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
