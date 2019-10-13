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

from odoo import fields, models


class ResConfigSettings(models.TransientModel):

    _inherit = "res.config.settings"

    # ----------------------------------------------------------
    # Selections
    # ----------------------------------------------------------

    def _attachment_location_selection(self):
        locations = self.env["ir.attachment"].storage_locations()
        return list(map(lambda location: (location, location.upper()), locations))

    # ----------------------------------------------------------
    # Database
    # ----------------------------------------------------------

    attachment_location = fields.Selection(
        selection=lambda self: self._attachment_location_selection(),
        config_parameter="ir_attachment.location",
        string="Storage Location",
        help="Attachment storage location.",
        required=True,
        default="file",
    )

    # ----------------------------------------------------------
    # Actions
    # ----------------------------------------------------------

    def action_attachment_force_storage(self):
        self.env["ir.attachment"].force_storage()
