#!/usr/bin/env python
# encoding: utf-8

import unittest

from prymatex.qt import QtGui
from prymatex.qt.helpers.keysequences import (keysequence2keyequivalent, keyequivalent2keysequence)

class KeySequencesTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_keysequence2keyequivalent(self):
        #print keysequence2keyequivalent()
        pass
    
    def test_keyequivalent2keysequence(self):
        tests = ['@r', '^~P', '@&', '@~)']
        for test in tests:
            code = keyequivalent2keysequence(test)
            print (code, QtGui.QKeySequence(code).toString())

        