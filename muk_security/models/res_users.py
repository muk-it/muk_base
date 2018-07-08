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

from odoo.addons.base.res import res_users

from odoo.addons.muk_security.tools import helper

_logger = logging.getLogger(__name__)

class AccessUser(models.Model):
    
    _inherit = 'res.users'

    #----------------------------------------------------------
    # Database
    #----------------------------------------------------------
    
    security_groups = fields.Many2many(
        comodel_name='muk_security.groups',
        relation='muk_security_groups_explicit_users_rel',
        column1='uid',
        column2='gid',
        string='Groups',
        readonly=True)

    #----------------------------------------------------------
    # Functions
    #----------------------------------------------------------
    
    @classmethod
    def _browse(cls, ids, env, prefetch=None):
        return super(AccessUser, cls)._browse([
            id if not isinstance(id, helper.NoSecurityUid)
            else super(helper.NoSecurityUid, id).__int__() 
            for id in ids], env, prefetch=prefetch)