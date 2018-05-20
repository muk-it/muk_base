.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3
   
.. image:: https://gitlab.mukit.at/base/muk_automation_extension/badges/11.0/pipeline.svg
   :target: https://gitlab.mukit.at/base/muk_automation_extension/commits/11.0
   :alt: Pipeline status
   
.. image:: https://gitlab.mukit.at/base/muk_automation_extension/badges/11.0/coverage.svg
   :target: https://gitlab.mukit.at/base/muk_automation_extension/commits/11.0
   :alt: Coverage report

========================
MuK Automation Extension
========================

Technical module to extend the Base Automation module. Another trigger is added,
which executes the action during creation, update and deletion.

Installation
============

To install this module, you need to:

Download the module and add it to your Odoo addons folder. Afterward, log on to
your Odoo server and go to the Apps menu. Trigger the debug modus and update the
list by clicking on the "Update Apps List" link. Now install the module by
clicking on the install button.

Configuration
=============

The converter uses a store to avoid the repeated conversion of the same file.
To avoid unnecessary memory consumption, Odoo's AutoVaccum Cron Job empties
the store accordingly. The system parameter ``muk_converter.max_store`` can
be used to set the maximum number of elements that can be in the store after
cleaning. By default, this value is set to 20.

Usage
=============

Another trigger can now be selected in the From View of Base Automation.

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
