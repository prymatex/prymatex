#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

KEY_NUMBERS = [getattr(QtCore.Qt, keyname) for keyname in [ "Key_%d" % index for index in range(10)]]
KEY_NAMES = dict([(getattr(QtCore.Qt, keyname), keyname) for keyname in dir(QtCore.Qt) if keyname.startswith('Key_')])

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

# Key press debugging 
def debug_key(key_event):
    ''' Prevents hair loss when debuging what the hell is going on '''
    key = key_event.key()
    mods = []
    print("count: ", key_event.count())
    print("isAutoRepeat: ", key_event.isAutoRepeat())
    print("key: ", key_event.key())
    print("nativeModifiers: ", key_event.nativeModifiers())
    print("nativeScanCode: ", key_event.nativeScanCode())
    print("nativeVirtualKey: ", key_event.nativeVirtualKey())
    print("text: ", str(key_event.text()).encode('utf-8'))
    print("isAccepted: ", key_event.isAccepted())
    print("modifiers: ", int(key_event.modifiers()))
    modifiers = key_event.modifiers()
    if modifiers & QtCore.Qt.AltModifier:
        mods.append("AltModifier")
    if modifiers & QtCore.Qt.ControlModifier:
        mods.append("ControlModifier")
    if modifiers & QtCore.Qt.MetaModifier:
        mods.append("MetaModifier")
    if modifiers & QtCore.Qt.ShiftModifier:
        mods.append("ShiftModifier")
    
    print("%s <%s> Code: %d chr(%d) = %s" % (KEY_NAMES[key],  ", ".join(mods), 
                                              key, key, key < 255 and chr(key) 
                                              or 'N/A'))