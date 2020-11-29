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

from odoo import _, api, models
from odoo.exceptions import AccessError
from odoo.osv import expression

_logger = logging.getLogger(__name__)


class IrAttachment(models.Model):

    _inherit = "ir.attachment"

    # ----------------------------------------------------------
    # Helper
    # ----------------------------------------------------------

    @api.model
    def _get_storage_domain(self, storage):
        return {
            "db": [("db_datas", "=", False)],
            "file": [("store_fname", "=", False)],
        }[storage]

    # ----------------------------------------------------------
    # Actions
    # ----------------------------------------------------------

    def action_migrate(self):
        self.migrate()

    # ----------------------------------------------------------
    # Functions
    # ----------------------------------------------------------

    @api.model
    def storage_locations(self):
        return ["db", "file"]

    @api.model
    def force_storage(self):
        if not self._storage() in self.storage_locations():
            return super(IrAttachment, self).force_storage()
        if not self.env.user._is_admin():
            raise AccessError(_("Only administrators can execute this action."))
        self.search(
            expression.AND(
                [
                    self._get_storage_domain(self._storage()),
                    [
                        "&",
                        "|",
                        ("res_field", "=", False),
                        ("res_field", "!=", False),
                        ("type", "=", "binary"),
                    ],
                ]
            )
        ).migrate(batch_size=100)
        return True

    def migrate(self, batch_size=None):
        commit_on_batch = bool(batch_size)
        attachments_to_migrate = len(self)
        batch_size = batch_size or len(self) or 1
        storage_location = self._storage().upper()
        for index, attachment in enumerate(self, start=1):
            _logger.info(
                "Migrate Attachment {index} of {total} to {storage}".format(
                    **{
                        "index": index,
                        "total": attachments_to_migrate,
                        "storage": storage_location,
                    }
                )
            )
            attachment.write(
                {"datas": attachment.datas, "mimetype": attachment.mimetype}
            )
            if commit_on_batch and not index % batch_size:
                self.env.cr.commit()
