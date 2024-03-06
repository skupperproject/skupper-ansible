
.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.7.0

.. Anchors

.. _ansible_collections.skupper.core.site_load_module:

.. Anchors: short name for ansible.builtin

.. Title

skupper.core.site_load module -- Loads site information as ansible facts into the respective host
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `skupper.core collection <https://galaxy.ansible.com/ui/repo/published/skupper/core/>`_ (version 1.6.0).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install skupper.core`.
    You need further requirements to be able to use this module,
    see :ref:`Requirements <ansible_collections.skupper.core.site_load_module_requirements>` for details.

    To use it in a playbook, specify: :code:`skupper.core.site_load`.

.. version_added

.. rst-class:: ansible-version-added

New in skupper.core 1.1.0

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

.. _ansible_collections.skupper.core.site_load_module_requirements:

Requirements
------------
The below requirements are needed on the host that executes this module.

- python \>= 3.9
- kubectl if using kubernetes platform
- podman v4+ if using podman as the site platform






.. Options

Parameters
----------

.. tabularcolumns:: \X{1}{3}\X{2}{3}

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1
  :class: longtable ansible-option-table

  * - Parameter
    - Comments

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-context"></div>

      .. _ansible_collections.skupper.core.site_load_module__parameter-context:

      .. rst-class:: ansible-option-title

      **context**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-context" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      KUBECONFIG context to use


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-hostname"></div>

      .. _ansible_collections.skupper.core.site_load_module__parameter-hostname:

      .. rst-class:: ansible-option-title

      **hostname**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-hostname" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Ansible's inventory\_hostname used to represent the given Skupper site

      This is automatically provided by the action plugin


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-kubeconfig"></div>

      .. _ansible_collections.skupper.core.site_load_module__parameter-kubeconfig:

      .. rst-class:: ansible-option-title

      **kubeconfig**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-kubeconfig" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      KUBECONFIG file to be used (defaults to ${HOME}/.kube/config)


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-namespace"></div>

      .. _ansible_collections.skupper.core.site_load_module__parameter-namespace:

      .. rst-class:: ansible-option-title

      **namespace**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-namespace" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Kubernetes namespace to run the Skupper site


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-platform"></div>

      .. _ansible_collections.skupper.core.site_load_module__parameter-platform:

      .. rst-class:: ansible-option-title

      **platform**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-platform" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Platform to be used (kubernetes or podman)


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-podman_endpoint"></div>

      .. _ansible_collections.skupper.core.site_load_module__parameter-podman_endpoint:

      .. rst-class:: ansible-option-title

      **podman_endpoint**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-podman_endpoint" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Podman endpoint to use when managing a Skupper site


      .. raw:: html

        </div>


.. Attributes


.. Notes


.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    
    - name: Loading site information
      skupper.core.site_load:




.. Facts


.. Return values

Return Values
-------------
Common return values are documented :ref:`here <common_return_values>`, the following are the fields unique to this module:

.. tabularcolumns:: \X{1}{3}\X{2}{3}

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1
  :class: longtable ansible-option-table

  * - Key
    - Description

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-site"></div>

      .. _ansible_collections.skupper.core.site_load_module__return-site:

      .. rst-class:: ansible-option-title

      **site**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-site" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

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

Authors
~~~~~~~

- Fernando Giorgetti (@fgiorgetti)



.. Extra links

Collection links
~~~~~~~~~~~~~~~~

.. ansible-links::

  - title: "Issue Tracker"
    url: "http://github.com/skupperproject/skupper-ansible/issues"
    external: true
  - title: "Homepage"
    url: "http://skupper.io"
    external: true
  - title: "Repository (Sources)"
    url: "http://github.com/skupperproject/skupper-ansible"
    external: true


.. Parsing errors

