===================================
MuK Large Object Attachment Storage
===================================

Provides a new attachment location to save attachments as PostgreSQL large objects.
To enable the large object storage option change the `ir_attachment.location`
parameter to `lobject`.

**Advantages over the in-database storage**

* Better RAM efficiency (This is more important for large files than for small ones.)
* Possibility to easily dump the base without the large objects (This can be useful for reproducing bugs.)

**Advantages over the file system storage**

* Large objects are transactional (fully ACID)
* They work out of the box in multi-system setups (So there is no need for NFS or similar file sharing tools.)
* Enables you to easily create backups of the entire system


Installation
============

To install this module, you need to:

Download the module and add it to your Odoo addons folder. Afterward, log on to
your Odoo server and go to the Apps menu. Trigger the debug modus and update the
list by clicking on the "Update Apps List" link. Now install the module by
clicking on the install button.

Configuration
=============

The module has an init hook, which automatically stores all attachments in
large objects, so no additional configuration is needed to use this module.

Usage
=============

This module has no direct visible effect on the system. However, existing and
future attachments are stored as large objects.

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
