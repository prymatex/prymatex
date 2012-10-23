#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string

from PyQt4 import QtGui
from PyQt4.Qt import QKeySequence, Qt

from prymatex.utils.decorators.memoize import memoized
from prymatex.utils.modmap import get_keymap_table
'''
    caret, foreground, selection, invisibles, lineHighlight, gutter, background
    * Meta -> (cinta de 4 esquinas) -> arroba (@)
    * Control es ^
    * Shift es la $
    * Backspace -> ^?
    * supr -> ?M-^\?
    * Alt -> ~
'''

#======================
# Colors
#======================
def rgba2color(rgba):
    '''
    @param rgba: A html formated color string i.e.: #RRGGBB or #RRGGBBAA
    @return: If rgba is a valid color, a QColor isntance
    ''' 
    rgba = unicode(rgba).strip('#')
    if len(rgba) in [ 6, 8 ]:
        red, green, blue, alpha = rgba[0:2], rgba[2:4], rgba[4:6], rgba[6:8]
    else:
        raise ValueError("Invalid RGBA value %s", rgba)
    return QtGui.QColor(int(red, 16), int(green, 16), int(blue, 16), int(alpha or 'FF', 16))

def color2rgba(color):
    '''
    @param color: A QColor, int, str, unicode instance
    @return: If color is a valid, a html formated color string i.e.: #RRGGBB or #RRGGBBAA
    ''' 
    if isinstance(color, QtGui.QColor):
        color = color.rgba()
    if isinstance(color, (int, long)):
        color = hex(long(color))[2:-1]
    if isinstance(color, (str, unicode)) and len(color) in [ 6, 7, 8 ]:
        color = color.upper()
        if len(color) == 8:
            color = color[2:] + color[0:2] if color[0:2] != 'FF' else color[2:]
        elif len(color) == 7:
            color = color[1:] + '0' + color[0]
        return "#%s" % color
    else:
        raise ValueError("Invalid color value %s" % color)
  
#======================
# Key Equivalents
#======================
QTCHARCODES = {9: Qt.Key_Backspace,
               10: Qt.Key_Return,
               127: Qt.Key_Delete,
               63232: Qt.Key_F1,
               63234: Qt.Key_F2,
               #63233: Qt.Key_F3,
               63235: Qt.Key_F11, #No se que es
               63236: Qt.Key_F11, #No se que es
               63238: Qt.Key_F3, #No se que es
               63240: Qt.Key_F5,
               63272: Qt.Key_F7}

KEYMAP = get_keymap_table()

def _keyboard_layout_keys(key):
    shift = False
    for _, keysyms in KEYMAP.iteritems():
        if key == keysyms[1]:
            return (True, key)
    return (shift, key)

@memoized
def keysequence2keyequivalent(sequence):
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
            keys.append(Qt.SHIFT) #Add Shift
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
        keys = _keyboard_layout_qtkeys(nemonic.pop())
        if Qt.SHIFT in keys and Qt.SHIFT in sequence:
            keys.remove(Qt.SHIFT)
        sequence.extend(keys)
    return sum(sequence)

if __name__ == '__main__':
    tests = ['@r', '^~P', '@&', '@~)']
    for test in tests:
        code = buildKeySequence(test)
        print "Code %d is sequence %s and nemonic is %s" % (code, QKeySequence(code).toString(), buildKeyEquivalent(code))
