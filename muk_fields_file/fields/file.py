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

import os
import re
import base64
import hashlib
import logging
import binascii
import tempfile

from odoo import fields, tools
from odoo.tools import human_size, config

from odoo.addons.muk_utils.tools.file import ensure_path_directories

_logger = logging.getLogger(__name__)

class File(fields.Field):
    
    type = 'file'
    column_type = ('varchar', 'varchar')
    _slots = {
        'prefetch': False,              
        'context_dependent': True,      
    }
    
    def _get_store_path(self, dbname):
        return os.path.join(config.get('data_dir'), 'files', dbname)

    def _get_file_path(self, checksume, dbname):
        name =  "%s/%s" % (checksume[:2], checksume)
        name = re.sub('[.]', '', name).strip('/\\')
        filestore = self._get_store_path(dbname)
        path = os.path.join(filestore, name)
        ensure_path_directories(path)
        return path 
    
    def _get_checksum(self, value):
        if isinstance(value, bytes):
            return hashlib.sha1(value).hexdigest()
        else:
            checksum = hashlib.sha1()
            while True:
                chunk = value.read(4096)
                if not chunk:
                    return checksum.hexdigest()
                checksum.update(chunk)
    
    def _add_to_checklist(self, path):
        print(path)
        pass
    
    def convert_to_column(self, value, record, values=None, validate=True):
        current_path = record.with_context({'path': True})[self.name]
        if current_path:
            self._add_to_checklist(current_path)
        if not value:
            return None
        binary = None
        if isinstance(value, bytes):
            binary = value
        elif isinstance(value, str):
            binary = base64.b64decode(value)
        if binary:
            checksume = self._get_checksum(binary)
            path = self._get_file_path(checksume, record.env.cr.dbname)
            with open(path, 'wb') as file:
                file.write(binary)
            self._add_to_checklist(path)
        else:
            checksume = self._get_checksum(value)
            path = self._get_file_path(checksume, record.env.cr.dbname)
            value.seek(0, 0)
            with open(path, 'wb') as file:
                while True:
                    chunk = value.read(4096)
                    if not chunk:
                        break
                    file.write(chunk)
            self._add_to_checklist(path)
        return path

    def convert_to_record(self, value, record):
        if value and isinstance(value, str) and os.path.exists(value):
            with open(value, 'rb') as file:
                if record._context.get('human_size'):
                    return human_size(file.seek(0, 2))
                elif record._context.get('bin_size'):
                    return file.seek(0, 2)
                elif record._context.get('path'):
                    return value
                elif record._context.get('base64'):
                    return base64.b64encode(file.read())
                elif record._context.get('stream'):
                    temp = tempfile.TemporaryFile()
                    while True:
                        chunk = file.read(4096)
                        if not chunk:
                            temp.seek(0)
                            return file
                        temp.write(chunk)
                elif record._context.get('checksum'):
                    checksum = hashlib.sha1()
                    while True:
                        chunk = file.read(4096)
                        if not chunk:
                            return checksum.hexdigest()
                        checksum.update(chunk)
                else:
                    return file.read()
        return value
    
    def convert_to_export(self, value, record):
        if value:
            with open(value, 'rb') as file:
                if record._context.get('export_raw_data'):
                    return file.read()
                return base64.b64encode(file.read())
        return ''