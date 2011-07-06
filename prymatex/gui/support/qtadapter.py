#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, string
sys.path.append(os.path.abspath('../../..'))

try:
    from PyQt4 import QtGui
    from PyQt4.Qt import QKeySequence, Qt
except:
    from prymatex.support.qtmock import Qt, QKeySequence
from prymatex.support.modmap import get_keymap_table
'''
    caret, foreground, selection, invisibles, lineHighlight, gutter, background
    * Meta -> (cinta de 4 esquinas) -> arroba (@)
    * Control es ^
    * Shift es la $
    * Backspace -> ^?
    * supr -> ?M-^\?
    * Alt -> ~
'''

#caret, foreground, selection, invisibles, lineHighbuildQColorlight, gutter, background
def RGBA2QColor(rgbColor):
    '''
    @param rgbColor: A html formated color string i.e.: #RRGGBB or #RRGGBBAA
    @return: If rgbColor is a valid color, a QColor isntance
    ''' 
    rgbColor = unicode(rgbColor).strip('#')
    if len(rgbColor) in [ 6, 8 ]:
        red, green, blue, alpha = rgbColor[0:2], rgbColor[2:4], rgbColor[4:6], rgbColor[6:8]
    else:
        raise ValueError("Invalid Color")
    return QtGui.QColor(int(red, 16), int(green, 16), int(blue, 16), int(alpha or 'FF', 16))

def QColor2RGB(color):
    if isinstance(color, QtGui.QColor):
        pass
    elif isinstance(color, (str, unicode)):
        pass
    elif isinstance(color, int):
        pass
    else:
        raise ValueError("Invalid Color")
    
QTCHARCODES = {9: Qt.Key_Backspace,
               10: Qt.Key_Return,
               #32: Qt.Key_Space,
               127: Qt.Key_Delete,
               63232: Qt.Key_F1,
               63234: Qt.Key_F2,
               63233: Qt.Key_F3,
               63240: Qt.Key_F5,
               63272: Qt.Key_F7}

KEYMAP = get_keymap_table()
def keyboardLayoutQtKeys(character):
    keys = []

    for _, keysyms in KEYMAP.iteritems():
        if character == keysyms[1]:
            keys.append(Qt.SHIFT) #Add Shift
    code = ord(character.upper())
    if code in QTCHARCODES:
        code = QTCHARCODES[code]
    keys.append(code)
    return keys

def keyboardLayoutKeys(key):
    shift = False
    for _, keysyms in KEYMAP.iteritems():
        if key == keysyms[1]:
            return (True, key)
    return (shift, key)

def buildKeyEquivalent(sequence):
    nemonic = []
    if sequence & Qt.CTRL:
        nemonic.append(u"^")
    if sequence & Qt.ALT:
        nemonic.append(u"~")
    if sequence & Qt.SHIFT:
        nemonic.append(u"$")
    if sequence & Qt.META:
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
        shift, code = keyboardLayoutKeys(key)
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
    
def buildKeySequence(nemonic):
    nemonic = list(nemonic)
    sequence = []
    if u"^" in nemonic:
        sequence.append(Qt.CTRL)
        nemonic.remove(u"^")
    if u"~" in nemonic:
        sequence.append(Qt.ALT)
        nemonic.remove(u"~")
    if u"$" in nemonic:
        sequence.append(Qt.SHIFT)
        nemonic.remove(u"$")
    if u"@" in nemonic:
        sequence.append(Qt.META)
        nemonic.remove(u"@")
    if len(nemonic) == 1:
        keys = keyboardLayoutQtKeys(nemonic.pop())
        if Qt.SHIFT in keys and Qt.SHIFT in sequence:
            keys.remove(Qt.SHIFT)
        sequence.extend(keys)
    return sum(sequence)

if __name__ == '__main__':
    tests = ['@r', '^~P', '@&', '@~)']
    for test in tests:
        code = buildKeySequence(test)
        print "Code %d is sequence %s and nemonic is %s" % (code, QKeySequence(code).toString(), buildKeyEquivalent(code))
