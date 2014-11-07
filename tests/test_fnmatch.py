#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

import re
import unittest
from prymatex.utils.fnmatch import fnmatch, translate

class FnmatchTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_match(self):
        t1 = translate("*.{icns,ico,jpg,jpeg,m4v,nib,pdf,png,psd,pyc,rtf,tif,tiff,xib}")
        p1 = re.compile(t1)
        t2 = translate("/System/Library/Frameworks/**/Headers/**/*")
        p2 = re.compile(t2)
        print(p1.search("/path/to/icon/myicon.jpg"))
        print(p2.search("/System/Library/Frameworks/hola/Headers/uno/dos.h"))
        self.assertTrue(fnmatch("", ""))
        self.assertTrue(fnmatch("/path/to/icon/myicon.ico", "*.{icns,ico,jpg,jpeg,m4v,nib,pdf,png,psd,pyc,rtf,tif,tiff,xib}"))
        self.assertTrue(fnmatch("", ""))
