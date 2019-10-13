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

import io
import logging
import mimetypes

from odoo import models

_logger = logging.getLogger(__name__)


class IrHttp(models.AbstractModel):

    _inherit = "ir.http"

    # ----------------------------------------------------------
    # Helper
    # ----------------------------------------------------------

    def _check_streamable(record, field):
        return False

    def _stream_content(
        self,
        record,
        field="content",
        filename=None,
        filename_field="content_fname",
        default_mimetype="application/octet-stream",
    ):
        if self._check_streamable(record, field):
            mimetype = "mimetype" in record and record.mimetype or False
            filehash = "checksum" in record and record["checksum"] or False
            stream = record.with_context({"stream": True})[field] or io.BytesIO()
            if not filename:
                if filename_field in record:
                    filename = record[filename_field]
                if not filename:
                    filename = "{}-{}-{}".format(record._name, record.id, field)
            if not mimetype and filename:
                mimetype = mimetypes.guess_type(filename)[0]
            if not mimetype:
                mimetype = default_mimetype
            _, existing_extension = os.path.splitext(filename)
            if not existing_extension:
                extension = mimetypes.guess_extension(mimetype)
                if extension:
                    filename = "{}{}".format(filename, extension)
            if not filehash and stream:
                filehash = record.with_context({"checksum": True})[field]
            return stream and 200 or 404, stream, filename, mimetype, filehash
        return (404, [], None)

    # ----------------------------------------------------------
    # Functions
    # ----------------------------------------------------------

    def binary_stream(
        self,
        xmlid=None,
        model=None,
        id=None,
        field="content",
        unique=False,
        filename=None,
        filename_field="content_fname",
        download=False,
        mimetype=None,
        default_mimetype="application/octet-stream",
        access_token=None,
    ):
        """ Get file, attachment or downloadable content

            If the ``xmlid`` and ``id`` parameter is omitted, fetches the default value for the
            binary field (via ``default_get``), otherwise fetches the field for
            that precise record.

            :param str xmlid: xmlid of the record
            :param str model: name of the model to fetch the binary from
            :param int id: id of the record from which to fetch the binary
            :param str field: binary field
            :param bool unique: add a max-age for the cache control
            :param str filename: choose a filename
            :param str filename_field: if not create an filename with model-id-field
            :param bool download: apply headers to download the file
            :param str mimetype: mintype of the field (for headers)
            :param str default_mimetype: default mintype if no mintype found
            :param str access_token: optional token for unauthenticated access
            :returns: (status, headers, content)
        """
        record, status = self._get_record_and_check(
            xmlid=xmlid, model=model, id=id, field=field, access_token=access_token
        )
        if not record:
            return (status or 404, [], None)
        status, stream, filename, mimetype, filehash = self._stream_content(
            record,
            field=field,
            filename=filename,
            filename_field=filename_field,
            default_mimetype="application/octet-stream",
        )
        status, headers, stream = self._binary_set_headers(
            status,
            stream,
            filename,
            mimetype,
            unique,
            filehash=filehash,
            download=download,
        )
        return status, headers, stream
