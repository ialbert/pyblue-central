
from __future__ import unicode_literals, print_function

import unittest
from pyblue.main import PyBlue, File
import shutil
import os
import os.path

_folder = os.path.join(os.path.dirname(__file__))
_output = os.path.join(_folder, "output")

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        os.makedirs(_output)
        self.pyblue = PyBlue()

    def tearDown(self):
        self.pyblue = None
        shutil.rmtree(_output)

    def test_static_get(self):
        self.pyblue.set_folder(os.path.join(_folder, "input_static_get"))
        value = self.pyblue.get(File("test.txt", root=self.pyblue.folder))
        self.assertEqual(value.strip(), b"test")

    def test_mako(self):
        self.pyblue.set_folder(os.path.join(_folder, "input_mako"))
        value = self.pyblue.get(File("test.html", root=self.pyblue.folder))
        self.assertEqual(value.strip(), b"3+2=5")

    def test_gen(self):
        self.pyblue.set_folder(os.path.join(_folder, "input_gen"))
        value = self.pyblue.gen_static(_output)
        with open(os.path.join(_output, "test.txt"), "rb") as _file:
            value = _file.read()
        self.assertEqual(value.strip(), b"test")
        with open(os.path.join(_output, "test.html"), "rb") as _file:
            value = _file.read()
        self.assertEqual(value.strip(), b"3+2=5")

    def test_markdown(self):
        self.pyblue.set_folder(os.path.join(_folder, "input_markdown"))
        value = self.pyblue.get(File("test.html", root=self.pyblue.folder))
        self.assertEqual(value.strip(), b"<h1>Test</h1>")

if __name__ == '__main__':
    unittest.main()
