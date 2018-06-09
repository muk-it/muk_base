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

from odoo import _, SUPERUSER_ID
from odoo import models, api, fields
from odoo.exceptions import AccessError

_logger = logging.getLogger(__name__)

class BaseModelAccessGroups(models.AbstractModel):
    
    _name = 'muk_security.access_groups'
    _description = "MuK Access Groups Model"
    _inherit = 'muk_security.access'
    
    # Set it to True to enforced security even if no group has been set
    _strict_security = False 
    
    #----------------------------------------------------------
    # Function
    #----------------------------------------------------------
        
    @api.model
    def _add_magic_fields(self):
        super(BaseModelAccessGroups, self)._add_magic_fields()
        def add(name, field):
            if name not in self._fields:
                self._add_field(name, field)
        base, model = self._name.split(".")
        add('groups', fields.Many2many(
            _module=base,
            comodel_name='muk_security.groups',
            relation='muk_groups_%s_rel' % model,
            column1='aid',
            column2='gid',
            string="Groups",
            automatic=True))
        add('complete_groups', fields.Many2many(
            _module=base,
            comodel_name='muk_security.groups',
            relation='muk_groups_complete_%s_rel' % model,
            column1='aid',
            column2='gid',
            string="Complete Groups", 
            compute='_compute_groups', 
            store=True,
            automatic=True))
    
    @api.model
    def _get_no_access_ids(self):
        base, model = self._name.split(".")
        if not self._strict_security:
            sql = '''
                SELECT id
                FROM %s a
                WHERE NOT EXISTS (
                    SELECT *
                    FROM muk_groups_complete_%s_rel r
                    WHERE r.aid = a.id
                );         
            ''' % (self._table, model)
            self.env.cr.execute(sql)
            fetch = self.env.cr.fetchall()
            return len(fetch) > 0 and list(map(lambda x: x[0], fetch)) or []
        else:
            return []
    
    @api.model
    def _get_access_ids(self):
        base, model = self._name.split(".")
        sql = '''
            SELECT r.aid
            FROM muk_groups_complete_%s_rel r
            JOIN muk_security_groups g ON r.gid = g.id
            JOIN muk_groups_users_rel u ON r.gid = u.gid
            WHERE u.uid = %s AND g.perm_read = true
        ''' % (model, self.env.user.id)
        self.env.cr.execute(sql)
        fetch = self.env.cr.fetchall()
        access_ids = len(fetch) > 0 and list(map(lambda x: x[0], fetch)) or []
        return access_ids
    
    @api.model
    def _get_complete_access_ids(self):
        return self._get_no_access_ids() + self._get_access_ids()
    
    @api.multi
    def _eval_access_skip(self):
        return False
    
    @api.multi
    def check_access_rule(self, operation):
        super(BaseModelAccessGroups, self).check_access_rule(operation)
        if self.env.user.id == SUPERUSER_ID or self._eval_access_skip():
            return None
        base, model = self._name.split(".")
        no_access_ids = self._get_no_access_ids()
        for record in self.filtered(lambda rec: rec.id not in no_access_ids):
            sql = '''
                SELECT perm_%s                
                FROM muk_groups_complete_%s_rel r
                JOIN muk_security_groups g ON g.id = r.gid
                JOIN muk_groups_users_rel u ON u.gid = g.id
                WHERE r.aid = %s AND u.uid = %s
            ''' % (operation, model, record.id, self.env.user.id)
            self.env.cr.execute(sql)
            fetch = self.env.cr.fetchall()
            if not any(list(map(lambda x: x[0], fetch))):
                raise AccessError(_("This operation is forbidden!"))
        
    #----------------------------------------------------------
    # Read
    #----------------------------------------------------------
        
    def _after_read(self, result, *largs, **kwargs):
        result = super(BaseModelAccessGroups, self)._after_read(result)
        if self.env.user.id == SUPERUSER_ID or self._eval_access_skip():
            return result
        access_ids = self._get_complete_access_ids()
        result = [result] if not isinstance(result, list) else result
        if len(access_ids) > 0:
            access_result = []
            for record in result:
                if record['id'] in access_ids:
                    access_result.append(record)
            return access_result
        return []
    
    def _after_search(self, result, *largs, **kwargs):
        result = super(BaseModelAccessGroups, self)._after_search(result)
        if self.env.user.id == SUPERUSER_ID or self._eval_access_skip():
            return result
        access_ids = self._get_complete_access_ids()
        if len(access_ids) > 0:
            access_result = self.env[self._name]
            if isinstance(result, int):
                if result in access_ids:
                    return result
            else:
                for record in result:
                    if record.id in access_ids:
                        access_result += record
                return access_result
        return self.env[self._name]
    
    def _after_name_search(self, result, *largs, **kwargs):
        result = super(BaseModelAccessGroups, self)._after_name_search(result)
        if self.env.user.id == SUPERUSER_ID or self._eval_access_skip():
            return result
        access_ids = self._get_complete_access_ids()
        if len(access_ids) > 0:
            access_result = []
            for tuple in result:
                if tuple[0] in access_ids:
                    access_result.append(tuple)
            return access_result
        return []
    
    #----------------------------------------------------------
    # Read, View 
    #----------------------------------------------------------
        
    def _compute_groups(self, write=True):
        if write:
            for record in self:
                record.complete_groups = record.groups
        else:
            self.ensure_one()
            return {'complete_groups': [(6, 0, self.groups.mapped('id'))]}