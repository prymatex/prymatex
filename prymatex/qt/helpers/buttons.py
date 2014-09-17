#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets

from prymatex.qt.helpers.base import text2objectname
import collections

def create_toolbutton(parent, settings):
    """Create a QToolButton"""
    button = QtWidgets.QToolButton(parent)
    text = settings["text"] if "text" in settings else "No name"
    button.setObjectName(text2objectname(text, prefix = "toolButton"))
    button.setText(text)
    
    # attrs
    if "icon" in settings:
        button.setIcon(settings["icon"])
    if "shortcut" in settings:
        button.setShortcut(settings["shortcut"])
    if "tip" in settings:
        button.setToolTip(settings["tip"])
    if settings.get("text_beside_icon", False):
        button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
    button.setAutoRaise(settings.get("autoraise", True))
    
    if "triggered" in settings and isinstance(settings["triggered"], collections.Callable):
        parent.connect(button, QtCore.SIGNAL("clicked()"), settings["triggered"])
    if "clicked" in settings and isinstance(settings["clicked"], collections.Callable):
        parent.connect(button, QtCore.SIGNAL("clicked()"), settings["clicked"])
    if "toggled" in settings and isinstance(settings["toggled"], collections.Callable):
        parent.connect(button, QtCore.SIGNAL("toggled(bool)"), settings["toggled"])
        button.setCheckable(True)
        
    return button

def action2button(action, autoraise=True, text_beside_icon=False, parent=None):
    """Create a QToolButton directly from a QAction object"""
    if parent is None:
        parent = action.parent()
    button = QtWidgets.QToolButton(parent)
    button.setDefaultAction(action)
    button.setAutoRaise(autoraise)
    if text_beside_icon:
        button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
    return button
