###################################################################################
#
#    Copyright (C) 2017 MuK IT GmbH
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
import base64
import uuid
import logging
import mimetypes

from odoo import _, api, fields, models

from odoo.addons.muk_utils.tools.http import get_response
from odoo.addons.muk_converter.tools import converter

_logger = logging.getLogger(__name__)

class ConverterWizard(models.TransientModel):
    
    _name = "muk_converter.convert"
    
    state = fields.Selection(
        selection=[("export", "Export"), ("download", "Download")],
        string="State",
        required=True,
        default="export")
    
    type = fields.Selection(
        selection=[("url", "URL"), ("binary", "File")],
        string="Type",
        default="binary", 
        change_default=True,
        states={'export': [('required', True)]},
        help="Either a binary file or an url can be converted")
    
    input_url = fields.Char(
        string="Url")
     
    input_name = fields.Char(
        string="Filename")
    
    input_binary = fields.Binary(
        string="File")
    
    format = fields.Selection(
        selection=converter.selection_formats(),
        string="Format",
        default="pdf",
        states={'export': [('required', True)]})
    
    output_name = fields.Char(
        string="Filename",
        readonly=True,
        states={'download': [('required', True)]})
    
    output_binary = fields.Binary(
        string="File",
        readonly=True,
        states={'download': [('required', True)]})
    
    @api.multi
    def convert(self):
        def export(record, content, filename):
            name = "%s.%s" % (os.path.splitext(filename)[0], record.format)
            output = record.env['muk_converter.converter'].convert(filename, content)
            record.write({
                'state': 'download',
                'output_name': name,
                'output_binary': base64.b64encode(output)})
            return {
                "name": _("Convert File"),
                'type': 'ir.actions.act_window',
                'res_model': 'muk_converter.convert',
                'view_mode': 'form',
                'view_type': 'form',
                'res_id': record.id,
                'views': [(False, 'form')],
                'target': 'new',
            }
        record = self[0]
        if record.input_url:
            status, headers, content = get_response(record.input_url)
            if status != 200:
                raise ValueError("Failed to retrieve the file from the url.")
            else:
                extension = mimetypes.guess_extension(headers['content-type'])[1:].strip().lower()
                if extension not in converter.imports():
                    raise ValueError("Invalid import format.")
                else:
                    return export(record, content, record.input_name or "%s.%s" % (uuid.uuid4(), extension))
        elif record.input_name and record.input_binary:
            return export(record, base64.b64decode(record.input_binary), record.input_name)
        else:
            raise ValueError("The conversion requires either a valid url or a filename and a file.") 