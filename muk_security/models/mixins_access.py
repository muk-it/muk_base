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

from odoo import _
from odoo import models, api, fields
from odoo.exceptions import AccessError

_logger = logging.getLogger(__name__)

class AccessModel(models.AbstractModel):
    
    _name = 'muk_security.mixins.access'
    _description = 'Access Mixin'
    
    #----------------------------------------------------------
    # Database
    #----------------------------------------------------------
            
    permission_read = fields.Boolean(
        compute='_compute_permissions_read',
        search='_search_permission_read',
        string="Read Access")
    
    permission_create = fields.Boolean(
        compute='_compute_permissions_create',
        search='_search_permission_create',
        string="Create Access")
    
    permission_write = fields.Boolean(
        compute='_compute_permissions_write',
        search='_search_permission_write',
        string="Write Access")
    
    permission_unlink = fields.Boolean(
        compute='_compute_permissions_unlink', 
        search='_search_permission_unlink',
        string="Delete Access")
        
    #----------------------------------------------------------
    # Function
    #----------------------------------------------------------
    
    @api.multi
    def check_access(self, operation, raise_exception=False):
        try:
            access_right = self.check_access_rights(operation, raise_exception)
            access_rule = self.check_access_rule(operation) is None
            return access_right and access_rule
        except AccessError:
            if raise_exception:
                raise
            return False

    #----------------------------------------------------------
    # Search
    #----------------------------------------------------------
    
    @api.model
    def _search_permission_read(self, operator, operand):
        records = self.search([]).filtered(lambda r: r.check_access('read') == True)
        if operator == '=' and operand:
            return [('id', 'in', records.mapped('id'))]
        return [('id', 'not in', records.mapped('id'))]
    
    @api.model
    def _search_permission_create(self, operator, operand):
        records = self.search([]).filtered(lambda r: r.check_access('create') == True)
        if operator == '=' and operand:
            return [('id', 'in', records.mapped('id'))]
        return [('id', 'not in', records.mapped('id'))]
    
    @api.model
    def _search_permission_write(self, operator, operand):
        records = self.search([]).filtered(lambda r: r.check_access('write') == True)
        if operator == '=' and operand:
            return [('id', 'in', records.mapped('id'))]
        return [('id', 'not in', records.mapped('id'))]
    
    @api.model
    def _search_permission_unlink(self, operator, operand):
        records = self.search([]).filtered(lambda r: r.check_access('unlink') == True)
        if operator == '=' and operand:
            return [('id', 'in', records.mapped('id'))]
        return [('id', 'not in', records.mapped('id'))]

    #----------------------------------------------------------
    # Read, View 
    #----------------------------------------------------------
    
    @api.multi
    def _compute_permissions_read(self):
        for record in self:
            record.update({'permission_read': record.check_access('read')})
            
    @api.multi
    def _compute_permissions_create(self):
        for record in self:
            record.update({'permission_create': record.check_access('create')})
            
    @api.multi
    def _compute_permissions_write(self):
        for record in self:
            record.update({'permission_write': record.check_access('write')})
            
    @api.multi
    def _compute_permissions_unlink(self):
        for record in self:
            record.update({'permission_unlink': record.check_access('unlink')})