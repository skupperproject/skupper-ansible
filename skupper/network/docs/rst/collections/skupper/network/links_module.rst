
.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. role:: ansible-attribute-support-label
.. role:: ansible-attribute-support-property
.. role:: ansible-attribute-support-full
.. role:: ansible-attribute-support-partial
.. role:: ansible-attribute-support-none
.. role:: ansible-attribute-support-na
.. role:: ansible-option-type
.. role:: ansible-option-elements
.. role:: ansible-option-required
.. role:: ansible-option-versionadded
.. role:: ansible-option-aliases
.. role:: ansible-option-choices
.. role:: ansible-option-choices-default-mark
.. role:: ansible-option-default-bold
.. role:: ansible-option-configuration
.. role:: ansible-option-returned-bold
.. role:: ansible-option-sample-bold

.. Anchors

.. _ansible_collections.skupper.network.links_module:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

skupper.network.links module -- Update links based on provided links list
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `skupper.network collection <https://galaxy.ansible.com/skupper/network>`_ (version 1.1.0).

    To install it, use: :code:`ansible-galaxy collection install skupper.network`.
    You need further requirements to be able to use this module,
    see :ref:`Requirements <ansible_collections.skupper.network.links_module_requirements>` for details.

    To use it in a playbook, specify: :code:`skupper.network.links`.

.. version_added

.. rst-class:: ansible-version-added

New in skupper.network 1.1.0

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Updates the links defined by the respective site, based on the links list defined through the host variables.
- Existing links that cannot be mapped to an inventory host will be deleted.
- Links with a corresponding token (provided by skupper\_token role) or manually through the token property will be created.
- If a corresponding token cannot be found for a requested link, it will fail.

.. note::
    This module has a corresponding :ref:`action plugin <action_plugins>`.

.. Aliases


.. Requirements

.. _ansible_collections.skupper.network.links_module_requirements:

Requirements
------------
The below requirements are needed on the host that executes this module.

- kubectl if using kubernetes platform
- podman v4+ if using podman as the site platform






.. Options


.. Attributes


.. Notes


.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    
    - name: Updating links
      skupper.network.links:




.. Facts


.. Return values


..  Status (Presently only deprecated)


.. Authors



.. Extra links

Collection links
~~~~~~~~~~~~~~~~

.. raw:: html

  <p class="ansible-links">
    <a href="http://github.com/skupperproject/skupper-ansible/issues" aria-role="button" target="_blank" rel="noopener external">Issue Tracker</a>
    <a href="http://skupper.io" aria-role="button" target="_blank" rel="noopener external">Homepage</a>
    <a href="http://github.com/skupperproject/skupper-ansible" aria-role="button" target="_blank" rel="noopener external">Repository (Sources)</a>
  </p>

.. Parsing errors

