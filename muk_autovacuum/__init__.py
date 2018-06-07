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

from odoo import api, SUPERUSER_ID

from . import models

def _get_value(env, model):
    model_model = env['ir.model']
    model_fields = env['ir.model.fields']
    model = model_model.search([('model', '=', model)], limit=1)
    if model.exists():
        field_domain = [
            ('model_id', '=', model.id),
            ('ttype', '=', 'datetime'),
            ('name', '=', 'create_date')]
        field = model_fields.search(field_domain, limit=1)
        return model, field
    return None
    
def _init_default_rules(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    rule = env['muk_autovacuum.rules']
    values = _get_value(env, 'mail.message')
    if values:
        rule.create({
            'name': "Delete Message Attachments after 6 Months",
            'model': values[0].id,
            'active': False,
            'state': 'time',
            'time_field': values[1].id,
            'time_type': 'months',
            'time': 6,
            'only_attachments': True})
        rule.create({
            'name': "Delete Messages after 1 Year",
            'model': values[0].id,
            'active': False,
            'state': 'time',
            'time_field': values[1].id,
            'time_type': 'years',
            'time': 1})
    values = _get_value(env, 'ir.logging')
    if values:
        rule.create({
            'name': "Delete Logs after 2 Weeks",
            'model': values[0].id,
            'active': False,
            'state': 'time',
            'time_field': values[1].id,
            'time_type': 'weeks',
            'time': 2,
            'protect_starred': False})