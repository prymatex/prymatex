#!/usr/bin/env python
# encoding: utf-8

import unittest
from prymatex.utils import plist

class PlistTests(unittest.TestCase):
    def setUp(self):
        self.plist_files = [
            './prymatex/share/Bundles/latex.tmbundle/Preferences/Symbol list.plist',
        ]

    def test_writePlistToString(self):
        data = {
            "dict": {}, 
            "int":1, 
            "str": "hello world", 
            "list_of_ints": [1,2,3,4,5],
            "list_of_str": "hello world of prymatex".split()
            }
        string = plist.writePlistToString(data)
        self.assertEqual(plist.readPlistFromString(string), data)
        
    def test_readPlistFromString(self):
        data = {
            "dict": {}, 
            "int":1, 
            "str": "hello world", 
            "list_of_ints": [1,2,3,4,5],
            "list_of_str": "hello world of prymatex".split()
            }
        string = plist.writePlistToString(data)
        self.assertEqual(plist.readPlistFromString(string), data)

    def test_writePlist(self):
        pass
        
    def test_readPlist(self):
        for plistPath in self.plist_files:
            with open(plistPath) as plistFile:
                content = plistFile.read()
                data = plist.readPlist(plistPath)
                print(plist.writePlistToString(data))
                self.assertEqual(content, plist.writePlistToString(data))

        