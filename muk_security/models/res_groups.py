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

_logger = logging.getLogger(__name__)

class AccessGroups(models.Model):
    
    _inherit = "res.groups"

    #----------------------------------------------------------
    # Database
    #----------------------------------------------------------
    
    security_groups = fields.Many2many(
        comodel_name='muk_security.groups',
        relation='muk_security_groups_groups_rel',
        column1='rid',
        column2='gid',
        string='Groups')
