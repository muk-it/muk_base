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

import logging

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError

from odoo.addons.muk_security.tools.security import NoSecurityUid

_logger = logging.getLogger(__name__)

class AccessUser(models.Model):
    
    _inherit = 'res.users'

    #----------------------------------------------------------
    # Functions
    #----------------------------------------------------------
    
    @classmethod
    def _browse(cls, ids, *args, **kwargs):
        def convert_security_uid(id):
            if isinstance(id, NoSecurityUid):
                return super(NoSecurityUid, id).__int__()
            return id
        access_ids = [convert_security_uid(id) for id in ids]
        return super(AccessUser, cls)._browse(access_ids, *args, **kwargs)