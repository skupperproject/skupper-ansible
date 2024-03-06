
.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.7.0

.. Anchors

.. _ansible_collections.skupper.core.skupper_link_role:

.. Title

skupper.core.skupper_link role -- Maintains existing links on a site
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This role is part of the `skupper.core collection <https://galaxy.ansible.com/ui/repo/published/skupper/core/>`_ (version 1.6.0).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it use: :code:`ansible-galaxy collection install skupper.core`.

    To use it in a playbook, specify: :code:`skupper.core.skupper_link`.

.. contents::
   :local:
   :depth: 2


.. Entry point title

Entry point ``main`` -- Maintains existing links on a site
----------------------------------------------------------

.. version_added

.. rst-class:: ansible-version-added

New in skupper.core 1.6.0

.. Deprecated


Synopsis
^^^^^^^^

.. Description

- Maintains existing links on a site based on the provided links object.
  All desired links must be provided as part of the \ :literal:`skupper\_link\_links`\  object.
  Links must specify a target hostname (a valid host from the Ansible inventory), in such
  case the token for the respective link is expected to be available as a host fact (for the target host)
  named \ :literal:`skupper\_token\_generated\_token`\ . This fact is set automatically if the \ `skupper.core.skupper\_token role <skupper_token_role.html>`__\ 
  is invoked prior to this one.
  Alternatively if the intention is to use a statically provided token, then the \ :literal:`token`\  parameter of the link object
  must be populated as well as the \ :literal:`name`\  of the link.
  This role uses the \ :ref:`skupper.core.links\_load <ansible_collections.skupper.core.links_load_module>`\  and \ :ref:`skupper.core.links <ansible_collections.skupper.core.links_module>`\  modules to ensure all desired are defined.


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
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_link_links"></div>

      .. _ansible_collections.skupper.core.skupper_link_role__parameter-main__skupper_link_links:

      .. rst-class:: ansible-option-title

      **skupper_link_links**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_link_links" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=dictionary`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      List of all desired links to exist at a given site.
          Links that are defined on the list, but does not exist, will be created.
          The links that exist on the Skupper site but are not defined through this list
          will be removed.
          


      .. raw:: html

        </div>
    
  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_link_links/cost"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.skupper.core.skupper_link_role__parameter-main__skupper_link_links/cost:

      .. rst-class:: ansible-option-title

      **cost**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_link_links/cost" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The cost of the link.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`1`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_link_links/host"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.skupper.core.skupper_link_role__parameter-main__skupper_link_links/host:

      .. rst-class:: ansible-option-title

      **host**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_link_links/host" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The Ansible Inventory hostname to use as a target for this link.
          It can be populated if the \ `skupper.core.skupper\_token role <skupper_token_role.html>`__\  has been invoked earlier,
          of when using the \ `skupper.core.network\_config role <network_config_role.html>`__\  (which also invokes the \ :literal:`skupper\_token role`\ 
          as a dependency.
          In case the intention is to use a static token, this argument must not be provided.
          


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_link_links/name"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.skupper.core.skupper_link_role__parameter-main__skupper_link_links/name:

      .. rst-class:: ansible-option-title

      **name**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_link_links/name" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The name of the link to be defined at the target site.
          When using a static token, this argument is mandatory, as it is used to determine if the link already exists.
          


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_link_links/token"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.skupper.core.skupper_link_role__parameter-main__skupper_link_links/token:

      .. rst-class:: ansible-option-title

      **token**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_link_links/token" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      A static token to be used when creating this link.
          When a static token is provided, the \ :literal:`name`\  argument must also be set and the \ :literal:`host`\  argument
          must not be provided.
          The token must be represented as a YAML string.
          


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

