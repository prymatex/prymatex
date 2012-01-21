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
    
def textToObjectName(text, sufix = "", prefix = ""):
    """
    &Text Button name -> %{prefix}TextButtonName%{sufix}
    """
    words = text.split(' ')
    name = ''.join(map(to_ascii_cap, words))
    return prefix + name + sufix

def createQAction(settings, parent):
    title = settings.get("title", "Action Title")
    icon = settings.get("icon")
    shortcut = settings.get("shortcut")
    checkable = settings.get("checkable", False)
    callback = settings.get("callback")
    testChecked = settings.get("testChecked")
    action = QtGui.QAction(title, parent)
    object_name = textToObjectName(title, prefix = "action")
    action.setObjectName(object_name)
    if icon is not None:
        action.setIcon(icon)
    if shortcut is not None:
        action.setShortcut(shortcut)
    action.setCheckable(checkable)
    action.testChecked = testChecked
    action.callback = callback
    return action
    
def createQMenu(settings, parent):
    """
    settings = {
            "title": "Menu Title",
            "icon": "resourece icon key"
            "items": [
                action1, action2, 
                {"title": "SubMenu Title",
                 "items": [
                    (gaction1, qaction2, qaction3),
                    [gaction1, qaction2, qaction3],
                    ["Action Title", "Sortcuts", QIcon, callback],
                    "-", action1, action2
                ]}
                action3, "-", action4
            ]
        }
    """
    actions = []
    title = settings.get("title", "Menu Title")
    icon = settings.get("icon")
    items = settings.get("items")
    menu = QtGui.QMenu(title, parent)
    object_name = textToObjectName(title, prefix = "menu")
    menu.setObjectName(object_name)
    if icon is not None:
        menu.setIcon(icon)
    #actions.append(menu.defaultAction())
    if items is not None:
        subactions = extendQMenu(menu, items)
        actions.extend(subactions)
    return menu, actions

def extendQMenu(menu, items):
    actions = []
    for item in items:
        if item == "-":
            action = menu.addSeparator()
            actions.append(action)
        elif isinstance(item, dict) and 'items' in item:
            submenu, subactions = createQMenu(item, menu)
            subaction = menu.addMenu(submenu)
            actions.append(subaction)
            actions.extend(subactions)
        elif isinstance(item, dict):
            action = createQAction(item, menu)
            actions.append(action)
            menu.addAction(action)
        elif isinstance(item, QtGui.QAction):
            menu.addAction(item)
        elif isinstance(item, list):
            actionGroup = QtGui.QActionGroup(menu)
            actions.append(actionGroup)
            actionGroup.setExclusive(True)
            map(menu.addAction, item)
            map(lambda action: action.setActionGroup(actionGroup), item)
        elif isinstance(item, tuple):
            actionGroup = QtGui.QActionGroup(menu)
            actions.append(actionGroup)
            actionGroup.setExclusive(False)
            map(menu.addAction, item)
            map(lambda action: action.setActionGroup(actionGroup), item)
        else:
            raise Exception("%s" % item)
    return actions

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