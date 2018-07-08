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

class Groups(models.AbstractModel):
    
    _name = 'muk_utils.groups'
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
        required=True, 
        translate=True)
    
    parent_left = fields.Integer(
        string='Left Parent', 
        index=True)
    
    parent_right = fields.Integer(
        string='Right Parent', 
        index=True)

    count_users = fields.Integer(
        compute='_compute_count_users',
        string="Users")
    
    @api.model
    def _add_magic_fields(self):
        super(Groups, self)._add_magic_fields()
        def add(name, field):
            if name not in self._fields:
                self._add_field(name, field)
        base, model = self._name.split(".")
        add('parent_group', fields.Many2one(
            _module=base,
            comodel_name=self._name,
            string='Parent Group', 
            ondelete='cascade', 
            auto_join=True,
            index=True,
            automatic=True))
        add('child_groups', fields.One2many(
            _module=base,
            comodel_name=self._name,
            inverse_name='parent_group', 
            string='Child Groups',
            automatic=True))
        add('groups', fields.Many2many(
            _module=base,
            comodel_name='res.groups',
            relation='%s_groups_rel' % (self._table),
            column1='gid',
            column2='rid',
            string='Groups',
            automatic=True))
        add('explicit_users', fields.Many2many(
            _module=base,
            comodel_name='res.users',
            relation='%s_explicit_users_rel' % (self._table),
            column1='gid',
            column2='uid', 
            string='Explicit Users',
            automatic=True))
        add('users', fields.Many2many(
            _module=base,
            comodel_name='res.users',
            relation='%s_users_rel' % (self._table),
            column1='gid',
            column2='uid', 
            string='Users',
            compute='_compute_users', 
            store=True,
            automatic=True))
    
    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'The name of the group must be unique!')
    ]
    
    #----------------------------------------------------------
    # Functions
    #----------------------------------------------------------

    @api.multi
    def trigger_computation_up(self, fields, *largs, **kwargs):
        parent_groups = self.mapped('parent_group')
        if parent_groups.exists():
            parent_groups.with_context(is_parent=True).trigger_computation(fields)
            
    @api.multi
    def trigger_computation_down(self, fields, *largs, **kwargs):
        child_groups = self.mapped('child_groups')
        if child_groups.exists():
            child_groups.with_context(is_child=True).trigger_computation(fields)

    @api.multi
    def trigger_computation(self, fields, *largs, **kwargs):
        super(Groups, self).trigger_computation(fields, *largs, **kwargs)
        if "users" in fields:
            self.suspend_security()._compute_users()
            self.suspend_security().trigger_computation_down(fields)

    @api.model
    def check_user_values(self, values):
        if any(field in values for field in [
            'parent_group', 'groups', 'explicit_users']):
            return True
        return False
    
    @api.multi
    @api.returns('res.users')
    def get_users(self):
        self.ensure_one()
        users = self.env['res.users']
        if self.parent_group:
            users |= self.parent_group.users
        users |= self.groups.mapped('users')
        users |= self.explicit_users
        return users
    
    #----------------------------------------------------------
    # Read, View 
    #----------------------------------------------------------
    
    @api.multi
    def _compute_users(self):
        for record in self:
            record.users = record.get_users()
    
    @api.depends('users')
    def _compute_count_users(self):
        for record in self:
            record.count_users = len(record.users)
    
    #----------------------------------------------------------
    # Create, Write, Delete
    #----------------------------------------------------------
    
    @api.multi
    def _check_recomputation(self, vals, olds, *largs, **kwargs):
        super(Groups, self)._check_recomputation(vals, olds, *largs, **kwargs)
        fields = []
        if self.check_user_values(vals):
            fields.extend(['users'])
        if fields:
            self.trigger_computation(fields)
    
    #----------------------------------------------------------
    # Cron Job Functions
    #----------------------------------------------------------
    
    @api.model
    def update_groups(self, *args, **kwargs):
        self.search([]).trigger_computation(['users'])
 