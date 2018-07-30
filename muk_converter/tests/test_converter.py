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

import os
import logging
import unittest

from odoo.tests import common

from odoo.addons.muk_converter.tools import converter

_path = os.path.dirname(os.path.dirname(__file__))
_logger = logging.getLogger(__name__)

class ConverterTestCase(common.TransactionCase):
    
    def setUp(self):
        super(ConverterTestCase, self).setUp()

    def tearDown(self):
        super(ConverterTestCase, self).tearDown()
        
    def test_formats(self):
        self.assertTrue(converter.formats())
    
    @unittest.skipIf(os.environ.get('TRAVIS', False), "Skipped for Travis CI")
    def test_convert(self):
        with open(os.path.join(_path, 'tests/data', 'sample.png'), 'rb') as file:
            self.assertTrue(converter.convert('sample.png', file.read(), "pdf"))
    
    @unittest.skipIf(os.environ.get('TRAVIS', False), "Skipped for Travis CI")
    def test_convert2pdf(self):
        with open(os.path.join(_path, 'tests/data', 'sample.png'), 'rb') as file:
            self.assertTrue(converter.convert2pdf('sample.png', file.read()))
    
    @unittest.skipIf(os.environ.get('TRAVIS', False), "Skipped for Travis CI")
    def test_convert2html(self):
        with open(os.path.join(_path, 'tests/data', 'sample.png'), 'rb') as file:
            self.assertTrue(converter.convert2html('sample.png', file.read()))