#!/usr/bin/env python
# encoding: utf-8

import unittest

from prymatex.qt import QtGui, QtCore
from prymatex.qt.helpers.menus import (create_menu, extend_menu)

MENU_SETTINGS = {
    "text": "Menu Uno",
    "items": [{
        "text": "Action Uno",
        "name": "MyAction",     #Custom name = "action" + <name>
    }, {
        "text": "Action Dos"
    }, "-", {
        "text": "Action Tres"
    }, "--Section", {
        "text": "Menu Dos",
        "name": "MyMenu",     #Custom name = "menu" + <name>
        "items": [
            {"text": "Action Cuatro"},
            "-",
            {"text": "Menu Tres", "items": []},
            {"text": "Action Seis"},
        ]
    }]
}

MENU_NAMES = [
    "menuMenuUno",
    "menuMyMenu",
    "menuMenuTres",
]

ACTION_NAMES = [ 
    "actionMenuMenuUno",
    "actionMyAction",
    "actionActionDos",
    "separatorNone",
    "actionActionTres",
    "separatorSection",
    "actionMenuMyMenu",
    "actionActionCuatro",
    "separatorNone",
    "actionMenuMenuTres",
    "actionActionSeis"
]

class MenusTests(unittest.TestCase):
    def setUp(self):
        self.qApp = QtGui.QApplication([])

    def test_create_menu(self):
        menus, actions = create_menu(None, MENU_SETTINGS, allMenus = True)
        self.assertEqual(len(menus), 3)
        self.assertEqual(len(actions), 11)
        
        for menu, name in zip(menus, MENU_NAMES):
            self.assertEqual(menu.objectName(), name)
            
        for action, name in zip(actions, ACTION_NAMES):
            self.assertEqual(action.objectName(), name)

    def test_extend_menu(self):
        pass
        