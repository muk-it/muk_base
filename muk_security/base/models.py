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

from odoo import models, api, SUPERUSER_ID

from odoo.addons.muk_utils.tools import patch
from odoo.addons.muk_security.tools import helper

_logger = logging.getLogger(__name__)

@api.model
def suspend_security(self, user=None):
    return self.sudo(user=helper.NoSecurityUid(user or self.env.uid))

models.BaseModel.suspend_security = suspend_security

@api.model
@patch.monkey_patch_model(models.BaseModel)
def check_field_access_rights(self, operation, fields):    
    if isinstance(self.env.uid, helper.NoSecurityUid):
        return fields or list(self._fields)
    return check_field_access_rights.super(self, operation, fields)