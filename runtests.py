#!/usr/bin/env python
# encoding: utf-8

import unittest
from tests.qt.test_keysequences import KeySequencesTests
from tests.test_support import TestSupportFunctions

def suite():
    #qtSuite = unittest.makeSuite(KeySequencesTests,'test')
    supportSuite = unittest.TestSuite()
    supportSuite.addTest(TestSupportFunctions("test_syntax"))
    return unittest.TestSuite([ supportSuite ])
    
if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
