###################################################################################
#
#    Copyright (c) 2017-2019 MuK IT GmbH.
#
#    This file is part of MuK Large Objects Attachment
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

import base64
import logging

from odoo import api, models
from odoo.addons.muk_fields_lobject.fields.lobject import LargeObject

_logger = logging.getLogger(__name__)


class LObjectIrAttachment(models.Model):

    _inherit = "ir.attachment"

    # ----------------------------------------------------------
    # Database
    # ----------------------------------------------------------

    store_lobject = LargeObject(string="Data")

    # ----------------------------------------------------------
    # Helper
    # ----------------------------------------------------------

    @api.model
    def _get_storage_domain(self, storage):
        if storage == "lobject":
            return [("store_lobject", "=", False)]
        return super(LObjectIrAttachment, self)._get_storage_domain(storage)

    # ----------------------------------------------------------
    # Function
    # ----------------------------------------------------------

    @api.model
    def storage_locations(self):
        locations = super(LObjectIrAttachment, self).storage_locations()
        locations.append("lobject")
        return locations

    # ----------------------------------------------------------
    # Read
    # ----------------------------------------------------------

    @api.depends("store_lobject")
    def _compute_datas(self):
        bin_size = self._context.get("bin_size")
        for attach in self:
            if attach.store_lobject:
                if bin_size:
                    attach.datas = attach.with_context(
                        {"human_size": True}
                    ).store_lobject
                else:
                    attach.datas = attach.with_context({"base64": True}).store_lobject
            else:
                super(LObjectIrAttachment, attach)._compute_datas()

    # ----------------------------------------------------------
    # Create, Write, Delete
    # ----------------------------------------------------------

    def _get_datas_related_values(self, data, mimetype):
        if self._storage() == "lobject":
            bin_data = base64.b64decode(data) if data else b""
            values = {
                "file_size": len(bin_data),
                "checksum": self._compute_checksum(bin_data),
                "index_content": self._index(bin_data, mimetype),
                "store_lobject": bin_data,
                "store_fname": False,
                "db_datas": False,
            }
            return values
        return super(LObjectIrAttachment, self)._get_datas_related_values(
            data, mimetype
        )
