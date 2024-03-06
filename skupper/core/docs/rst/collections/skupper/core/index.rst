

.. meta::
  :antsibull-docs: 2.7.0


.. _plugins_in_skupper.core:

Skupper.Core
============

Collection version 1.6.0

.. contents::
   :local:
   :depth: 1

Description
-----------

Provides roles to help managing Skupper sites

**Author:**

* Fernando Giorgetti <fgiorgetti@gmail.com>

**Supported ansible-core versions:**

* 2.14.0 or newer

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




.. toctree::
    :maxdepth: 1


Plugin Index
------------

These are the plugins in the skupper.core collection:


Modules
~~~~~~~

* :ansplugin:`links module <skupper.core.links#module>` -- Update links based on provided links list
* :ansplugin:`links_load module <skupper.core.links_load#module>` -- Loads existing links to other sites
* :ansplugin:`services module <skupper.core.services#module>` -- Update services based on provided services list
* :ansplugin:`services_load module <skupper.core.services_load#module>` -- Loads existing services and targets
* :ansplugin:`site_load module <skupper.core.site_load#module>` -- Loads site information as ansible facts into the respective host

.. toctree::
    :maxdepth: 1
    :hidden:

    links_module
    links_load_module
    services_module
    services_load_module
    site_load_module


Role Index
----------

These are the roles in the skupper.core collection:

* :ansplugin:`skupper_cli_install role <skupper.core.skupper_cli_install#role>` -- Installs the Skupper CLI
* :ansplugin:`skupper_delete role <skupper.core.skupper_delete#role>` -- Deletes a Skupper site
* :ansplugin:`skupper_init role <skupper.core.skupper_init#role>` -- Initializes a Skupper site
* :ansplugin:`skupper_link role <skupper.core.skupper_link#role>` -- Maintains existing links on a site
* :ansplugin:`skupper_option role <skupper.core.skupper_option#role>` -- Provides common parameters to be used across the skupper.core roles.
* :ansplugin:`skupper_token role <skupper.core.skupper_token#role>` -- Creates a Skupper token that can be used by other sites to establish links
* :ansplugin:`skupper_update role <skupper.core.skupper_update#role>` -- Updates a Skupper site

.. toctree::
    :maxdepth: 1
    :hidden:

    skupper_cli_install_role
    skupper_delete_role
    skupper_init_role
    skupper_link_role
    skupper_option_role
    skupper_token_role
    skupper_update_role


.. seealso::

    List of :ref:`collections <list_of_collections>` with docs hosted here.
