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

import urllib
import logging

import requests
import werkzeug

from odoo.http import request
from odoo.tools import config

_logger = logging.getLogger(__name__)

def get_route(url):
    url_parts = url.split('?')
    path = url_parts[0]
    query_string = url_parts[1] if len(url_parts) > 1 else None
    router = request.httprequest.app.get_db_router(request.db).bind('')
    match = router.match(path, query_args=query_string)
    method = router.match(path, query_args=query_string)[0]
    params = dict(urllib.parse.parse_qsl(query_string))
    if len(match) > 1:
        params.update(match[1])
    return method, params, path

def make_error_response(status, message):
    exception = werkzeug.exceptions.HTTPException()
    exception.code = status
    exception.description = message
    return exception

def get_response(url):
    _logger.info(url)
    if not bool(urllib.parse.urlparse(url).netloc):
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        method, params, path = get_route(url)
        params.update({'csrf_token': request.csrf_token()})
        session = requests.Session()
        session.cookies['session_id'] = request.session.sid
        try:
            response = session.post("%s%s" % (base_url, path), params=params, verify=False)
            return response.status_code, response.headers, response.content
        except:
            _logger.info("Trying custom certificate")
            custom_cert = config.get("muk_custom_certificate", False)
            try:
                _logger.info("Using Certificate: {}".format(custom_cert))
                response = session.post("%s%s" % (base_url, path), params=params, verify=custom_cert)
                return response.status_code, response.headers, response.reason
            except:
                try:
                    _logger.info("Custom Certificate didn't work")
                    response = session.post("%s%s" % (base_url, path), params=params, verify=False)
                    return response.status_code, response.headers, response.reason
                except Exception as e:
                    _logger.exception("Request failed!")
                    return 501, [], str(e)
    else:
        try:
            response = requests.get(url)
            return response.status_code, response.headers, response.content
        except requests.exceptions.RequestException as exception:
            try:
                return exception.response.status_code, exception.response.headers, exception.response.reason
            except Exception as e:
                _logger.exception("Request failed!")
                return 501, [], str(e)
    
