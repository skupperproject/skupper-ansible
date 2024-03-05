

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



.. seealso::

    List of :ref:`collections <list_of_collections>` with docs hosted here.
