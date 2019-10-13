###################################################################################
#
#    Copyright (c) 2017-2019 MuK IT GmbH.
#
#    This file is part of MuK Utils
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

import base64
import logging

from odoo.addons.muk_utils.tools import http
from odoo.tests import common

_logger = logging.getLogger(__name__)


class HttpTestCase(common.TransactionCase):
    def test_decode_http_basic_authentication(self):
        credentials = base64.b64encode(b"username:password").decode("ascii")
        res = http.decode_http_basic_authentication("Basic {}".format(credentials))
        self.assertEqual(res, ("username", "password"))
