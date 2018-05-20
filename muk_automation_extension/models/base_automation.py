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

from collections import defaultdict

from odoo import api, models, fields

_logger = logging.getLogger(__name__)

class BaseAutomation(models.Model):
   
    _inherit = 'base.automation'

    trigger = fields.Selection(
        selection_add=[('on_create_or_write_or_unlink', 'On Creation & Update & Deletion')])
    
    @api.onchange('trigger')
    def onchange_trigger(self):
        super(BaseAutomation, self).onchange_trigger()
        if self.trigger == "on_create_or_write_or_unlink":
            self.filter_pre_domain = False
            self.trg_date_id = False
            self.trg_date_range = False
            self.trg_date_range_type = False
            
    @api.model_cr
    def _register_hook(self):
        def make_create():
            @api.model
            def create(self, vals, **kw):
                actions = self.env['base.automation']._get_actions(self, ['on_create_or_write_or_unlink'])
                record = create.origin(self.with_env(actions.env), vals, **kw)
                for action in actions.with_context(old_values=None):
                    action._process(action._filter_post(record))
                return record.with_env(self.env)
            return create

        def make_write():
            @api.multi
            def _write(self, vals, **kw):
                actions = self.env['base.automation']._get_actions(self, ['on_create_or_write_or_unlink'])
                records = self.with_env(actions.env)
                pre = {action: action._filter_pre(records) for action in actions}
                old_values = {
                    old_vals.pop('id'): old_vals
                    for old_vals in records.read(list(vals))
                }
                _write.origin(records, vals, **kw)
                for action in actions.with_context(old_values=old_values):
                    action._process(action._filter_post(pre[action]))
                return True
            return _write

        def make_unlink():
            @api.multi
            def unlink(self, **kwargs):
                actions = self.env['base.automation']._get_actions(self, ['on_create_or_write_or_unlink'])
                records = self.with_env(actions.env)
                for action in actions:
                    action._process(action._filter_post(records))
                return unlink.origin(self, **kwargs)
            return unlink

        patched_models = defaultdict(set)
        def patch(model, name, method):
            if model not in patched_models[name]:
                patched_models[name].add(model)
                model._patch_method(name, method)

        super(BaseAutomation, self)._register_hook()
        for action_rule in self.with_context({}).search([]):
            Model = self.env.get(action_rule.model_name)
            if Model is None:
                continue
            if action_rule.trigger == 'on_create_or_write_or_unlink':
                patch(Model, 'create', make_create())
                patch(Model, '_write', make_write())
                patch(Model, 'unlink', make_unlink())