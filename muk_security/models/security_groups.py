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

from odoo import models, fields, api

class AccessGroups(models.Model):
    
    _name = 'muk_security.groups'
    _description = "Access Groups"
    _inherit = 'muk_utils.groups'
    
    #----------------------------------------------------------
    # Database
    #----------------------------------------------------------
    
    perm_read = fields.Boolean(
        string='Read Access')
    
    perm_create = fields.Boolean(
        string='Create Access')
    
    perm_write = fields.Boolean(
        string='Write Access')
    
    perm_unlink = fields.Boolean(
        string='Unlink Access')
 