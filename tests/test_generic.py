# -*- coding: utf-8 -*-
from unittest import TestCase
import os
import glob


class GenericTestCase(TestCase):
    maxDiff = None

    def test_simple(self):
        modules = []
        import rest_framework_helpers
        lib_path = os.path.dirname(os.path.dirname(rest_framework_helpers.__file__))

        for module_file in glob.glob(os.path.join(lib_path, 'rest_framework_helpers', "**", "*.py")):
            module_name = os.path.splitext(os.path.relpath(module_file, lib_path).replace('/', '.'))[0]
            modules.append(__import__(module_name))

        self.assertTrue(modules)
