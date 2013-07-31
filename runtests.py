#!/usr/bin/env python
# encoding: utf-8

import unittest
from tests.qt.test_keysequences import KeySequencesTests
from tests.test_support import TestSupportFunctions
from tests.test_scope import ScopeSelectorTests
from tests.test_plist import PlistTests

def suite():
    #qtSuite = unittest.makeSuite(KeySequencesTests,'test')
    supportSuite = unittest.TestSuite()
    supportSuite.addTest(PlistTests("test_readPlist"))
    #supportSuite.addTest(ScopeSelectorTests("test_none_selector"))
    return unittest.TestSuite([ supportSuite ])
    
if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
