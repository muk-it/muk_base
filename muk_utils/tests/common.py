###################################################################################
# 
#    Copyright (C) 2017 MuK IT GmbH
#
#    Odoo Proprietary License v1.0
#    
#    This software and associated files (the "Software") may only be used 
#    (executed, modified, executed after modifications) if you have
#    purchased a valid license from the authors, typically via Odoo Apps,
#    or if you have received a written agreement from the authors of the
#    Software (see the COPYRIGHT file).
#    
#    You may develop Odoo modules that use the Software as a library 
#    (typically by depending on it, importing it and using its resources),
#    but without copying any source code or material from the Software.
#    You may distribute those modules under the license of your choice,
#    provided that this license is compatible with the terms of the Odoo
#    Proprietary License (For example: LGPL, MIT, or proprietary licenses
#    similar to this one).
#    
#    It is forbidden to publish, distribute, sublicense, or sell copies of
#    the Software or modified copies of the Software.
#    
#    The above copyright notice and this permission notice must be included
#    in all copies or substantial portions of the Software.
#    
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#    OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#    DEALINGS IN THE SOFTWARE.
#
###################################################################################

import os
import time
import hmac
import hashlib
import logging
import functools
import traceback

from odoo.tests import common, HOST, PORT

_path = os.path.dirname(os.path.dirname(__file__))
_logger = logging.getLogger(__name__)

#----------------------------------------------------------
# Decorators
#----------------------------------------------------------

def multi_users(users=[['base.user_root', True], ['base.user_admin', True]], reset=True, raise_exception=True):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            user_list = users(self) if callable(users) else users
            test_results = []
            for user in user_list:
                self.cr.execute('SAVEPOINT test_multi_users')
                try:
                    if not isinstance(user[0], int):
                        self.uid = self.ref(user[0])
                    else:
                        self.uid = user[0]
                    func(self, *args, **kwargs)
                except Exception as error:
                    test_results.append({
                        'user': user[0], 
                        'expect': user[1],
                        'result': False,
                        'error': error,
                    })
                else:
                    test_results.append({
                        'user': user[0], 
                        'expect': user[1],
                        'result': True,
                        'error': None,
                    })
                if reset:
                    self.env.cache.invalidate()
                    self.registry.clear_caches()
                    self.registry.reset_changes()
                    self.cr.execute('ROLLBACK TO SAVEPOINT test_multi_users')
                else:
                    self._cr.execute('RELEASE SAVEPOINT test_multi_users')
            test_fails = []
            for result in test_results:
                if result['expect'] != result['result']:
                    message = "Test (%s) with user (%s) failed!"
                    _logger.info(message % (func.__name__, result['user']))
                    if result['error']:
                        _logger.error(result['error'], exc_info=True)
                    test_fails.append(result)
            if test_fails:
                message = "%s out of %s tests failed" % (len(test_fails), len(test_results))
                if raise_exception:
                    raise test_fails[0]['error']
                else:
                    _logger.info(message)
            return test_results
        return wrapper
    return decorator

#----------------------------------------------------------
# Test Cases
#----------------------------------------------------------

class HttpCase(common.HttpCase):
    
    def csrf_token(self, time_limit=3600):
        token = self.session.sid
        max_ts = '' if not time_limit else int(time.time() + time_limit)
        msg = '%s%s' % (token, max_ts)
        secret = self.env['ir.config_parameter'].sudo().get_param('database.secret')
        assert secret, "CSRF protection requires a configured database secret"
        hm = hmac.new(secret.encode('ascii'), msg.encode('utf-8'), hashlib.sha1).hexdigest()
        return '%so%s' % (hm, max_ts)
    
    def url_open(self, url, data=None, timeout=10, csrf=False):
        if url.startswith('/'):
            url = "http://%s:%s%s" % (HOST, PORT, url)
        if data:
            if csrf:
                data.update({'csrf_token': self.csrf_token()})
            return self.opener.post(url, data=data, timeout=timeout)
        return self.opener.get(url, timeout=timeout)
    
    