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
    return method, params

def make_error_response(status, message):
    exception = werkzeug.exceptions.HTTPException()
    exception.code = status
    exception.description = message
    return exception

def get_response(url):
    if not bool(urllib.parse.urlparse(url).netloc):
        method, params = get_route(url)
        response = method(**params)
        return response.status_code, response.headers, response.data
    else:
        try:
            response = requests.get(url)
            return response.status_code, response.headers, response.content
        except requests.exceptions.RequestException as exception:
            return exception.response.status_code, exception.response.headers, exception.response.reason
    
