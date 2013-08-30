#!/usr/bin/env python
# encoding: utf-8

import unittest
from prymatex.utils import osextra

class OsExtraTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_paths(self):
        self.assertEqual(osextra.to_valid_name("$name of %path /and"), "name of path and")
        