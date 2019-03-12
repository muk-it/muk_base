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
import sys
import time
import logging
import unicodedata

_logger = logging.getLogger(__name__)

#----------------------------------------------------------
# Functions
#----------------------------------------------------------

def slugify(value):
    value = str(unicodedata.normalize('NFKD', value))
    value = str(value.encode('ascii', 'ignore'))
    value = str(re.sub('[^\w\s-]', '', value).strip().lower())
    value = str(re.sub('[-\s]+', '-', value))
    return value

#----------------------------------------------------------
# Decorators
#----------------------------------------------------------

def timeout(func, delay=30):
    def wrapper(*args, **kwargs):
        if args[0]._name in wrapper.timeouts:
            timeout = wrapper.timeouts[args[0]._name]
            if time.time() > timeout + delay:
                wrapper.timeouts[args[0]._name] = time.time()
                return func(*args, **kwargs)
        else:
            wrapper.timeouts[args[0]._name] = time.time()
            return func(*args, **kwargs)
    wrapper.timeouts = {}
    return wrapper