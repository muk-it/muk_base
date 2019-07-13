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
from odoo.exceptions import UserError

from odoo.addons.muk_utils.tools.http import get_response

_logger = logging.getLogger(__name__)

class ConverterWizard(models.TransientModel):
    
    _name = "muk_converter.convert"
    
    #----------------------------------------------------------
    # Selections
    #----------------------------------------------------------
    
    def _format_selection(self):
        formats = self.env['muk_converter.converter'].formats()
        return list(map(lambda format: (format, format.upper()), formats))
    
    #----------------------------------------------------------
    # Database
    #----------------------------------------------------------
    
    state = fields.Selection(
        selection=[
            ("export", "Export"),
            ("download", "Download")],
        string="State",
        required=True,
        default="export")
     
    input_name = fields.Char(
        string="Filename",
        states={'export': [('required', True)]})
     
    input_url = fields.Char(
        string="URL")
    
    input_binary = fields.Binary(
        string="File")
    
    format = fields.Selection(
        selection=_format_selection,
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
    
    #----------------------------------------------------------
    # Functions
    #----------------------------------------------------------
    
    @api.multi
    def convert(self):
        self.ensure_one()

        if not self.input_url and not self.input_binary:
            raise UserError(_("Please choose a file to convert."))

        if self.input_url:
            status, headers, content = get_response(self.input_url)
            if status != 200:
                raise ValueError(_("Failed to retrieve the file from the url."))
            else:
                content = base64.b64encode(content)
        else:
            content = self.input_binary

        name = "%s.%s" % (os.path.splitext(self.input_name)[0], self.format)
        output = self.env['muk_converter.converter'].convert(self.input_name, content, format=self.format)
        self.write({
            'state': 'download',
            'output_name': name,
            'output_binary': output})
        return {
            "name": _("Convert File"),
            'type': 'ir.actions.act_window',
            'res_model': 'muk_converter.convert',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }