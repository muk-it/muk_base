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

from collections import defaultdict

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError

from odoo.addons.base.res import res_users

from odoo.addons.muk_security.tools import helper

_logger = logging.getLogger(__name__)

class ResUser(models.Model):
    
    _inherit = 'res.users'
        
    #----------------------------------------------------------
    # Create, Update, Delete
    #----------------------------------------------------------
    
    @api.model
    def create(self, values):
        result = super(ResUser, self).create(values)
        model_recs = defaultdict(set)
        model_names = self.pool.descendants(['muk_utils.groups'], '_inherit', '_inherits')
        for model_name in model_names:
            model = self.env[model_name].sudo()
            if not model._abstract:
                model_recs[model_name] = model.search([['groups', 'in', self.mapped('groups_id.id')]])
        for tuple in model_recs.items():
            tuple[1].trigger_computation(['users'])
        return result
                
    @api.multi
    def write(self, vals):
        group_ids = self.mapped('groups_id.id')
        result = super(ResUser, self).write(vals)
        group_ids += [vals[k] for k in vals if res_users.is_selection_groups(k) and vals[k]]
        group_ids += [vals[k] for k in vals if res_users.is_boolean_group(k) and vals[k]]
        if any(field in vals for field in ['groups_id']):
            group_ids += self.mapped('groups_id.id')
        if group_ids:
            model_recs = defaultdict(set)
            model_names = self.pool.descendants(['muk_utils.groups'], '_inherit', '_inherits')
            for model_name in model_names:
                model = self.env[model_name].sudo()
                if not model._abstract:
                     model_recs[model_name] = model.search([['groups', 'in', group_ids]])
            for tuple in model_recs.items():
                tuple[1].trigger_computation(['users'])
        return result
    
    @api.multi
    def unlink(self):
        model_recs = defaultdict(set)
        model_names = self.pool.descendants(['muk_utils.groups'], '_inherit', '_inherits')
        for model_name in model_names:
            model = self.env[model_name].sudo()
            if not model._abstract:
                model_recs[model_name] = model.search([['groups', 'in', self.mapped('groups_id.id')]])
        result = super(ResUser, self).unlink()
        for tuple in model_recs.items():
            tuple[1].trigger_computation(['users'])
        return result