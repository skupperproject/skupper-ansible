
.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.7.0

.. Anchors

.. _ansible_collections.skupper.core.skupper_cli_install_role:

.. Title

skupper.core.skupper_cli_install role -- Installs the Skupper CLI
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This role is part of the `skupper.core collection <https://galaxy.ansible.com/ui/repo/published/skupper/core/>`_ (version 1.6.0).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it use: :code:`ansible-galaxy collection install skupper.core`.

    To use it in a playbook, specify: :code:`skupper.core.skupper_cli_install`.

.. contents::
   :local:
   :depth: 2


.. Entry point title

Entry point ``main`` -- Installs the Skupper CLI
------------------------------------------------

.. version_added

.. rst-class:: ansible-version-added

New in skupper.core 1.6.0

.. Deprecated


Synopsis
^^^^^^^^

.. Description

- Installs the Skupper CLI from released versions available
  through https://github.com/skupperproject/skupper/releases.


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
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_cli_install_arch"></div>

      .. _ansible_collections.skupper.core.skupper_cli_install_role__parameter-main__skupper_cli_install_arch:

      .. rst-class:: ansible-option-title

      **skupper_cli_install_arch**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_cli_install_arch" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Target Architecture


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"amd64"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_cli_install_force"></div>

      .. _ansible_collections.skupper.core.skupper_cli_install_role__parameter-main__skupper_cli_install_force:

      .. rst-class:: ansible-option-title

      **skupper_cli_install_force**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_cli_install_force" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean` / :ansible-option-required:`required`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Target installation directory


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_cli_install_location"></div>

      .. _ansible_collections.skupper.core.skupper_cli_install_role__parameter-main__skupper_cli_install_location:

      .. rst-class:: ansible-option-title

      **skupper_cli_install_location**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_cli_install_location" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Target installation directory


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"/usr/local/bin"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_cli_install_os"></div>

      .. _ansible_collections.skupper.core.skupper_cli_install_role__parameter-main__skupper_cli_install_os:

      .. rst-class:: ansible-option-title

      **skupper_cli_install_os**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_cli_install_os" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Target OS


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"linux"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_cli_install_version"></div>

      .. _ansible_collections.skupper.core.skupper_cli_install_role__parameter-main__skupper_cli_install_version:

      .. rst-class:: ansible-option-title

      **skupper_cli_install_version**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_cli_install_version" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The Skupper CLI version to be installed


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"1.6.0"`

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

