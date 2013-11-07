#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from prymatex.qt.helpers.base import text2objectname

import collections

def create_shortcut(parent, settings, dispatcher = None, sequence_handler=None):
    """Create a QAction"""
    shortcut = QtGui.QShortcut(parent)
    name = settings.get("name", "None")
    shortcut.setObjectName(text2objectname(name, prefix = "shortcut"))
    
    # attrs
    if "sequence" in settings:
        sequence = settings["sequence"]
        if sequence_handler is not None:
            sequence_handler(shortcut, sequence)
        elif isinstance(sequence, QtGui.QKeySequence):
            shortcut.setKey(sequence)
    
    # Action functions
    shortcut.functionActivated = None
    if "activated" in settings and isinstance(settings["activated"], collections.Callable):
        shortcut.functionActivated = settings["activated"]
    
    # The signal dispatcher
    def dispatch_signal(dispatcher, handler):
        def _dispatch(*largs):
            dispatcher(handler, *largs)
        return _dispatch

    if shortcut.functionActivated is not None:
        parent.connect(shortcut, QtCore.SIGNAL("activated()"),
            isinstance(dispatcher, collections.Callable) and \
            dispatch_signal(dispatcher, shortcut.functionActivated) or \
            shortcut.functionActivated)
        
    # Test functions
    if "testEnabled" in settings and isinstance(settings["testEnabled"], collections.Callable):
        shortcut.testEnabled = settings["testEnabled"]
    
    shortcut.setContext(settings.get("context", QtCore.Qt.WidgetShortcut))
    
    return shortcut
