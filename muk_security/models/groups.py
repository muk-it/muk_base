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
    _inherit = 'muk_utils.model'
    
    _parent_store = True
    _parent_name = "parent_group"
    _parent_order = 'parent_left'
    _order = 'parent_left'
    
    #----------------------------------------------------------
    # Database
    #----------------------------------------------------------
    
    name = fields.Char(
        string="Group Name", 
        required=True)
    
    parent_group = fields.Many2one(
        comodel_name='muk_security.groups', 
        string='Parent Group', 
        ondelete='cascade', 
        auto_join=True,
        index=True)
    
    child_groups = fields.One2many(
        comodel_name='muk_security.groups', 
        inverse_name='parent_group', 
        string='Child Groups')
    
    parent_left = fields.Integer(
        string='Left Parent', 
        index=True)
    
    parent_right = fields.Integer(
        string='Right Parent', 
        index=True)
    
    perm_read = fields.Boolean(
        string='Read Access')
    
    perm_create = fields.Boolean(
        string='Create Access')
    
    perm_write = fields.Boolean(
        string='Write Access')
    
    perm_unlink = fields.Boolean(
        string='Unlink Access')
    
    groups = fields.Many2many(
        comodel_name='res.groups',
        relation='muk_groups_groups_rel',
        column1='gid',
        column2='rid',
        string='Groups')
    
    explicit_users = fields.Many2many(
        comodel_name='res.users',
        relation='muk_groups_explicit_users_rel',
        column1='gid',
        column2='uid', 
        string='Explicit Users')
    
    users = fields.Many2many(
        comodel_name='res.users',
        relation='muk_groups_users_rel',
        column1='gid',
        column2='uid', 
        string='Users', 
        compute='_compute_users', 
        store=True)

    count_users = fields.Integer(
        compute='_compute_count_users',
        string="Users")
    
    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'The name of the group must be unique!')
    ]
    
    #----------------------------------------------------------
    # Functions
    #----------------------------------------------------------
    
    def trigger_computation_up(self, fields):
        parent_group = self.parent_group
        if parent_group:
            parent_group.trigger_computation(fields)
            
    def trigger_computation_down(self, fields):
        for child in self.child_groups:
            child.with_context(is_subnode=True).trigger_computation(fields)
            
    def trigger_computation(self, fields):
        values = {}
        if "users" in fields:
            values.update(self._compute_users(write=False))
        if values:
            self.write(values);   
            if "users" in fields:
                self.trigger_computation_down(fields)

    #----------------------------------------------------------
    # Read, View 
    #----------------------------------------------------------
    
    @api.model
    def check_user_values(self, values):
        if any(field in values for field in ['parent_group', 'groups', 'explicit_users']):
            return True
        return False
    
    @api.multi
    def get_users(self):
        self.ensure_one()
        users = self.env['res.users']
        if self.parent_group:
            users |= self.parent_group.users
        users |= self.groups.mapped('users')
        users |= self.explicit_users
        return users
    
    def _compute_users(self, write=True):
        if write:
            for record in self:
                record.users = record.get_users()
        else:
            self.ensure_one()
            return {'users': [(6, 0, self.get_users().mapped('id'))]}
    
    @api.depends('users')
    def _compute_count_users(self):
        for record in self:
            record.count_users = len(record.users)
    
    #----------------------------------------------------------
    # Create, Write, Delete
    #----------------------------------------------------------
    
    def _after_create(self, vals):
        record = super(AccessGroups, self)._after_create(vals)
        record._check_recomputation(vals)
        return record
        
    def _after_write_record(self, vals):
        vals = super(AccessGroups, self)._after_write_record(vals)
        self._check_recomputation(vals)
        return vals
    
    def _check_recomputation(self, values):
        fields = []
        if self.check_user_values(values):
            fields.extend(['users'])
        if fields:
            self.trigger_computation(fields)