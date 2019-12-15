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

import io
import os
import base64
import mimetypes
import functools

from odoo import http, SUPERUSER_ID
from odoo.modules import registry, get_resource_path
from odoo.tools.mimetypes import guess_mimetype
from odoo.tools import config
from odoo.http import request

from odoo.addons.web.controllers.main import Binary
from odoo.addons.muk_saas_branding.tools.utils import safe_execute

class Binary(Binary):
    
    def _get_company_image_placeholder(self):
        if config.get("default_company_image_folder", False):
            def get_path(filename):
                return os.path.join(config.get("default_company_image_folder"), filename)
            return get_path
        return functools.partial(get_resource_path, 'muk_saas_branding', 'static', 'src', 'img')
    
    def _get_company_image_data(self, dbname, uid, field, company=None):
        try:
            dbreg = registry.Registry(dbname)
            with dbreg.cursor() as cr:
                if company:
                    cr.execute("""
                        SELECT {0}, write_date
                        FROM res_company
                        WHERE id = %s        
                    """.format(field), (company,))
                else:
                    cr.execute("""
                        SELECT c.{0}, c.write_date
                        FROM res_users u
                        LEFT JOIN res_company c
                        ON c.id = u.company_id
                        WHERE u.id = %s
                    """.format(field), (uid,))
                return cr.fetchone()
        except Exception:
            return None
        
    def _get_company_image_response(self, dbname, field, placeholders, default_mimetype, company=None):
        uid = request.session.uid if request.session.db else None
        placeholder = self._get_company_image_placeholder()
        if request.session.db:
            dbname = request.session.db
        elif dbname is None:
            dbname = http.db_monodb()
        if not dbname:
            response = http.send_file(placeholder(placeholders[0]))
        else:
            uid = uid if uid else SUPERUSER_ID
            company_data = self._get_company_image_data(dbname, uid, field, company)
            if company_data and company_data[0]:
                image_data = base64.b64decode(company_data[0])
                mimetype = guess_mimetype(image_data, default=default_mimetype)
                extension = mimetypes.guess_extension(mimetype)
                response = http.send_file(
                    io.BytesIO(image_data), filename=('logo%s' % extension),
                    mimetype=mimetype, mtime=company_data[1]
                )
            else:
                response = http.send_file(placeholder(placeholders[1]))
        return response
    
    @http.route(['/web/binary/company_logo', '/logo', '/logo.png'], type='http', auth="none")
    def company_logo(self, dbname=None, **kw):
        company = safe_execute(False, int, kw['company']) if kw and kw.get('company') else False
        return self._get_company_image_response(
            dbname, 'logo_web', ('logo.png', 'nologo.png'), 'image/png', company
        )
        
    @http.route(['/web/binary/company_favicon', '/favicon', '/favicon.ico'], type='http', auth="none")
    def company_favicon(self, dbname=None, **kw):
        company = safe_execute(False, int, kw['company']) if kw and kw.get('company') else False
        return self._get_company_image_response(
            dbname, 'favicon', ('favicon.ico', 'nofavicon.ico'), 'image/x-icon', company
        )
        