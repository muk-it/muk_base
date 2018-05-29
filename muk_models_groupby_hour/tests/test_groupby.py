###################################################################################
# 
#    MuK Document Management System
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

import os
import json
import base64
import logging
import unittest
import requests

import odoo
from odoo import _
from odoo.tests import common

_logger = logging.getLogger(__name__)

class AttachmentTestCase(common.TransactionCase):
    
    at_install = False
    post_install = True
    
    def setUp(self):
        super(AttachmentTestCase, self).setUp()
        self.attachment = self.env['ir.attachment'].sudo()
        
    def tearDown(self):
        super(AttachmentTestCase, self).tearDown()
    
    def test_groupy(self):
        result = self.attachment.read_group(
            domain=[],
            fields=['name', 'create_date'],
            groupby='create_date:hour')
        self.assertTrue(result)
        