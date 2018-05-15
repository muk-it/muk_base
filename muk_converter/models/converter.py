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

import hashlib
import logging

from odoo import api, models, fields

from odoo.addons.muk_converter.tools import converter

_logger = logging.getLogger(__name__)

class Converter(models.AbstractModel):
    
    _name = 'muk_converter.converter'
    _description = 'Converter'

    @api.model
    def convert(self, filename, content, format="pdf", recompute=False):
        def parse(filename, content, format):
            return converter.convert(filename, content, format)
        def store(checksum, filename, content, format, stored):
            if not stored.exists():
                self.env['muk_converter.store'].sudo().create({
                    'checksum': checksum,
                    'format': format,
                    'content_fname': filename,
                    'content': content})
            else:
                stored.write({'used_date': fields.Datetime.now})
        checksum = hashlib.sha1(content).hexdigest()
        stored = self.env['muk_converter.store'].sudo().search(
            [["checksum", "=", checksum], ["format", "=", format]], limit=1)
        if not recompute and stored.exists():
            return stored.content
        else: 
            output = parse(filename, content, format)
            name = "%s.%s" % (filename, format)
            store(checksum, name, output, format, stored)
            return output
   