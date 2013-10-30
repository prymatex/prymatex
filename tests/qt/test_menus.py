#!/usr/bin/env python
# encoding: utf-8

import unittest

from prymatex.qt import QtGui, QtCore
from prymatex.qt.helpers.menus import (create_menu, extend_menu)

class MenusTests(unittest.TestCase):
    def setUp(self):
        self.qApp = QtGui.QApplication([])

    def test_create_menu(self):
        menu, actions = create_menu(None, {"text": "Menu"})
        print(actions)
        actions = extend_menu(menu, [ {"text": "Hola"} ])
        print(actions)
        menu.show()
    
    def test_extend_menu(self):
        pass
        