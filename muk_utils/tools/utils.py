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

_logger = logging.getLogger(__name__)

#----------------------------------------------------------
# List Methods
#----------------------------------------------------------

def uniquify_list(seq):
    seen = set()
    return [
        val for val in seq if val not in seen and not seen.add(val)
    ]

#----------------------------------------------------------
# Safe Execute
#----------------------------------------------------------

def safe_execute_exception(default, exception, function, *args, **kwargs):
    try:
        return function(*args, **kwargs)
    except exception:
        return default
    
def safe_execute(default, function, *args, **kwargs):
    return safe_execute_exception(default, Exception, function, *args, **kwargs)