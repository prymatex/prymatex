#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import string

from PyQt4 import QtGui, QtCore

from prymatex.utils.i18n import ugettext as _

"""
Algunas definciones en Python para tareas de Gui
"""

to_ascii = lambda s: filter(lambda c: c in string.ascii_letters, s)
to_ascii_cap = lambda s: to_ascii(s).capitalize()

def centerWidget(widget, scale = None):
    """
    Center de widget in the screen
    Scale is a tuple with width and height ex: (0.7, 0.65)
    """
    screen = QtGui.QDesktopWidget().screenGeometry()
    if scale is not None:
        widget.resize(screen.width() * scale[0], screen.height() * scale[1])
    widget.move((screen.width() - widget.size().width()) / 2, (screen.height() - widget.size().height()) / 2)
    
def createObjectName(text, sufix = "", prefix = ""):
    """
    &Text Button name -> %{prefix}TextButtonName%{sufix}
    """
    words = text.split(' ')
    name = ''.join(map(to_ascii_cap, words))
    return prefix + name + sufix

def createQMenu(title, menuItems, parent):
    """
    menuItems = [
            {"title": "New",
             "menuItems": [
                action1, action2, action3, "-", action4
            ]},
            {"title": "Order",
             "menuItems": [
                (gaction1, qaction2, qaction3),
                "-", action1, action2
            ]}
        ]
    """
    menu = QtGui.QMenu(parent)
    object_name = createObjectName(title, sufix = "Menu")
    menu.setObjectName(object_name)
    for item in menuItems:
        if item == "-":
            menu.addSeparator()
        elif isinstance(item, dict):
            for key, value in item.iteritems():
                submenu = createQMenu(key, value, menu)
                menu.addMenu(submenu)
        elif isinstance(item, QtGui.QAction):
            menu.addAction(item)
        elif isinstance(item, tuple):
            actionGroup = QtGui.QActionGroup(menu)
            actionGroup.setExclusive(True)
            map(menu.addAction, item)
            map(lambda action: action.setActionGroup(actionGroup), item)
        else:
            raise Exception("%s" % item)
    return menu

# Key press debugging 
KEY_NAMES = dict([(getattr(QtCore.Qt, keyname), keyname) for keyname in dir(QtCore.Qt) 
                  if keyname.startswith('Key_')])

ANYKEY = -1

def debug_key(key_event):
    ''' Prevents hair loss when debuging what the hell is going on '''
    key = key_event.key()
    mods = []
    print "count: ", key_event.count()
    print "isAutoRepeat: ", key_event.isAutoRepeat()
    print "key: ", key_event.key()
    print "nativeModifiers: ", key_event.nativeModifiers()
    print "nativeScanCode: ", key_event.nativeScanCode()
    print "nativeVirtualKey: ", key_event.nativeVirtualKey()
    print "text: ", unicode(key_event.text()).encode('utf-8')
    print "isAccepted: ", key_event.isAccepted()
    print "modifiers: ", int(key_event.modifiers())
    modifiers = key_event.modifiers()
    if modifiers & QtCore.Qt.AltModifier:
        mods.append("AltModifier")
    if modifiers & QtCore.Qt.ControlModifier:
        mods.append("ControlModifier")
    if modifiers & QtCore.Qt.MetaModifier:
        mods.append("MetaModifier")
    if modifiers & QtCore.Qt.ShiftModifier:
        mods.append("ShiftModifier")
    
    print "%s <%s> Code: %d chr(%d) = %s" % (KEY_NAMES[key],  ", ".join(mods), 
                                              key, key, key < 255 and chr(key) 
                                              or 'N/A')

if __name__ == "__main__":
    print text_to_object_name('Button Text Editor')
    print text_to_object_name('Button Text Editor', 'action')