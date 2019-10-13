###################################################################################
#
#    Copyright (c) 2017-2019 MuK IT GmbH.
#
#    This file is part of MuK Utils
#    (see https://mukit.at).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
###################################################################################

import logging

from odoo.tests import common

_logger = logging.getLogger(__name__)


class SecurityTestCase(common.TransactionCase):
    def setUp(self):
        super(SecurityTestCase, self).setUp()
        self.model = self.env["res.partner"].with_user(
            self.browse_ref("base.user_admin")
        )
        self.record_ids = self.model.search([], limit=25).ids

    def tearDown(self):
        super(SecurityTestCase, self).tearDown()

    def test_check_access(self):
        self.model.browse(self.record_ids).check_access("read")
        self.model.browse(self.record_ids).check_access("create")
        self.model.browse(self.record_ids).check_access("write")
        self.model.browse(self.record_ids).check_access("unlink")

    def test_filter_access(self):
        self.model.browse(self.record_ids)._filter_access("read", in_memory=True)
        self.model.browse(self.record_ids)._filter_access("read", in_memory=False)
        self.model.browse(self.record_ids)._filter_access_ids("read", in_memory=True)
        self.model.browse(self.record_ids)._filter_access_ids("read", in_memory=False)
