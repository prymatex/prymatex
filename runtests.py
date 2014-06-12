#!/usr/bin/env python
# encoding: utf-8

import unittest
from tests.qt.test_keysequences import KeySequencesTests
from tests.qt.test_menus import MenusTests
from tests.test_support import SupportTests
from tests.test_scope import ScopeSelectorTests
from tests.test_regexp import RegexpTests
from tests.test_plist import PlistTests
from tests.test_osextra import OsExtraTests

def suite():
    return unittest.TestSuite([ 
        #unittest.makeSuite(KeySequencesTests, 'test'),
        #unittest.makeSuite(MenusTests, 'test'),
        #unittest.makeSuite(SupportTests, 'test_bundleitems'),
        unittest.makeSuite(ScopeSelectorTests, 'test'),
        #unittest.makeSuite(RegexpTests, 'test_symbol_transformation'),
        #unittest.makeSuite(PlistTests, 'test'),
        #unittest.makeSuite(OsExtraTests, 'test')
    ])

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
