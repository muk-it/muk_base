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

from odoo.addons.muk_security.tools import helper

_logger = logging.getLogger(__name__)

class ExtendedIrModelAccess(models.Model):
    
    _inherit = 'ir.model.access'
    
    @api.model
    @tools.ormcache_context('self._uid', 'model', 'mode', 'raise_exception', keys=('lang',))
    def check(self, model, mode='read', raise_exception=True):
        if isinstance(self.env.uid, helper.NoSecurityUid):
            return True
        return super(ExtendedIrModelAccess, self).check(model, mode=mode, raise_exception=raise_exception)