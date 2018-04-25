=======================
MuK Large Objects Field
=======================

PostgreSQL offers support for large objects, which provide stream-style access
to user data that is stored in a special large-object structure. They are useful
with data values too large to be manipulated conveniently as a whole.

Psycopg allows access to the large object using the `lobject` class. Objects are
generated using the `connection.lobject()` factory method. Data can be retrieved
either as bytes or as Unicode strings.

Psycopg large object support efficient import/export with file system files using
the `lo_import()` and `lo_export()` libpq functions.

Changed in version 2.6: added support for large objects greated than 2GB. Note
that the support is enabled only if all the following conditions are verified:

* the Python build is 64 bits;
* the extension was built against at least libpq 9.3;
* the server version is at least PostgreSQL 9.3 (server_version must be >= 90300).

If Psycopg was built with 64 bits large objects support (i.e. the first two
contidions above are verified), the `psycopg2.__version__` constant will contain
the lo64 flag. If any of the contition is not met several lobject methods will
fail if the arguments exceed 2GB.

Installation
============

To install this module, you need to:

Download the module and add it to your Odoo addons folder. Afterward, log on to
your Odoo server and go to the Apps menu. Trigger the debug modus and update the
list by clicking on the "Update Apps List" link. Now install the module by
clicking on the install button.

Configuration
=============

No additional configuration is needed to use this module.

Usage
=============

This module has no direct visible effect on the system. It adds a new field type,
which can be used in other modules.

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
