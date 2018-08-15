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
import datetime

from odoo.tests import common

_logger = logging.getLogger(__name__)

class AutoVacuumTestCase(common.TransactionCase):
    
    at_install = False
    post_install = True
    
    def setUp(self):
        super(AutoVacuumTestCase, self).setUp()
        # create test rules
        model_model = self.env['ir.model']
        model_fields = self.env['ir.model.fields']
        model_logs = model_model.search([('model', '=', 'ir.logging')], limit=1)
        time_field_domain = [
            ('model_id', '=', model_logs.id),
            ('ttype', '=', 'datetime'),
            ('name', '=', 'create_date')]
        time_field_logs = model_fields.search(time_field_domain, limit=1)
        self.rules = self.env['muk_autovacuum.rules']
        self.rules |= self.rules.create({
            'name': "Delete Logs after 2 Day",
            'state': 'time',
            'model': model_logs.id,
            'time_field': time_field_logs.id,
            'time_type': 'days',
            'time': 2})
        self.rules |= self.rules.create({
            'name': "Delete Logs Count > 1",
            'state': 'size',
            'model': model_logs.id,
            'size': 1,
            'size_order': "id desc",
            'size_type': 'fixed'})
        self.rules |= self.rules.create({
            'name': "Delete Logs with Domain",
            'state': 'domain',
            'model': model_logs.id,
            'domain': "[]"})
        # create test logs
        self.logs = self.env['ir.logging']
        time = datetime.datetime.utcnow()
        for index in range(0, 10):
            self.logs |= self.logs.create({
                'create_date': time - datetime.timedelta(days=index),
                'create_uid': self.env.user.id,
                'name': "Test %s" % index,
                'type': 'server',
                'dbname': self.env.cr.dbname,
                'level': "INFO",
                'message': "TEST",
                'path': "PATH",
                'func': "TEST",
                'line': 1})
        
    def tearDown(self):
        super(AutoVacuumTestCase, self).tearDown()
        self.logs.unlink()
        self.rules.unlink()
    
    def test_autovacuum(self):
        count_before = self.env['ir.logging'].search([], count=True)
        self.env['ir.cron'].search([('model_id', '=', 'ir.autovacuum')]).ir_actions_server_id.run()
        count_after = self.env['ir.logging'].search([], count=True)
        self.assertTrue(count_before > count_after)
        