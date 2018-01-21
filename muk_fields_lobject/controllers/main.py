# -*- coding: utf-8 -*-

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

import base64
import logging
import hashlib
import mimetypes

from werkzeug import utils
from  werkzeug import wrappers

from odoo import _
from odoo import tools
from odoo import http
from odoo.http import request
from odoo.http import Response
from odoo.exceptions import AccessError

_logger = logging.getLogger(__name__)

class LargeObjectController(http.Controller):

    @http.route(['/web/content',
        '/web/lobject/<string:xmlid>',
        '/web/lobject/<string:xmlid>/<string:filename>',
        '/web/lobject/<int:id>',
        '/web/lobject/<int:id>/<string:filename>',
        '/web/lobject/<string:model>/<int:id>/<string:field>',
        '/web/lobject/<string:model>/<int:id>/<string:field>/<string:filename>'], type='http', auth="public")
    def content_common(self, xmlid=None, model='ir.attachment', id=None, field='datas', filename=None,
                       filename_field='datas_fname', mimetype=None, download=None, access_token=None):
        obj = None
        if xmlid:
            obj = request.env.ref(xmlid, False)
        elif id and model in request.env.registry:
            obj = request.env[model].browse(int(id))
        if not obj or not obj.exists() or field not in obj:
            return request.not_found()
        try:
            last_update = obj['__last_update']
        except AccessError:
            return wrappers.Response(status=403, headers=[])
        status, headers, content = None, [], None
        content = obj.with_context({'stream': True})[field] or b''
        if not filename:
            if filename_field in obj:
                filename = obj[filename_field]
            else:
                filename = "%s-%s-%s" % (obj._name, obj.id, field)
        mimetype = 'mimetype' in obj and obj.mimetype or False
        if not mimetype and filename:
            mimetype = mimetypes.guess_type(filename)[0]
        headers += [('Content-Type', mimetype), ('X-Content-Type-Options', 'nosniff')]
        etag = bool(request) and request.httprequest.headers.get('If-None-Match')
        retag = '"%s"' % hashlib.md5(content).hexdigest()
        status = status or (304 if etag == retag else 200)
        headers.append(('ETag', retag))
        if download:
            headers.append(('Content-Disposition', http.content_disposition(filename)))
        return wrappers.Response(content, headers=headers, direct_passthrough=True, status=status)
        