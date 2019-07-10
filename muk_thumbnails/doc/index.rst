==============
MuK Thumbnails
==============

Technical module to provide some utility features and libraries that can be used
in other applications. This module has no direct effect on the running system.

Requirements
=============

Unoconv
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

FFmpeg 
-------------

FFmpeg is a complete, cross-platform solution to record, convert and stream audio and video.

To install FFmpeg please follow the instructions (`here <https://www.ffmpeg.org/download.html>`_).

Ghostscript  
-------------

Ghostscript is a suite of software based on an interpreter for Adobe Systems PostScript and
Portable Document Format (PDF) page description languages. Its main purposes are the
rasterization or rendering of such page description language files, for the display or printing
of document pages, and the conversion between PostScript and PDF files.

To install Ghostscript please follow the instructions (`here <https://www.ghostscript.com/download.html>`_).

ImageMagick 
-------------

ImageMagick can be used to create, edit, compose, or convert bitmap images. It can read and write
images in a variety of formats (over 200) including PNG, JPEG, GIF, HEIC, TIFF, DPX, EXR, WebP,
Postscript, PDF, and SVG. Use ImageMagick to resize, flip, mirror, rotate, distort, shear and
transform images, adjust image colors, apply various special effects, or draw text, lines, polygons,
ellipses and Bezier curves.

To install ImageMagick please follow the instructions (`here <https://www.imagemagick.org/script/download.php>`_).

Wand 
-------------

Wand is a ctypes-based simple ImageMagick binding for Python. It is used to interact with ImageMagick via a Python interface.

To install Wand please follow the instructions (`here <http://docs.wand-py.org/en/0.4.1/guide/install.html>`_).

Imageio 
-------------

Imageio is a Python library that provides an easy interface to read and write a wide range of image data, including animated images, volumetric data, and scientific formats.

To install Imageio please follow the instructions (`here <https://pypi.org/project/imageio/>`_).

MoviePy 
-------------

MoviePy is a Python module for video editing, which can be used for basic operations (like cuts, concatenations, title insertions), video compositing (a.k.a. non-linear editing), video processing, or to create advanced effects. It can read and write the most common video formats, including GIF.

To install MoviePy please follow the instructions (`here <https://zulko.github.io/moviepy/install.html>`_).

Installation
============

To install this module, you need to:

Download the module and add it to your Odoo addons folder. Afterward, log on to
your Odoo server and go to the Apps menu. Trigger the debug mode and update the
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

Once the installation has been successfully completed, the app is already in the
correct folder. Log on to your Odoo server and go to the Apps menu. Trigger the 
debug mode and update the list by clicking on the "Update Apps List" link. Now
install the module by clicking on the install button.

The biggest advantage of this variant is that you can now also update the app
using the "pip" command. To do this, enter the following command in your console:

``pip install --upgrade --extra-index-url https://nexus.mukit.at/repository/odoo/simple <module>``

When the process is finished, restart your server and update the application in 
Odoo. The steps are the same as for the installation only the button has changed
from "Install" to "Upgrade".

You can also view available Apps directly in our `repository <https://nexus.mukit.at/#browse/browse:odoo>`_
and find a more detailed installation guide on our `website <https://mukit.at/page/open-source>`_.

For modules licensed under OPL-1, you will receive access data when you purchase
the module. If the modules were not purchased directly from
`MuK IT <https://www.mukit.at/>`_ please contact our support (support@mukit.at)
with a confirmation of purchase to receive the corresponding access data.

Upgrade
============

To upgrade this module, you need to:

Download the module and add it to your Odoo addons folder. Restart the server
and log on to your Odoo server. Select the Apps menu and upgrade the module by
clicking on the upgrade button.

If you installed the module using the "pip" command, you can also update the
module in the same way. Just type the following command into the console:

``pip install --upgrade --extra-index-url https://nexus.mukit.at/repository/odoo/simple <module>``

When the process is finished, restart your server and update the application in 
Odoo, just like you would normally.

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
