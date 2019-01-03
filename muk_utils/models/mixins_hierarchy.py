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

import json
import operator
import functools
import collections

from odoo import models, fields, api

class Hierarchy(models.AbstractModel):
    
    _name = 'muk_utils.mixins.hierarchy'
    _description = 'Hierarchy Mixin'
    
    _parent_store = True
    _parent_path_sudo = False
    
    #----------------------------------------------------------
    # Database
    #----------------------------------------------------------
    
    parent_path = fields.Char(
        string="Parent Path", 
        index=True)
    
    @api.model
    def _add_magic_fields(self):
        super(Hierarchy, self)._add_magic_fields()
        def add(name, field):
            if name not in self._fields:
                self._add_field(name, field)
        add('parent_path_names', fields.Char(
            _module=self._module,
            compute='_compute_parent_path',
            compute_sudo=self._parent_path_sudo,
            string="Path Names",
            readonly=True,
            store=True,
            automatic=True))
        add('parent_path_json', fields.Char(
            _module=self._module,
            compute='_compute_parent_path',
            compute_sudo=self._parent_path_sudo,
            string="Path Json",
            readonly=True,
            store=True,
            automatic=True))
    
    #----------------------------------------------------------
    # Read, View 
    #----------------------------------------------------------
    
    @api.depends('parent_path')
    def _compute_parent_path(self):
        paths = [list(map(int, rec.parent_path.split('/')[:-1])) for rec in self]
        ids = set(functools.reduce(operator.concat, paths))
        data = dict(self.browse(ids).name_get())
        for record in self:
            path_names = [""]
            path_json = []
            for id in reversed(list(map(int, record.parent_path.split('/')[:-1]))):
                if id not in data:
                    break
                path_names.append(data[id][0])
                path_json.append({
                    'model': record._name,
                    'name': data[id][0],
                    'id': record.id,
                })
            path_names.reverse()
            path_json.reverse()
            record.update({
                'parent_path_names': '/'.join(path_names),
                'parent_path_json': json.dumps(path_json),
            })
            