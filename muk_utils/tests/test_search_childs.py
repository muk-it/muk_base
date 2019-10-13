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


class SearchChildsTestCase(common.TransactionCase):
    def setUp(self):
        super(SearchChildsTestCase, self).setUp()
        self.model = self.env["res.partner.category"]
        self.parent = self.model.create(
            {"parent_id": False, "name": "Parent", "active": True}
        )
        self.child = self.model.create(
            {"parent_id": self.parent.id, "name": "Child", "active": True}
        )
        self.child_parent = self.model.create(
            {"parent_id": self.parent.id, "name": "Child Parent", "active": True}
        )
        self.child_parent_child = self.model.create(
            {
                "parent_id": self.child_parent.id,
                "name": "Child Parent Child",
                "active": True,
            }
        )

    def tearDown(self):
        super(SearchChildsTestCase, self).tearDown()

    def test_search_childs(self):
        childs = self.model.search_childs(self.parent.id)
        self.assertEqual(set(childs.ids), {self.child.id, self.child_parent.id})

    def test_search_read_childs(self):
        childs = self.model.search_childs(self.parent.id)
        childs_names = self.model.search_read_childs(self.parent.id, fields=["name"])
        self.assertEqual(childs.read(["name"]), childs_names)
