#!/usr/bin/env python
# encoding: utf-8

import unittest

from prymatex.qt import QtGui, QtCore
from prymatex.qt.helpers.keysequences import (keysequence_to_keyequivalent, keyequivalent_to_keysequence)

class KeySequencesTests(unittest.TestCase):
    def setUp(self):
        self.keyTestData = [('@r', QtCore.Qt.META + QtCore.Qt.Key_R), 
            ('^~P', QtCore.Qt.ALT + QtCore.Qt.CTRL + QtCore.Qt.SHIFT + QtCore.Qt.Key_P), 
            ('@&', QtCore.Qt.META + QtCore.Qt.SHIFT + QtCore.Qt.Key_Ampersand ), 
            ('@~)', QtCore.Qt.META + QtCore.Qt.SHIFT + QtCore.Qt.ALT + QtCore.Qt.Key_ParenRight )]

    def test_keysequence_to_keyequivalent(self):
        for keyeq, keysec in self.keyTestData:
            self.assertEqual(set(keyeq), set(keysequence_to_keyequivalent(keysec)))
    
    def test_keyequivalent_to_keysequence(self):
        for keyeq, keysec in self.keyTestData:
            self.assertEqual(keyequivalent_to_keysequence(keyeq), keysec)
        