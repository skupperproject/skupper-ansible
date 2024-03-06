
.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.7.0

.. Anchors

.. _ansible_collections.skupper.core.skupper_option_role:

.. Title

skupper.core.skupper_option role -- Provides common parameters to be used across the skupper.core roles.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This role is part of the `skupper.core collection <https://galaxy.ansible.com/ui/repo/published/skupper/core/>`_ (version 1.6.0).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it use: :code:`ansible-galaxy collection install skupper.core`.

    To use it in a playbook, specify: :code:`skupper.core.skupper_option`.

.. contents::
   :local:
   :depth: 2


.. Entry point title

Entry point ``main`` -- Provides common parameters to be used across the skupper.core roles.
--------------------------------------------------------------------------------------------

.. version_added

.. rst-class:: ansible-version-added

New in skupper.core 1.6.0

.. Deprecated


Synopsis
^^^^^^^^

.. Description

- Provides common parameters to be used across the skupper.core roles (except skupper\_cli\_install).
  This role is not supposed to be executed directly, as the intent is simply to be used as a dependency
  to all other skupper.core roles that need to use the global options.


.. Requirements


.. Options

Parameters
^^^^^^^^^^

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
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_option_kubeconfig"></div>

      .. _ansible_collections.skupper.core.skupper_option_role__parameter-main__skupper_option_kubeconfig:

      .. rst-class:: ansible-option-title

      **skupper_option_kubeconfig**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_option_kubeconfig" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Kubeconfig file to use, if empty uses the default under ${HOME}/.kube/config


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_option_kubecontext"></div>

      .. _ansible_collections.skupper.core.skupper_option_role__parameter-main__skupper_option_kubecontext:

      .. rst-class:: ansible-option-title

      **skupper_option_kubecontext**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_option_kubecontext" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Kubernetes context to use, if empty uses the currently set context


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_option_namespace"></div>

      .. _ansible_collections.skupper.core.skupper_option_role__parameter-main__skupper_option_namespace:

      .. rst-class:: ansible-option-title

      **skupper_option_namespace**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_option_namespace" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Kubernetes namespace to use, if empty uses the currently set namespace


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_option_platform"></div>

      .. _ansible_collections.skupper.core.skupper_option_role__parameter-main__skupper_option_platform:

      .. rst-class:: ansible-option-title

      **skupper_option_platform**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_option_platform" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Target platform (kubernetes or podman)


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`"kubernetes"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"podman"`


      .. raw:: html

        </div>


.. Attributes


.. Notes


.. Seealso


Authors
^^^^^^^

- Skupper team



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

