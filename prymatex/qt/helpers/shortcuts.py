#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets

from .base import text_to_objectname

import collections

def create_shortcut(parent, settings, dispatcher=None, sequence_handler=None):
    """Create a QAction"""
    shortcut = QtWidgets.QShortcut(parent)
    name = settings.get("name", "None")
    shortcut.setObjectName(text_to_objectname(name, prefix="shortcut"))
    
    # attrs
    sequence = settings.get("sequence", name)
    if sequence_handler is not None:
        sequence_handler(shortcut, sequence)
    elif isinstance(sequence, QtGui.QKeySequence) and not sequence.isEmpty():
        shortcut.setShortcut(sequence)

    if "sequence" in settings:
        sequence = settings["sequence"]
        if sequence_handler is not None:
            sequence_handler(shortcut, sequence)
        elif isinstance(sequence, QtGui.QKeySequence):
            shortcut.setKey(sequence)

    if "context" in settings:
        shortcut.setContext(settings["context"])
        
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
        shortcut.activated.connect(
            isinstance(dispatcher, collections.Callable) and \
            dispatch_signal(dispatcher, shortcut.functionActivated) or \
            shortcut.functionActivated)
        
    # Test functions
    if "testEnabled" in settings and isinstance(settings["testEnabled"], collections.Callable):
        shortcut.testEnabled = settings["testEnabled"]
    
    return shortcut
