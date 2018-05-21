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
import logging

_logger = logging.getLogger(__name__)

def unique_name(name, names, escape_suffix=False):
    def compute_name(name, suffix, escape_suffix):
        if escape_suffix:
            name, extension = os.path.splitext(name)
            return "%s(%s)%s" % (name, suffix, extension)
        else:
            return "%s(%s)" % (name, suffix)
    if not name in names:
        return name
    else:
        suffix = 1
        name = compute_name(name, suffix, escape_suffix)
        while name in names:
            suffix += 1
            name = compute_name(name, suffix, escape_suffix)
        return name