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

from odoo.addons.muk_thumbnails.service import thumbnail

_path = os.path.dirname(os.path.dirname(__file__))
_logger = logging.getLogger(__name__)

class ThumbnailTestCase(common.TransactionCase):
    
    def setUp(self):
        super(ThumbnailTestCase, self).setUp()

    def tearDown(self):
        super(ThumbnailTestCase, self).tearDown()
    
    @unittest.skipIf(os.environ.get('TRAVIS', False), "Skipped for Travis CI")
    def test_thumbnail_unoconv(self):
        with open(os.path.join(_path, 'tests/data', 'sample.xls'), 'rb') as file:
           self.assertTrue(thumbnail.create_thumbnail(binary=file.read(), filename='sample.xls'))
    
    @unittest.skipIf(os.environ.get('TRAVIS', False), "Skipped for Travis CI")
    def test_thumbnail_video(self):
        with open(os.path.join(_path, 'tests/data', 'sample.mp4'), 'rb') as file:
           self.assertTrue(thumbnail.create_thumbnail(binary=file.read(), filename='sample.mp4'))
   