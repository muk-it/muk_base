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


class SearchParentTestCase(common.TransactionCase):
    def setUp(self):
        super(SearchParentTestCase, self).setUp()
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
        self.ids = [
            self.parent.id,
            self.child.id,
            self.child_parent.id,
            self.child_parent_child.id,
        ]
        self.domain = [("id", "in", self.ids)]

    def tearDown(self):
        super(SearchParentTestCase, self).tearDown()

    def _evaluate_parent_result(self, parents, records):
        for parent in parents:
            self.assertTrue(
                not parent.parent_id or parent.parent_id.id not in records.ids
            )

    def test_search_parents(self):
        records = self.model.search([])
        parents = self.model.search_parents([])
        self._evaluate_parent_result(parents, records)

    def test_search_parents_domain(self):
        records = self.model.search([("id", "!=", 1)])
        parents = self.model.search_parents([("id", "!=", 1)])
        self._evaluate_parent_result(parents, records)

    def test_search_parents_domain(self):
        records = self.model.search([("id", "!=", 1)])
        parents = self.model.search_parents([("id", "!=", 1)])
        self._evaluate_parent_result(parents, records)

    def test_search_parents_args(self):
        records = self.model.search([], offset=1, limit=1, order="name desc")
        parents = self.model.search_parents(offset=1, limit=1, order="name desc")
        self._evaluate_parent_result(parents, records)

    def test_search_parents_count(self):
        parents = self.model.search_parents(self.domain, count=False)
        parent_count = self.model.search_parents(self.domain, count=True)
        self.assertTrue(len(parents) == parent_count)

    def test_search_parents_access_rights(self):
        model = self.model.with_user(self.browse_ref("base.user_admin"))
        parents = model.search_parents(self.domain)
        self._evaluate_parent_result(parents, model.browse(self.ids))
        self.assertTrue(len(parents) == 1 and parents.id == self.parent.id)
        access_rule = self.env["ir.rule"].create(
            {
                "model_id": self.browse_ref("base.model_res_partner_category").id,
                "domain_force": [("id", "!=", self.parent.id)],
                "name": "Restrict Access",
            }
        )
        records = model.search(self.domain)
        parents = model.search_parents(self.domain)
        self._evaluate_parent_result(parents, records)
        self.assertTrue(set(parents.ids) == {self.child.id, self.child_parent.id})

    def test_search_read_parents(self):
        parents = self.model.search_parents([])
        read_names = parents.read(["name"])
        search_names = self.model.search_read_parents([], ["name"])
        self.assertTrue(read_names == search_names)
