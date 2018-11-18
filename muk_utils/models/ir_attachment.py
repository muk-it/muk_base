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

import base64
import logging
import mimetypes

from odoo import api, models, _
from odoo.exceptions import AccessError
from odoo.tools.mimetypes import guess_mimetype

_logger = logging.getLogger(__name__)

class Attachment(models.Model):
    
    _inherit = 'ir.attachment'
    
    #----------------------------------------------------------
    # Functions
    #----------------------------------------------------------
    
    @api.model
    def storage_locations(self):
        return ['db', 'file']
    
    @api.model
    def force_storage(self):
        if not self.env.user._is_admin():
            raise AccessError(_('Only administrators can execute this action.'))
        storage_domain = {
            'db': ('db_datas', '=', False),
            'file': ('store_fname', '=', False), 
        }
        record_domain = [
            '&', storage_domain[self._storage()], 
            '|', ('res_field', '=', False), ('res_field', '!=', False)
        ]
        self.search(record_domain).migrate()
        return True
    
    @api.multi
    def migrate(self):
        record_count = len(self)
        storage = self._storage().upper()
        for index, attach in enumerate(self):
            _logger.info(_("Migrate Attachment %s of %s to %s") % (index + 1, record_count, storage))
            attach.with_context(migration=True).write({'datas': attach.datas})
            
    #----------------------------------------------------------
    # Read
    #----------------------------------------------------------
    
    def _compute_mimetype(self, values):
        if self.env.context.get('migration') and len(self) == 1:
            return self.mimetype or 'application/octet-stream'
        else:
            return super(Attachment, self)._compute_mimetype(values)
        