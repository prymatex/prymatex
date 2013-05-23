#!/usr/bin/env python
# encoding: utf-8

import unittest
from tests.qt.test_keysequences import KeySequencesTests

def suite():
    qtSuite = unittest.makeSuite(KeySequencesTests,'test')
    return unittest.TestSuite([ qtSuite ])
    
if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
