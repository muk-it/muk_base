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

import logging

from odoo import tools

from odoo.addons.muk_converter.service.unoconv import unoconv

_logger = logging.getLogger(__name__)

def formats():
    return unoconv.formats

def selection_formats():
    return list(map(lambda format: (format, format.upper()), unoconv.formats))

def imports():
    return unoconv.imports

def convert(filename, content, format):
    return unoconv.convert(content, filename=filename, format=format)

def convert2pdf(filename, content):
    return unoconv.convert(content, filename=filename, format="pdf")
    
def convert2html(filename, content):
    output = unoconv.convert(content, filename=filename, format="html")
    return tools.html_sanitize(output)