#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string

from prymatex.qt import QtCore, QtGui

from prymatex.utils.decorators.memoize import memoized
from prymatex.utils.modmap import get_keymap_table

def keybinding(attr):
    """Return keybinding"""
    ks = getattr(QtGui.QKeySequence, attr)
    return QtGui.QKeySequence.keyBindings(ks)[0]
    
#======================
# Key Equivalents
#======================
QTCHARCODES = {
    0: QtCore.Qt.Key_Escape,
    8: QtCore.Qt.Key_Backspace,
    9: QtCore.Qt.Key_Tab,
    10: QtCore.Qt.Key_Return,
    127: QtCore.Qt.Key_Delete,
    63232: QtCore.Qt.Key_F1,
    63233: QtCore.Qt.Key_F3,
    63234: QtCore.Qt.Key_F2,
    63235: QtCore.Qt.Key_F11, #No se que es
    63236: QtCore.Qt.Key_F11, #No se que es
    63238: QtCore.Qt.Key_F3, #No se que es
    63240: QtCore.Qt.Key_F5,
    63272: QtCore.Qt.Key_F7
}

KEYMAP = get_keymap_table()

def _keyboard_layout_keys(key):
    shift = False
    for _, keysyms in KEYMAP.items():
        if key == keysyms[1]:
            return (True, key)
    return (shift, key)

""" Convert nemonics to qt key sequences
* Meta -> (cinta de 4 esquinas) -> arroba (@)
* Control es ^
* Shift es la $
* Backspace -> ^?
* supr -> ?M-^\?
* Alt -> ~
"""
@memoized
def keysequence2keyequivalent(sequence):
    nemonic = []
    if sequence & QtCore.Qt.CTRL:
        nemonic.append("^")
    if sequence & QtCore.Qt.ALT:
        nemonic.append("~")
    if sequence & QtCore.Qt.SHIFT:
        nemonic.append("$")
    if sequence & QtCore.Qt.META:
        nemonic.append("@")
    key = chr(sequence & 0xFFFF)
    # TODO Refactorizar esto que es un asco
    if key in string.ascii_uppercase and "$" in nemonic:
        nemonic.remove("$")
        nemonic.append(key)
        return "".join(nemonic)
    elif key in string.ascii_uppercase and "$" not in nemonic:
        nemonic.append(key.lower())
        return "".join(nemonic)
    elif "$" not in nemonic:
        for orig, qtcode in QTCHARCODES.items():
            if sequence & qtcode == qtcode:
                key = chr(orig)
        nemonic.append(key)
        return "".join(nemonic)
    else:
        #Seguro que apreto shift
        shift, code = _keyboard_layout_keys(key)
        if shift:
            nemonic.remove("$")
            nemonic.append(key)
            return "".join(nemonic)
        else:
            for orig, qtcode in QTCHARCODES.items():
                if sequence & qtcode == qtcode:
                    key = chr(orig)
            nemonic.append(key)
            return "".join(nemonic)

def _keyboard_layout_qtkeys(character):
    keys = []

    for _, keysyms in KEYMAP.items():
        if character == keysyms[1]:
            keys.append(QtCore.Qt.SHIFT) #Add Shift
    code = ord(character.upper())
    if code in QTCHARCODES:
        code = QTCHARCODES[code]
    keys.append(code)
    return keys

@memoized    
def keyequivalent2keysequence(nemonic):
    nemonic = list(nemonic)
    sequence = []
    if "^" in nemonic:
        sequence.append(QtCore.Qt.CTRL)
        nemonic.remove("^")
    if "~" in nemonic:
        sequence.append(QtCore.Qt.ALT)
        nemonic.remove("~")
    if "$" in nemonic:
        sequence.append(QtCore.Qt.SHIFT)
        nemonic.remove("$")
    if "@" in nemonic:
        sequence.append(QtCore.Qt.META)
        nemonic.remove("@")
    if len(nemonic) == 1:
        keys = _keyboard_layout_qtkeys(nemonic.pop())
        if QtCore.Qt.SHIFT in keys and QtCore.Qt.SHIFT in sequence:
            keys.remove(QtCore.Qt.SHIFT)
        sequence.extend(keys)
    return QtGui.QKeySequence(sum(sequence))