
.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.7.0

.. Anchors

.. _ansible_collections.skupper.core.skupper_token_role:

.. Title

skupper.core.skupper_token role -- Creates a Skupper token that can be used by other sites to establish links
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This role is part of the `skupper.core collection <https://galaxy.ansible.com/ui/repo/published/skupper/core/>`_ (version 1.6.0).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it use: :code:`ansible-galaxy collection install skupper.core`.

    To use it in a playbook, specify: :code:`skupper.core.skupper_token`.

.. contents::
   :local:
   :depth: 2


.. Entry point title

Entry point ``main`` -- Creates a Skupper token that can be used by other sites to establish links
--------------------------------------------------------------------------------------------------

.. version_added

.. rst-class:: ansible-version-added

New in skupper.core 1.6.0

.. Deprecated


Synopsis
^^^^^^^^

.. Description

- Creates a Skupper token that can be used by other sites to establish links.
  The token is generated as a host fact named \ :literal:`skupper\_token\_generated\_token`\ .


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
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_token_expiry"></div>

      .. _ansible_collections.skupper.core.skupper_token_role__parameter-main__skupper_token_expiry:

      .. rst-class:: ansible-option-title

      **skupper_token_expiry**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_token_expiry" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Duration for which a token claim is considered as valid.
          This is only used when \ :literal:`skupper\_token\_type=claim`\  and \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"15m0s"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_token_ingress_host"></div>

      .. _ansible_collections.skupper.core.skupper_token_role__parameter-main__skupper_token_ingress_host:

      .. rst-class:: ansible-option-title

      **skupper_token_ingress_host**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_token_ingress_host" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The ingress-host to use in the generated token on Podman sites.
          Usually when a podman site has more than one ingress host, this might be needed.
          This can only be used when \ :literal:`skupper\_option\_platform=podman`\ .
          If absent or empty, Skupper will use the first available ingress host.
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_token_name"></div>

      .. _ansible_collections.skupper.core.skupper_token_role__parameter-main__skupper_token_name:

      .. rst-class:: ansible-option-title

      **skupper_token_name**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_token_name" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Name of the token that will be created.
          When using \ :literal:`skupper\_token\_type=claim`\ , only one token can exist with a given name.
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"skupper"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_token_password"></div>

      .. _ansible_collections.skupper.core.skupper_token_role__parameter-main__skupper_token_password:

      .. rst-class:: ansible-option-title

      **skupper_token_password**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_token_password" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Password to be set of the token claim. If empty, a random password will be generated (default).
          This is only used when \ :literal:`skupper\_token\_type=claim`\  and \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_token_type"></div>

      .. _ansible_collections.skupper.core.skupper_token_role__parameter-main__skupper_token_type:

      .. rst-class:: ansible-option-title

      **skupper_token_type**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_token_type" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      The token type to use.
          When using \ :literal:`skupper\_option\_platform=podman`\ , the only allowed value is \ :literal:`cert`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`"claim"` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`"cert"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_token_uses"></div>

      .. _ansible_collections.skupper.core.skupper_token_role__parameter-main__skupper_token_uses:

      .. rst-class:: ansible-option-title

      **skupper_token_uses**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_token_uses" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Number of times that the given token claim can be redeemed.
          This is only used when \ :literal:`skupper\_token\_type=claim`\  and \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`1`

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

