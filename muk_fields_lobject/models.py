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

import re
import hashlib
import logging
import psycopg2

from odoo import _
from odoo import models, api, fields
from odoo.tools import ustr, human_size

_logger = logging.getLogger(__name__)


unlink = models.BaseModel.unlink

def large_object_unlink(self):
    oids = []
    for name in self._fields:
        field = self._fields[name]
        if field.type == 'lobject' and field.store:
            for record in self:
                oids.append(record.with_context({'oid': True})[name])
    unlink(self)
    for oid in oids:
        lobject = self.env.cr._cnx.lobject(oid, 'rb').unlink()
    
models.BaseModel.unlink = large_object_unlink