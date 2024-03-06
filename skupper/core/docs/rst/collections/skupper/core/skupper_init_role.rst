
.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.7.0

.. Anchors

.. _ansible_collections.skupper.core.skupper_init_role:

.. Title

skupper.core.skupper_init role -- Initializes a Skupper site
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This role is part of the `skupper.core collection <https://galaxy.ansible.com/ui/repo/published/skupper/core/>`_ (version 1.6.0).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it use: :code:`ansible-galaxy collection install skupper.core`.

    To use it in a playbook, specify: :code:`skupper.core.skupper_init`.

.. contents::
   :local:
   :depth: 2


.. Entry point title

Entry point ``main`` -- Initializes a Skupper site
--------------------------------------------------

.. version_added

.. rst-class:: ansible-version-added

New in skupper.core 1.6.0

.. Deprecated


Synopsis
^^^^^^^^

.. Description

- Initializes a Skupper site based on provided options and parameters.
  Some arguments are only used when \ :literal:`skupper\_option\_platform`\  is set to \ :literal:`kubernetes`\ 
  and others when set to \ :literal:`podman`\ .
  These arguments are similar to the arguments accepted by the Skupper CLI, when
  the initialization is performed against a given platform (kubernetes or podman).


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
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_annotations"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_annotations:

      .. rst-class:: ansible-option-title

      **skupper_init_annotations**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_annotations" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Annotations to add to skupper pods.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_bind_port"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_bind_port:

      .. rst-class:: ansible-option-title

      **skupper_init_bind_port**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_bind_port" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Ingress host binding port used for incoming links from sites using interior mode.
          This argument is only used when \ :literal:`skupper\_option\_platform=podman`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`55671`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_bind_port_edge"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_bind_port_edge:

      .. rst-class:: ansible-option-title

      **skupper_init_bind_port_edge**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_bind_port_edge" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Ingress host binding port used for incoming links from sites using edge mode.
          This argument is only used when \ :literal:`skupper\_option\_platform=podman`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`45671`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_bind_port_flow_collector"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_bind_port_flow_collector:

      .. rst-class:: ansible-option-title

      **skupper_init_bind_port_flow_collector**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_bind_port_flow_collector" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Ingress host binding port used for flow-collector and console.
          This argument is only used when \ :literal:`skupper\_option\_platform=podman`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`8010`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_config_sync_cpu"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_config_sync_cpu:

      .. rst-class:: ansible-option-title

      **skupper_init_config_sync_cpu**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_config_sync_cpu" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      CPU request for config-sync pods.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_config_sync_cpu_limit"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_config_sync_cpu_limit:

      .. rst-class:: ansible-option-title

      **skupper_init_config_sync_cpu_limit**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_config_sync_cpu_limit" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      CPU limit for config-sync pods.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_config_sync_memory"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_config_sync_memory:

      .. rst-class:: ansible-option-title

      **skupper_init_config_sync_memory**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_config_sync_memory" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Memory request for config-sync pods.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_config_sync_memory_limit"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_config_sync_memory_limit:

      .. rst-class:: ansible-option-title

      **skupper_init_config_sync_memory_limit**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_config_sync_memory_limit" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Memory limit for config-sync pods.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_console_auth"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_console_auth:

      .. rst-class:: ansible-option-title

      **skupper_init_console_auth**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_console_auth" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Authentication mode for console(s).
          On Kubernetes, use one of: 'openshift', 'internal', 'unsecured' (default "internal").
          On Podman, use one of: 'internal', 'unsecured' (default "internal")
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"internal"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_console_ingress"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_console_ingress:

      .. rst-class:: ansible-option-title

      **skupper_init_console_ingress**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_console_ingress" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Determines if/how console is exposed outside cluster. If not specified uses value of --ingress.
          One of: [route|loadbalancer|nodeport|nginx-ingress-v1|contour-http-proxy|ingress|none].
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_console_password"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_console_password:

      .. rst-class:: ansible-option-title

      **skupper_init_console_password**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_console_password" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Skupper console password. Valid only when --console-auth=internal


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_console_user"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_console_user:

      .. rst-class:: ansible-option-title

      **skupper_init_console_user**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_console_user" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Skupper console user. Valid only when --console-auth=internal


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"admin"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_container_network"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_container_network:

      .. rst-class:: ansible-option-title

      **skupper_init_container_network**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_container_network" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Container network name to be used.
          This argument is only used when \ :literal:`skupper\_option\_platform=podman`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"skupper"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_controller_cpu"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_controller_cpu:

      .. rst-class:: ansible-option-title

      **skupper_init_controller_cpu**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_controller_cpu" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      CPU request for controller pods.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_controller_cpu_limit"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_controller_cpu_limit:

      .. rst-class:: ansible-option-title

      **skupper_init_controller_cpu_limit**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_controller_cpu_limit" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      CPU limit for controller pods.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_controller_ingress_host"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_controller_ingress_host:

      .. rst-class:: ansible-option-title

      **skupper_init_controller_ingress_host**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_controller_ingress_host" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Host through which node is accessible when using nodeport as ingress.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_controller_load_balancer_ip"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_controller_load_balancer_ip:

      .. rst-class:: ansible-option-title

      **skupper_init_controller_load_balancer_ip**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_controller_load_balancer_ip" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Load balancer ip that will be used for controller service, if supported by cloud provider.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_controller_memory"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_controller_memory:

      .. rst-class:: ansible-option-title

      **skupper_init_controller_memory**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_controller_memory" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Memory request for controller pods.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_controller_memory_limit"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_controller_memory_limit:

      .. rst-class:: ansible-option-title

      **skupper_init_controller_memory_limit**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_controller_memory_limit" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Memory limit for controller pods.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_controller_node_selector"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_controller_node_selector:

      .. rst-class:: ansible-option-title

      **skupper_init_controller_node_selector**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_controller_node_selector" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Node selector to control placement of controller pods.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_controller_pod_affinity"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_controller_pod_affinity:

      .. rst-class:: ansible-option-title

      **skupper_init_controller_pod_affinity**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_controller_pod_affinity" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Pod affinity label matches to control placement of controller pods.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_controller_pod_antiaffinity"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_controller_pod_antiaffinity:

      .. rst-class:: ansible-option-title

      **skupper_init_controller_pod_antiaffinity**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_controller_pod_antiaffinity" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Pod antiaffinity label matches to control placement of controller pods.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_controller_service_annotations"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_controller_service_annotations:

      .. rst-class:: ansible-option-title

      **skupper_init_controller_service_annotations**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_controller_service_annotations" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Annotations to add to skupper controller service.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_create_network_policy"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_create_network_policy:

      .. rst-class:: ansible-option-title

      **skupper_init_create_network_policy**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_create_network_policy" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Create network policy to restrict access to skupper services exposed through this site to current pods in namespace.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_enable_cluster_permissions"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_enable_cluster_permissions:

      .. rst-class:: ansible-option-title

      **skupper_init_enable_cluster_permissions**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_enable_cluster_permissions" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enable cluster wide permissions in order to expose deployments.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_enable_console"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_enable_console:

      .. rst-class:: ansible-option-title

      **skupper_init_enable_console**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_enable_console" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enable skupper console must be used in conjunction with '--enable-flow-collector' flag


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_enable_flow_collector"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_enable_flow_collector:

      .. rst-class:: ansible-option-title

      **skupper_init_enable_flow_collector**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_enable_flow_collector" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enable cross-site flow collection for the application network


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_enable_ipv6"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_enable_ipv6:

      .. rst-class:: ansible-option-title

      **skupper_init_enable_ipv6**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_enable_ipv6" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enable IPV6 on the container network to be created (ignored when using an existing container network)


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_enable_rest_api"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_enable_rest_api:

      .. rst-class:: ansible-option-title

      **skupper_init_enable_rest_api**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_enable_rest_api" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enable REST API.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_enable_service_sync"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_enable_service_sync:

      .. rst-class:: ansible-option-title

      **skupper_init_enable_service_sync**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_enable_service_sync" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Participate in cross-site service synchronization.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry-default:`false` :ansible-option-choices-default-mark:`← (default)`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_enable_skupper_events"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_enable_skupper_events:

      .. rst-class:: ansible-option-title

      **skupper_init_enable_skupper_events**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_enable_skupper_events" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enable sending Skupper events to Kubernetes.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry-default:`true` :ansible-option-choices-default-mark:`← (default)`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_flow_collector_cpu"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_flow_collector_cpu:

      .. rst-class:: ansible-option-title

      **skupper_init_flow_collector_cpu**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_flow_collector_cpu" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      CPU request for flow collector pods.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_flow_collector_cpu_limit"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_flow_collector_cpu_limit:

      .. rst-class:: ansible-option-title

      **skupper_init_flow_collector_cpu_limit**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_flow_collector_cpu_limit" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      CPU limit for flow collector pods.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_flow_collector_memory"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_flow_collector_memory:

      .. rst-class:: ansible-option-title

      **skupper_init_flow_collector_memory**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_flow_collector_memory" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Memory request for flow collector pods.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_flow_collector_memory_limit"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_flow_collector_memory_limit:

      .. rst-class:: ansible-option-title

      **skupper_init_flow_collector_memory_limit**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_flow_collector_memory_limit" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Memory limit for flow collector pods.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_flow_collector_record_ttl"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_flow_collector_record_ttl:

      .. rst-class:: ansible-option-title

      **skupper_init_flow_collector_record_ttl**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_flow_collector_record_ttl" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Time after which terminated flow records are deleted, i.e. those flow records that have an end time set.
          Default is 15 minutes (duration format).
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"15m"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_ingress"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_ingress:

      .. rst-class:: ansible-option-title

      **skupper_init_ingress**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_ingress" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Ingress types varies based on target platform.
          On Kubernetes:
          You can use one of: [route|loadbalancer|nodeport|nginx-ingress-v1|contour-http-proxy|ingress|none].
          If not specified route is used when available, otherwise loadbalancer is used.
          On Podman:
          You can use one of: [external|none].
          Default is set to external if not provided.
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_ingress_annotations"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_ingress_annotations:

      .. rst-class:: ansible-option-title

      **skupper_init_ingress_annotations**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_ingress_annotations" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Annotations to add to skupper ingress.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_ingress_bind_ips"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_ingress_bind_ips:

      .. rst-class:: ansible-option-title

      **skupper_init_ingress_bind_ips**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_ingress_bind_ips" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      IP addresses in the host machines that will be bound to the inter-router and edge ports.
          This argument is only used when \ :literal:`skupper\_option\_platform=podman`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`[]`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_ingress_host"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_ingress_host:

      .. rst-class:: ansible-option-title

      **skupper_init_ingress_host**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_ingress_host" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Hostname or alias by which the ingress route or proxy can be reached.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_ingress_hosts"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_ingress_hosts:

      .. rst-class:: ansible-option-title

      **skupper_init_ingress_hosts**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_ingress_hosts" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Hostname or alias by which the ingress route or proxy can be reached.
          Tokens can only be generated for addresses provided through ingress-hosts.
          This argument is only used when \ :literal:`skupper\_option\_platform=podman`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`[]`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_labels"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_labels:

      .. rst-class:: ansible-option-title

      **skupper_init_labels**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_labels" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Labels to add to resources created by Skupper


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_podman_endpoint"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_podman_endpoint:

      .. rst-class:: ansible-option-title

      **skupper_init_podman_endpoint**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_podman_endpoint" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Local podman endpoint to use.
          This argument is only used when \ :literal:`skupper\_option\_platform=podman`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_prometheus_cpu"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_prometheus_cpu:

      .. rst-class:: ansible-option-title

      **skupper_init_prometheus_cpu**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_prometheus_cpu" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      CPU request for prometheus pods.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_prometheus_cpu_limit"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_prometheus_cpu_limit:

      .. rst-class:: ansible-option-title

      **skupper_init_prometheus_cpu_limit**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_prometheus_cpu_limit" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      CPU limit for prometheus pods.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_prometheus_memory"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_prometheus_memory:

      .. rst-class:: ansible-option-title

      **skupper_init_prometheus_memory**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_prometheus_memory" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Memory request for prometheus pods.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_prometheus_memory_limit"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_prometheus_memory_limit:

      .. rst-class:: ansible-option-title

      **skupper_init_prometheus_memory_limit**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_prometheus_memory_limit" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Memory limit for prometheus pods.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_router_cpu"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_router_cpu:

      .. rst-class:: ansible-option-title

      **skupper_init_router_cpu**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_router_cpu" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      CPU request for router pods.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_router_cpu_limit"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_router_cpu_limit:

      .. rst-class:: ansible-option-title

      **skupper_init_router_cpu_limit**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_router_cpu_limit" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      CPU limit for router pods.
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_router_ingress_host"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_router_ingress_host:

      .. rst-class:: ansible-option-title

      **skupper_init_router_ingress_host**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_router_ingress_host" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Host through which node is accessible when using nodeport as ingress.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_router_load_balancer_ip"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_router_load_balancer_ip:

      .. rst-class:: ansible-option-title

      **skupper_init_router_load_balancer_ip**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_router_load_balancer_ip" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Load balancer ip that will be used for router service, if supported by cloud provider.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_router_logging"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_router_logging:

      .. rst-class:: ansible-option-title

      **skupper_init_router_logging**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_router_logging" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Logging settings for router. 'trace', 'debug', 'info' (default), 'notice', 'warning', and 'error' are valid values.
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"info"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_router_memory"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_router_memory:

      .. rst-class:: ansible-option-title

      **skupper_init_router_memory**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_router_memory" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Memory request for router pods
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_router_memory_limit"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_router_memory_limit:

      .. rst-class:: ansible-option-title

      **skupper_init_router_memory_limit**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_router_memory_limit" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Memory limit for router pods.
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_router_mode"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_router_mode:

      .. rst-class:: ansible-option-title

      **skupper_init_router_mode**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_router_mode" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Router mode, one of: [interior, edge (only kubernetes)].
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"interior"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_router_node_selector"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_router_node_selector:

      .. rst-class:: ansible-option-title

      **skupper_init_router_node_selector**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_router_node_selector" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Node selector to control placement of router pods.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_router_pod_affinity"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_router_pod_affinity:

      .. rst-class:: ansible-option-title

      **skupper_init_router_pod_affinity**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_router_pod_affinity" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Pod affinity label matches to control placement of router pods.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_router_pod_antiaffinity"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_router_pod_antiaffinity:

      .. rst-class:: ansible-option-title

      **skupper_init_router_pod_antiaffinity**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_router_pod_antiaffinity" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Pod antiaffinity label matches to control placement of router pods.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_router_service_annotations"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_router_service_annotations:

      .. rst-class:: ansible-option-title

      **skupper_init_router_service_annotations**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_router_service_annotations" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Annotations to add to skupper router service.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_routers"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_routers:

      .. rst-class:: ansible-option-title

      **skupper_init_routers**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_routers" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Number of router replicas to start.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`1`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_service_sync_site_ttl"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_service_sync_site_ttl:

      .. rst-class:: ansible-option-title

      **skupper_init_service_sync_site_ttl**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_service_sync_site_ttl" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Time after which stale services, i.e. those whose site has not been heard from, created through service-sync are removed.
          Duration format.
          This argument is only used when \ :literal:`skupper\_option\_platform=kubernetes`\ .
          


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"0"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_site_name"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_site_name:

      .. rst-class:: ansible-option-title

      **skupper_init_site_name**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_site_name" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A specific name for this skupper installation


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`""`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-main--skupper_init_timeout"></div>

      .. _ansible_collections.skupper.core.skupper_init_role__parameter-main__skupper_init_timeout:

      .. rst-class:: ansible-option-title

      **skupper_init_timeout**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-main--skupper_init_timeout" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      :ansible-option-versionadded:`added in skupper.core 1.6.0`





      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Configurable timeout for site initialization (using duration format)


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"2m"`

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

