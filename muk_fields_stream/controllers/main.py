###################################################################################
#
#    Copyright (c) 2017-2019 MuK IT GmbH.
#
#    This file is part of MuK Binary Stream Support
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

import logging

from odoo import http
from odoo.http import request
from werkzeug import wrappers

_logger = logging.getLogger(__name__)


class StreamController(http.Controller):

    # ----------------------------------------------------------
    # Routes
    # ----------------------------------------------------------

    @http.route(
        [
            "/binary/content",
            "/binary/content/<string:xmlid>",
            "/binary/content/<string:xmlid>/<string:filename>",
            "/binary/content/<int:id>",
            "/binary/content/<int:id>/<string:filename>",
            "/binary/content/<int:id>-<string:unique>",
            "/binary/content/<int:id>-<string:unique>/<string:filename>",
            "/binary/content/<int:id>-<string:unique>/<path:extra>/<string:filename>",
            "/binary/content/<string:model>/<int:id>/<string:field>",
            "/binary/content/<string:model>/<int:id>/<string:field>/<string:filename>",
        ],
        type="http",
        auth="public",
    )
    def binary_content(
        self,
        xmlid=None,
        model=None,
        id=None,
        field="content",
        filename=None,
        filename_field="content_fname",
        unique=None,
        mimetype=None,
        download=None,
        token=None,
        access_token=None,
        **kwargs
    ):
        status, headers, stream = request.env["ir.http"].binary_stream(
            xmlid=xmlid,
            model=model,
            id=id,
            field=field,
            unique=unique,
            filename=filename,
            filename_field=filename_field,
            download=download,
            mimetype=mimetype,
            access_token=access_token,
        )
        if status != 200:
            return request.env["ir.http"]._response_by_status(status, headers, False)
        else:
            headers.append(("Content-Length", stream.seek(0, 2)))
            stream.seek(0, 0)
            response = wrappers.Response(
                stream, headers=headers, status=status, direct_passthrough=True
            )
        if token:
            response.set_cookie("fileToken", token)
        return response
