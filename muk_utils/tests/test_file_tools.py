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

import logging
import os
import shutil
import tempfile

from odoo.addons.muk_utils.tools import file
from odoo.tests import common

_logger = logging.getLogger(__name__)


class FileTestCase(common.TransactionCase):
    def test_check_name(self):
        self.assertTrue(file.check_name("Test"))
        self.assertFalse(file.check_name("T/est"))

    def test_compute_name(self):
        self.assertEqual(file.compute_name("Test", 1, False), "Test(1)")
        self.assertEqual(file.compute_name("Test.png", 1, True), "Test(1).png")

    def test_unique_name(self):
        self.assertEqual(file.unique_name("Test", ["A", "B"]), "Test")
        self.assertEqual(file.unique_name("Test", ["Test"]), "Test(1)")

    def test_unique_files(self):
        files = file.unique_files(
            [("Test.png", b"\xff data"), ("Test.png", b"\xff data")]
        )
        self.assertEqual(
            files, [("Test.png", b"\xff data"), ("Test(1).png", b"\xff data")]
        )

    def test_guess_extension(self):
        self.assertEqual(file.guess_extension(filename="Test.png"), "png")
        self.assertEqual(file.guess_extension(mimetype="image/png"), "png")

    def test_ensure_path_directories(self):
        tmp_dir = tempfile.mkdtemp()
        try:
            path = os.path.join(tmp_dir, "Test/Test/")
            file.ensure_path_directories(path)
            self.assertTrue(os.path.exists(path))
        finally:
            shutil.rmtree(tmp_dir)
        return True

    def test_remove_empty_directories(self):
        tmp_dir = tempfile.mkdtemp()
        try:
            dir = os.path.join(tmp_dir, "Test/")
            path = os.path.join(dir, "Test/")
            os.makedirs(path)
            open(os.path.join(dir, "F"), "ab").close()
            file.remove_empty_directories(path)
            self.assertFalse(os.path.exists(path))
            self.assertTrue(os.path.exists(dir))
        finally:
            shutil.rmtree(tmp_dir)
        return True
