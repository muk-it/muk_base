=============
MuK Converter
=============

Technical module to provide some utility features and libraries that can be used
in other applications. This module has no direct effect on the running system.

Requirements
=============

unoconv
-------------

Universal Office Converter (unoconv) is a command line tool to convert any
document format that LibreOffice can import to any document format that
LibreOffice can export. It makes use of the LibreOffice's UNO bindings for
non-interactive conversion of documents.

To install unoconv please follow the instructions (`here <https://github.com/dagwieers/unoconv>`_).

Make sure that unoconv can be executed from the console and the conversion 
is done correctly.

To set an individual path for the LibreOffice installation, the config
variable ``uno_path`` can be set accordingly in the Odoo config.

Under Windows you should rename the ``unoconv`` file to ``unoconv.py`` and set
the corresponding path for the ``uno_path`` variable. Since it does not work
reliably with the environment variable ``UNO_PATH``.

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

This module has no direct visible effect on the system. It provides functions
to convert data from one file format to another.

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