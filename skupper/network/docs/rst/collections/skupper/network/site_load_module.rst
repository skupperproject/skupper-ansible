
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

.. _ansible_collections.skupper.network.site_load_module:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

skupper.network.site_load module -- Loads site information as ansible facts into the respective host
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `skupper.network collection <https://galaxy.ansible.com/skupper/network>`_ (version 1.1.0).

    To install it, use: :code:`ansible-galaxy collection install skupper.network`.
    You need further requirements to be able to use this module,
    see :ref:`Requirements <ansible_collections.skupper.network.site_load_module_requirements>` for details.

    To use it in a playbook, specify: :code:`skupper.network.site_load`.

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

- Loads Skupper site information as a hostvar named 'site'. It contains the site name, site id and inventory hostname related to it. This 'site' info can be used by modules to map runtime information of a skupper site to an ansible host defined through the inventory file.
  Kubernetes options can be set through host variables (kubeconfig, context, namespace). Podman endpoint can be customized through init.podmanEndpoint host variable.

.. note::
    This module has a corresponding :ref:`action plugin <action_plugins>`.

.. Aliases


.. Requirements

.. _ansible_collections.skupper.network.site_load_module_requirements:

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

    
    - name: Loading site information
      skupper.network.site_load:




.. Facts


.. Return values

Return Values
-------------
Common return values are documented :ref:`here <common_return_values>`, the following are the fields unique to this module:

.. rst-class:: ansible-option-table

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1

  * - Key
    - Description

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-site"></div>

      .. _ansible_collections.skupper.network.site_load_module__return-site:

      .. rst-class:: ansible-option-title

      **site**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-site" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Skupper site information


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` always

      .. rst-class:: ansible-option-line
      .. rst-class:: ansible-option-sample

      :ansible-option-sample-bold:`Sample:` :ansible-rv-sample-value:`{"site": {"host": "host-a", "id": "53899d80-1ae6-11ee-be28-1e9341abe0db", "name": "site-a"}}`


      .. raw:: html

        </div>



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

