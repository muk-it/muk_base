###################################################################################
# 
#    Copyright (C) 2018 MuK IT GmbH
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###################################################################################

import os
import io
import sys
import PyPDF2
import base64
import shutil
import urllib
import logging
import tempfile
import mimetypes

from contextlib import closing

from odoo.tools import config
from odoo.tools.mimetypes import guess_mimetype

from odoo.addons.muk_utils.tools import utils_os
from odoo.addons.muk_converter.service import unoconv

_logger = logging.getLogger(__name__)

try:
    from wand.image import Image
    from wand.color import Color
except ImportError:
    Image = False
    Color = False
    _logger.warn('Cannot `import wand`.')
    
try:
    import imageio
except ImportError:
    imageio = False
    _logger.warn('Cannot `import imageio`.')

try:
    from moviepy.editor import VideoFileClip
except ImportError:
    VideoFileClip = False
    _logger.warn('Cannot `import moviepy`.')

FORMATS = [
    "png", "jpg", "jepg"
]

VIDEO_IMPORTS = [
    "mp4", "mov", "wav", "avi", "mpg", "flv", "wmv", "webm"
]

PDF_IMPORTS = [
    "pdf"
]

WAND_IMPORTS = [
    "aai", "art", "arw", "avi", "avs", "bpg", "brf", "cals", "cgm", "cin", "cip", "cmyk", "cmyka", "svg",
    "cr2", "crw", "cur", "cut", "dcm", "dcr", "dcx", "dds", "dib", "djvu", "dng", "dot", "dpx", "tim",
    "emf", "epdf", "epi", "eps", "eps2", "eps3", "epsf", "epsi", "ept", "exr", "fax", "fig", "fits", 
    "fpx", "gplt", "gray", "graya", "hdr", "hdr", "heic", "hpgl", "hrz", "html", "ico", "info", "ttf",
    "inline", "isobrl", "isobrl6", "jbig", "jng", "jp2", "jpt", "j2c", "j2k", "jxr", "json", "man", "bmp", 
    "mat", "miff", "mono", "mng", "m2v", "mpeg", "mpc", "mpr", "mrw", "msl", "mtv", "mvg", "nef", "yuv",
    "orf", "otb", "p7", "palm", "pam", "clipboard", "pbm", "pcd", "pcds", "pcl", "pcx", "pdb", "jpe",
    "pef", "pes", "pfa", "pfb", "pfm", "pgm", "picon", "pict", "pix", "png8", "png00", "png24", "tiff", 
    "png32", "png48", "png64", "pnm", "ppm", "ps", "ps2", "ps3", "psb", "psd", "ptif", "pwp", "rad", 
    "raf", "rgb", "rgba", "rgf", "rla", "rle", "sct", "sfw", "sgi", "shtml", "sid", " mrsid", "jpeg", 
    "sparse-color", "sun", "tga", "ubrl", "ubrl6", "uyvy", "vicar", "viff", "wbmp", "jpg", "png", "uil", 
    "wdp", "webp", "wmf", "wpg", "x", "xbm", "xcf", "xpm", "xwd", "x3f", "ycbcr", "ycbcra", "bmp3", "bmp2",
]

def formats():
    return FORMATS

def imports():
    return VIDEO_IMPORTS + PDF_IMPORTS + WAND_IMPORTS + unoconv.UNOCONV_IMPORTS

def create_thumbnail(binary, mimetype=None, filename=None, export="binary", format="png", page=0, frame=0,
                     animation=False, video_resize={'width': 256}, image_resize='256x256>', image_crop=None):
    """
    Converts a thumbnail for a given file.
    
    :param binary: The binary value.
    :param mimetype: The mimetype of the binary value.
    :param filename: The filename of the binary value.
    :param export: The output format (binary, file, base64).
    :param format: Specify the output format for the document.
    :param page: Specifies the page if the file has several pages, e.g. if it is a PDF file.
    :param frame: Specifies the frame if the file has several frames, e.g. if it is a video file.
    :param animation: In this case, the parameter frame specifies the number of frames.
    :param video_resize: Specify to resize the output image.
    :param image_resize: Specify to resize the output image.
    :param image_crop: Specify to crop the output image.
    :return: Returns the output depending on the given format.
    :raises ValueError: The file extension could not be determined or the format is invalid.
    """
    extension = utils_os.get_extension(binary, filename, mimetype)
    if not extension:
        raise ValueError("The file extension could not be determined.")
    if format not in FORMATS:
        raise ValueError("Invalid export format.")
    if extension not in (VIDEO_IMPORTS + PDF_IMPORTS + WAND_IMPORTS + unoconv.UNOCONV_IMPORTS):
        raise ValueError("Invalid import format.")
    if not imageio or not Image or not VideoFileClip:
        raise ValueError("Some libraries couldn't be imported.")
    image_data = None
    image_extension = extension
    if extension in WAND_IMPORTS:
        image_data = binary
    elif not image_data and (extension in PDF_IMPORTS or extension in unoconv.UNOCONV_IMPORTS):
        pdf_data = binary if extension in PDF_IMPORTS else None
        if not pdf_data:
            image_extension = "pdf"
            pdf_data = unoconv.unoconv.convert(binary, mimetype, filename)
        reader = PyPDF2.PdfFileReader(io.BytesIO(pdf_data))
        writer = PyPDF2.PdfFileWriter()
        if reader.getNumPages() >= page:
            writer.addPage(reader.getPage(page))
        else:
            writer.addPage(reader.getPage(0))
        pdf_bytes = io.BytesIO()
        writer.write(pdf_bytes)
        image_data = pdf_bytes.getvalue()
    if image_data:
        with Image(blob=image_data, format=image_extension) as thumbnail:
            thumbnail.format = format
            if image_extension == "pdf":
                thumbnail.background_color = Color('white')
                thumbnail.alpha_channel = 'remove'
            if image_resize:
                thumbnail.transform(resize=image_resize)
            if image_crop:
                thumbnail.transform(crop=image_crop)
            if export == 'file':
                return io.BytesIO(thumbnail.make_blob())
            elif export == 'base64':
                return base64.b64encode(thumbnail.make_blob())
            else:
                return thumbnail.make_blob()
    elif extension in VIDEO_IMPORTS:
        tmp_dir = tempfile.mkdtemp()
        try:
            tmp_wpath = os.path.join(tmp_dir, "tmpfile.%s" % extension)
            if os.name == 'nt':
                tmp_wpath = tmp_wpath.replace("\\", "/")
            with closing(open(tmp_wpath, 'wb')) as file:
                file.write(binary)
            clip = VideoFileClip(tmp_wpath)
            try:
                tmp_opath = os.path.join(tmp_dir, "output.%s" % format)
                clip.resize(**video_resize)
                if animation:
                    files = []
                    current_frame = 0
                    while clip.duration > current_frame and current_frame < frame:
                        filename = os.path.join(tmp_dir, "output_%s.png" % frame)
                        clip.save_frame(filename, t=frame)
                        files.append(filename)
                        frame += 0.25
                    tmp_opath = os.path.join(tmp_dir, "output.gif")
                    with imageio.get_writer(tmp_opath, fps=5, mode='I') as writer:
                        for filename in files:
                            image = imageio.imread(filename)
                            writer.append_data(image)
                elif clip.duration > int(frame):
                    clip.save_frame(tmp_opath, t=int(frame))
                else:
                    clip.save_frame(tmp_opath, t=int(0))
                if os.path.isfile(tmp_opath):
                    with open(tmp_opath, 'rb') as file:
                        if export == 'file':
                            return io.BytesIO(file.read())
                        elif export == 'base64':
                            return base64.b64encode(file.read())
                        else:
                            return file.read()
                else:
                    raise ValueError("No output could be created from the video.")
            finally:
                try:
                    clip.reader.close()
                    del clip.reader
                    if clip.audio != None:
                        clip.audio.reader.close_proc()
                        del clip.audio
                    del clip
                except Exception as e:
                    sys.exc_clear()
        finally:
            try:
                shutil.rmtree(tmp_dir)
            except PermissionError:
                _logger.warn("Temporary directory could not be deleted.")
    else:
        raise ValueError("No output could be generated.")
