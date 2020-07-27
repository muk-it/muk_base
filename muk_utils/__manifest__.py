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

{
    "name": "MuK Utils",
    "summary": """Utility Features""",
    "version": "13.0.1.0.2",
    "category": "Extra Tools",
    "license": "LGPL-3",
    "author": "MuK IT",
    "website": "https://www.mukit.at",
    "contributors": ["Mathias Markl <mathias.markl@mukit.at>"],
    "depends": ["base_setup"],
    "data": [
        "actions/ir_attachment.xml",
        "views/ir_attachment.xml",
        "views/mixins_groups.xml",
        "views/res_config_settings.xml",
    ], 
    "images": ["static/description/banner.png"],
    "application": False,
    "installable": True,
    "auto_install": False,
}