#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
    9: QtCore.Qt.Key_Backspace,
    10: QtCore.Qt.Key_Return,
    127: QtCore.Qt.Key_Delete,
    63232: QtCore.Qt.Key_F1,
    63234: QtCore.Qt.Key_F2,
    #63233: QtCore.Qt.Key_F3,
    63235: QtCore.Qt.Key_F11, #No se que es
    63236: QtCore.Qt.Key_F11, #No se que es
    63238: QtCore.Qt.Key_F3, #No se que es
    63240: QtCore.Qt.Key_F5,
    63272: QtCore.Qt.Key_F7
}

KEYMAP = get_keymap_table()

def _keyboard_layout_keys(key):
    shift = False
    for _, keysyms in KEYMAP.iteritems():
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
        nemonic.append(u"^")
    if sequence & QtCore.Qt.ALT:
        nemonic.append(u"~")
    if sequence & QtCore.Qt.SHIFT:
        nemonic.append(u"$")
    if sequence & QtCore.Qt.META:
        nemonic.append(u"@")
    key = unichr(sequence & 0xFFFF)
    if key in string.uppercase and u"$" in nemonic:
        nemonic.remove(u"$")
        nemonic.append(key)
        return u"".join(nemonic)
    elif key in string.uppercase and u"$" not in nemonic:
        nemonic.append(key.lower())
        return u"".join(nemonic)
    elif u"$" not in nemonic:
        for orig, qtcode in QTCHARCODES.iteritems():
            if sequence & qtcode == qtcode:
                key = unichr(orig)
        nemonic.append(key)
        return u"".join(nemonic)
    else:
        #Seguro que apreto shift
        shift, code = _keyboard_layout_keys(key)
        if shift:
            nemonic.remove(u"$")
            nemonic.append(key)
            return u"".join(nemonic)
        else:
            for orig, qtcode in QTCHARCODES.iteritems():
                if sequence & qtcode == qtcode:
                    key = unichr(orig)
            nemonic.append(key)
            return u"".join(nemonic)

def _keyboard_layout_qtkeys(character):
    keys = []

    for _, keysyms in KEYMAP.iteritems():
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
    if u"^" in nemonic:
        sequence.append(QtCore.Qt.CTRL)
        nemonic.remove(u"^")
    if u"~" in nemonic:
        sequence.append(QtCore.Qt.ALT)
        nemonic.remove(u"~")
    if u"$" in nemonic:
        sequence.append(QtCore.Qt.SHIFT)
        nemonic.remove(u"$")
    if u"@" in nemonic:
        sequence.append(QtCore.Qt.META)
        nemonic.remove(u"@")
    if len(nemonic) == 1:
        keys = _keyboard_layout_qtkeys(nemonic.pop())
        if QtCore.Qt.SHIFT in keys and QtCore.Qt.SHIFT in sequence:
            keys.remove(QtCore.Qt.SHIFT)
        sequence.extend(keys)
    return sum(sequence)

if __name__ == '__main__':
    tests = ['@r', '^~P', '@&', '@~)']
    for test in tests:
        code = keyequivalent2keysequence(test)
        print "Code %d is sequence %s and nemonic is %s" % (code, QtGui.QKeySequence(code).toString(), buildKeyEquivalent(code))
