###################################################################################
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

{
    "name": "MuK Converter",
    "summary": """Universal Converter""",
    "version": '11.0.1.2.6',   
    "category": 'Extra Tools',   
    "license": "AGPL-3",
    "website": "https://www.mukit.at",
    "live_test_url": "https://demo.mukit.at/web/login",
    "author": "MuK IT",
    "contributors": [
        "Mathias Markl <mathias.markl@mukit.at>",
        "Kerrim Abd El-Hamed <kerrim.abdelhamed@mukit.at>",
    ],
    "depends": [
        "iap",
        "base_setup",
        "muk_autovacuum",
        "muk_fields_lobject",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/params.xml",
        "data/autovacuum.xml",
        "views/convert.xml",
        "views/res_config_settings_view.xml",
    ],
    "qweb": [
        "static/src/xml/*.xml",
    ],
    "images": [
        'static/description/banner.png'
    ],
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "application": False,
    "installable": True,
}
