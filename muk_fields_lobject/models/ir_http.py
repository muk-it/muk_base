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

import logging
import mimetypes

from odoo import models
from odoo.http import request, STATIC_CACHE
from odoo.exceptions import AccessError

_logger = logging.getLogger(__name__)

class LargeObjectControllerIrHttp(models.AbstractModel):
    
    _inherit = 'ir.http'
    
    @classmethod
    def lobject_content(cls, xmlid=None, model=None, id=None, field='content', unique=False,
                        filename=None, filename_field='content_fname', download=False, mimetype=None,
                        default_mimetype='application/octet-stream', access_token=None, env=None):
        obj = None
        env = env or request.env
        if xmlid:
            obj = env.ref(xmlid, False)
        elif id and model in env.registry:
            obj = env[model].browse(int(id))
        if not obj or not obj.exists() or field not in obj:
            return (404, [], None)
        try:
            last_update = obj['__last_update']
        except AccessError:
            return (403, [], None)
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
        if not mimetype:
            mimetype = default_mimetype
        headers += [('Content-Type', mimetype), ('X-Content-Type-Options', 'nosniff')]
        etag = bool(request) and request.httprequest.headers.get('If-None-Match')
        retag = '"%s"' % obj.with_context({'checksum': True})[field] if content else ""
        status = status or (304 if etag == retag else 200)
        headers.append(('ETag', retag))
        headers.append(('Cache-Control', 'max-age=%s' % (STATIC_CACHE if unique else 0)))
        if download:
            headers.append(('Content-Disposition', cls.content_disposition(filename)))
        return (status, headers, content)