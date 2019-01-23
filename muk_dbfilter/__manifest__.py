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
    "name": "MuK DB Filter",
    "summary": """Headers based Database Selection""",
    "version": "12.0.1.0.1",
    'category': 'Extra Tools',
    'license': 'AGPL-3',
    'author': 'MuK IT',
    'website': 'https://www.mukit.at',
    'live_test_url': 'https://demo.mukit.at/web/login',
    "depends": [
    ],
    "contributors": [
        "Kerrim Abdelhamed <kerrim.abdelhamed@mukit.at>",
        "Mathias Markl <mathias.markl@mukit.at>"
    ],
    "data": [
    ],
    "demo": [
    ],
    "qweb": [
    ],
    "images": [
        'static/description/banner.png'
    ],
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "installable": True,
    "auto_install": False,
    "application": False,
    "post_load": "_patch_system",
}
