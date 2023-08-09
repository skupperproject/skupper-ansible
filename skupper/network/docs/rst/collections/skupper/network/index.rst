


.. _plugins_in_skupper.network:

Skupper.Network
===============

Collection version 1.1.3

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

.. raw:: html

  <p class="ansible-links">
    <a href="http://github.com/skupperproject/skupper-ansible/issues" aria-role="button" target="_blank" rel="noopener external">Issue Tracker</a>
    <a href="http://skupper.io" aria-role="button" target="_blank" rel="noopener external">Homepage</a>
    <a href="http://github.com/skupperproject/skupper-ansible" aria-role="button" target="_blank" rel="noopener external">Repository (Sources)</a>
  </p>



.. toctree::
    :maxdepth: 1


Plugin Index
------------

These are the plugins in the skupper.network collection:


Modules
~~~~~~~

* :ansplugin:`links module <skupper.network.links#module>` -- Update links based on provided links list
* :ansplugin:`links_load module <skupper.network.links_load#module>` -- Loads existing links to other sites
* :ansplugin:`services module <skupper.network.services#module>` -- Update services based on provided services list
* :ansplugin:`services_load module <skupper.network.services_load#module>` -- Loads existing services and targets
* :ansplugin:`site_load module <skupper.network.site_load#module>` -- Loads site information as ansible facts into the respective host

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
