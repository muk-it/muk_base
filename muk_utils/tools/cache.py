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

import time

class memoize(object):
    _caches = {}
    _timeouts = {}

    def __init__(self, timeout=2):
        self.timeout = timeout

    def collect(self):
        for func in self._caches:
            cleaned_cache = {}
            current_time = time.time()
            for key in self._caches[func]:
                if (current_time - self._caches[func][key][1]) < self._timeouts[func]:
                    cleaned_cache[key] = self._caches[func][key]
            self._caches[func] = cleaned_cache

    def __call__(self, func):
        self.cache = self._caches[func] = {}
        self._timeouts[func] = self.timeout
        def wrapper(*args, **kwargs):
            current_time = time.time()
            kw = sorted(kwargs.items())
            key = (args, tuple(kw))
            try:
                value = self.cache[key]
                if (current_time - value[1]) > self.timeout:
                    raise KeyError
            except KeyError:
                value = self.cache[key] = (func(*args,**kwargs), current_time)
            return value[0]
        wrapper.func_name = func.__name__
        return wrapper