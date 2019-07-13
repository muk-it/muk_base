###################################################################################
#
#    MuK Document Management System
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
import mimetypes

import odoo
from odoo import api, models, _
from odoo.exceptions import AccessError

from odoo.addons.muk_fields_lobject.fields.lobject import LargeObject

_logger = logging.getLogger(__name__)

class LObjectIrAttachment(models.Model):

    _inherit = 'ir.attachment'

    store_lobject = LargeObject(
        string="Data")

    def _force_storage_prepare_chunks(self):
        """ Technical method to select attachments that need to be migrated
            This method automaticaly splits attachment by chunks,
            to speed up migration.

            :return list: list of chunks where each chunk is list of attachment ids
                          [[1,2,3],[40, 42, 12,33], ...]
        """
        CHUNK_SIZE = 100
        attachments = self.search(['|', ['res_field', '=', False], ['res_field', '!=', False]])
        storage = self._storage()
        chunks = []
        current_chunk = []
        for attach in attachments:
            # Detect storage_type of attachment
            if attach.db_datas:
                current = 'db'
            elif attach.store_lobject:
                current = 'lobject'
            elif attach.store_fname:
                current = 'file'
            else:
                current = None

            if storage != current:
                # This attachment needs migration, thus adding it to result
                current_chunk += [attach.id]
                if len(current_chunk) >= CHUNK_SIZE:
                    chunks += [current_chunk]
                    current_chunk = []

        if current_chunk:
            chunks += [current_chunk]
        return chunks

    @api.model
    def force_storage(self):
        if not self.env.user._is_admin():
            raise AccessError(_('Only administrators can execute this action.'))

        # Do migration by chunks to make it faster.
        chunks_to_migrate = self._force_storage_prepare_chunks()
        for chunk_index, chunk in enumerate(self._force_storage_prepare_chunks()):
            # Here we need to precess each chunk in new transaction.
            # When all attachments in chunk processed, then commit.
            # In case of any errors - rollback
            with api.Environment.manage():
                with odoo.registry(self.env.cr.dbname).cursor() as new_cr:
                    new_env = api.Environment(new_cr, self.env.uid,
                                              self.env.context.copy())
                    attachments = new_env['ir.attachment'].browse(chunk)
                    try:
                        for index, attach in enumerate(attachments):
                            _logger.info(
                                "Migrate Attachment %s of %s [chunk %s of %s]",
                                    index, len(attachments),
                                    chunk_index, len(chunks_to_migrate))
                            attach.write({'datas': attach.datas})
                    except Exception:
                        _logger.error(
                            "Cannot migrate attachments.", exc_info=True)
                        new_cr.rollback()
                        raise
                    else:
                        new_cr.commit()

    @api.depends('store_fname', 'db_datas', 'store_lobject')
    def _compute_datas(self):
        bin_size = self._context.get('bin_size')
        for attach in self:
            if attach.store_lobject:
                if bin_size:
                    attach.datas = attach.store_lobject
                else:
                    attach.datas = attach.with_context({'base64': True}).store_lobject
            else:
                super(LObjectIrAttachment, attach)._compute_datas()

    def _inverse_datas(self):
        location = self._storage()
        for attach in self:
            if location == 'lobject':
                value = attach.datas
                bin_data = base64.b64decode(value) if value else b''
                vals = {
                    'file_size': len(bin_data),
                    'checksum': self._compute_checksum(bin_data),
                    'index_content': self._index(bin_data, attach.datas_fname, attach.mimetype),
                    'store_fname': False,
                    'db_datas': False,
                    'store_lobject': bin_data,
                }
                fname = attach.store_fname
                super(LObjectIrAttachment, attach.sudo()).write(vals)
                if fname:
                    self._file_delete(fname)
            else:
                super(LObjectIrAttachment, attach)._inverse_datas()
                # It is required to set 'store_lobject' to false, because it is
                # used in muk_dms_attachment to detect storage type of
                # attachment, thus it is impossible to detect attachments that
                # need migration 'LObject -> File' or 'LObject -> smthng'
                attach.write({'store_lobject': False})

    def _compute_mimetype(self, values):
        mimetype = super(LObjectIrAttachment, self)._compute_mimetype(values)
        if not mimetype or mimetype == 'application/octet-stream':
            mimetype = None
            for attach in self:
                if attach.mimetype:
                    mimetype = attach.mimetype
                if not mimetype and attach.datas_fname:
                    mimetype = mimetypes.guess_type(attach.datas_fname)[0]
        return mimetype or 'application/octet-stream'