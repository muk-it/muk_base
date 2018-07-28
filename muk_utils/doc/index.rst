=========
MuK Utils
=========

Technical module to provide some utility features and libraries that can be used
in other applications. This module has no direct effect on the running system.

Installation
============

To install this module, you need to:

Download the module and add it to your Odoo addons folder. Afterward, log on to
your Odoo server and go to the Apps menu. Trigger the debug modus and update the
list by clicking on the "Update Apps List" link. Now install the module by
clicking on the install button.

Another way to install this module is via the package management for Python
(`PyPI <https://pypi.org/project/pip/>`_).

To install our modules using the package manager make sure
`odoo-autodiscover <https://pypi.org/project/odoo-autodiscover/>`_ is installed
correctly. Then open a console and install the module by entering the following
command:

``pip install --extra-index-url https://nexus.mukit.at/repository/odoo/simple <module>``

The module name consists of the Odoo version and the module name, where
underscores are replaced by a dash.

**Module:** 

``odoo<version>-addon-<module_name>``

**Example:**

``sudo -H pip3 install --extra-index-url https://nexus.mukit.at/repository/odoo/simple odoo11-addon-muk-utils``

You can also view available Apps directly in our `repository <https://nexus.mukit.at/#browse/browse:odoo>`_
and find a more detailed installation guide on our `website <https://mukit.at/page/open-source>`_.

For modules licensed under OPL-1, you will receive access data when you purchase
the module. If the modules were not purchased directly from
`MuK IT <https://www.mukit.at/>`_ please contact our support (support@mukit.at)
with a confirmation of purchase to receive the corresponding access data.

Configuration
=============

No additional configuration is needed to use this module.

Usage
=============

This module has no direct visible effect on the system. It provide utility features.

Credits
=======

Contributors
------------

* Mathias Markl <mathias.markl@mukit.at>

Author & Maintainer
-------------------

This module is maintained by the `MuK IT GmbH <https://www.mukit.at/>`_.

MuK IT is an Austrian company specialized in customizing and extending Odoo.
We develop custom solutions for your individual needs to help you focus on
your strength and expertise to grow your business.

If you want to get in touch please contact us via mail
(sale@mukit.at) or visit our website (https://mukit.at).