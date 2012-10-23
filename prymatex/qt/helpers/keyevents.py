#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

def keyevent2tuple(event):
    """Convert QKeyEvent instance into a tuple"""
    return (event.type(), event.key(), event.modifiers(), event.text(),
            event.isAutoRepeat(), event.count())
    
def tuple2keyevent(past_event):
    """Convert tuple into a QKeyEvent instance"""
    return QtGui.QKeyEvent(*past_event)

def restore_keyevent(event):
    if isinstance(event, tuple):
        _, key, modifiers, text, _, _ = event
        event = tuple2keyevent(event)
    else:
        text = event.text()
        modifiers = event.modifiers()
        key = event.key()
    ctrl = modifiers & QtCore.Qt.ControlModifier
    shift = modifiers & QtCore.Qt.ShiftModifier
    return event, text, key, ctrl, shift
