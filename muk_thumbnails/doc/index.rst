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
