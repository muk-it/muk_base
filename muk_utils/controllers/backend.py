###################################################################################
# 
#    Copyright (C) 2017 MuK IT GmbH
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

import json
import base64
import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

class BackendController(http.Controller):
    
    @http.route('/utils/attachment/add', type='http', auth="user", methods=['POST'])
    def add_attachment(self, ufile=None, **kw):
        content = ufile.read()
        attachment = request.env['ir.attachment'].create({
            'name': "Access Attachment: %s" % ufile.filename,
            'datas': base64.b64encode(content),
            'datas_fname': ufile.filename,
            'type': 'binary',
            'public': False,
        })
        attachment.generate_access_token()
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        result = attachment.read(['name', 'datas_fname', 'mimetype', 'checksum', 'access_token'])[0]
        result['url'] = '%s/web/content/%s?access_token=%s' % (base_url, attachment.id, attachment.access_token)
        return json.dumps(result)
    
    @http.route('/utils/attachment/remove', type='http', auth="user", methods=['POST'])
    def remove_attachment(self, id, **kw):
        return json.dumps(request.env['ir.attachment'].browse(id).unlink())
        