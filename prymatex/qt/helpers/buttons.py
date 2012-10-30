#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from prymatex import resources
from prymatex.qt.helpers import text2objectname

def create_toolbutton(parent, settings):
    """Create a QToolButton"""
    button = QtGui.QToolButton(parent)
    text = settings["text"] if settings.has_key("text") else "No name"
    button.setObjectName(text2objectname(text, prefix = "toolButton"))
    button.setText(text)
    
    # attrs
    if settings.has_key("icon"):
        icon = settings["icon"]
        if isinstance(icon, basestring):
            icon = resources.getIcon(icon)
        button.setIcon(icon)
    if settings.has_key("shortcut"):
        button.setShortcut(settings["shortcut"])
    if settings.has_key("tip"):
        button.setToolTip(settings["tip"])
    if settings.get("text_beside_icon", False):
        button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
    button.setAutoRaise(settings.get("autoraise", True))
    
    if settings.has_key("clicked") and callable(settings["clicked"]):
        parent.connect(button, QtCore.SIGNAL("clicked()"), settings["clicked"])
    if settings.has_key("toggled") and callable(settings["toggled"]):
        parent.connect(button, QtCore.SIGNAL("toggled(bool)"), settings["toggled"])
        button.setCheckable(True)
        
    return button


def action2button(action, autoraise=True, text_beside_icon=False, parent=None):
    """Create a QToolButton directly from a QAction object"""
    if parent is None:
        parent = action.parent()
    button = QtGui.QToolButton(parent)
    button.setDefaultAction(action)
    button.setAutoRaise(autoraise)
    if text_beside_icon:
        button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
    return button