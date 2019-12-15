###################################################################################
#
#    Copyright (c) 2017-2019 MuK IT GmbH.
#
#    This file is part of MuK SaaS Branding 
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

import os
import sys
import json

from odoo import http, tools, service
from odoo.http import request, db_monodb, db_list

from odoo.addons.web.controllers.main import DBNAME_PATTERN
from odoo.addons.web.controllers.main import jinja2, Database

if hasattr(sys, 'frozen'):
    location = os.path.dirname(__file__)
    path = os.path.join(location, '..', 'templates')
    loader = jinja2.FileSystemLoader(os.path.realpath(path))
else:
    loader = jinja2.PackageLoader('odoo.addons.muk_saas_branding', 'templates')

env = jinja2.Environment(loader=loader, autoescape=True)
env.filters["json"] = json.dumps

class Database(Database):
    
    def _render_template(self, **d):
        d.setdefault('manage', True)
        d['insecure'] = tools.config.verify_admin_password('admin')
        d['list_db'] = tools.config['list_db']
        d['langs'] = service.db.exp_list_lang()
        d['countries'] = service.db.exp_list_countries()
        d['pattern'] = DBNAME_PATTERN
        d['system_name'] = tools.config.get(
            "database_manager_system_name", "Odoo"
        )
        d['system_logo'] = tools.config.get(
            "database_manager_system_logo_url",
            "/web/static/src/img/logo2.png"
        )
        d['system_favicon'] = tools.config.get(
            "database_manager_system_favicon_url",
            "/web/static/src/img/favicon.ico"
        )
        d['privacy_policy'] = tools.config.get(
            "database_manager_privacy_policy_url",
            "https://www.odoo.com/privacy"
        )
        d['databases'] = []
        try:
            d['databases'] = db_list()
            d['incompatible_databases'] = service.db.list_db_incompatible(d['databases'])
        except odoo.exceptions.AccessDenied:
            monodb = db_monodb()
            if monodb:
                d['databases'] = [monodb]
        return env.get_template("database_manager.html").render(d)
