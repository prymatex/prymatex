#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string

from prymatex.qt import QtCore, QtGui

from prymatex.utils.modmap import get_keymap_table
from .base import text_to_objectname

text_to_sequencesname = text_to_objectname

def keybinding(name):
    """Return keybinding"""
    ks = getattr(QtGui.QKeySequence, name, None)
    if ks is not None:
        bindings = QtGui.QKeySequence.keyBindings(ks)
        if bindings:
            return bindings[0]
    return QtGui.QKeySequence.mnemonic(name)

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
def keysequence_to_keyequivalent(sequence):
    nemonic = []
    for key in sequence:
        seq = []
        if key & QtCore.Qt.CTRL:
            seq.append("^")
        if key & QtCore.Qt.ALT:
            seq.append("~")
        if key & QtCore.Qt.SHIFT:
            seq.append("$")
        if key & QtCore.Qt.META:
            seq.append("@")
        seq.append(chr(key & 0xFFFF))
        if seq[-1] in string.ascii_uppercase and "$" in seq:
            seq.remove("$")
            nemonic.append("".join(seq))
        elif seq[-1] in string.ascii_uppercase and "$" not in seq:
            seq[-1] = seq[-1].lower()
            nemonic.append("".join(seq))
        elif "$" not in seq:
            for orig, qtcode in QTCHARCODES.items():
                if key & qtcode == qtcode:
                    seq[-1] = chr(orig)
            nemonic.append("".join(seq))
        else:
            #Seguro que apreto shift
            shift, code = _keyboard_layout_keys(key)
            if shift:
                seq.remove("$")
                nemonic.append("".join(seq))
            else:
                for orig, qtcode in QTCHARCODES.items():
                    if key & qtcode == qtcode:
                        seq[-1] = chr(orig)
                nemonic.append("".join(seq))
    return ", ".join(nemonic)

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

def keyequivalent_to_keysequence(nemonic):
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
