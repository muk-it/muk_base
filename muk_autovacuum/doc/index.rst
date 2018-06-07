==============
MuK Autovacuum
==============

Allows the administrator to create rules to automatically garbage collect
a certain model. Every rule can have a different time interval additional
constraints. An extra constraint can be for example to only delete inactive
records.

Installation
============

To install this module, you need to:

Download the module and add it to your Odoo addons folder. Afterward, log on to
your Odoo server and go to the Apps menu. Trigger the debug modus and update the
list by clicking on the "Update Apps List" link. Now install the module by
clicking on the install button.

Configuration
=============

To configure this module, you need to:

#. Go to *Settings* while being in debug mode.
#. Afterwards go to *Technical -> Automation -> Auto Vacuum Rules*.
#. And create a new rule.

Usage
=============

This module has no direct visible effect on the system. The garbage collections
happens during the autovacuum cron job.

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
