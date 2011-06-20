#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, string
sys.path.append(os.path.abspath('../../..'))

try:
    from PyQt4.Qt import QTextCharFormat, QColor, QFont, QKeySequence, Qt
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

#caret, foreground, selection, invisibles, lineHighlight, gutter, background
def buildQColor(color):
    if type(color) == str:
        if color[0] == "#":
            alpha = color[7:]
            qcolor = QColor(color[:7])
            if alpha:
                qcolor.setAlpha(int(alpha, 16))
    else:
        qcolor = QColor()
    return qcolor

def buildQTextFormat(style):
    # isinstance(style, PMXStyle) == True
    format = QTextCharFormat()
    if 'foreground' in style:
        format.setForeground(buildQColor(style['foreground']))
    if 'background' in style:
        format.setBackground(buildQColor(style['background']))
    if 'fontStyle' in style:
        if style['fontStyle'] == 'bold':
            format.setFontWeight(QFont.Bold)
        elif style['fontStyle'] == 'underline':
            format.setFontUnderline(True)
        elif style['fontStyle'] == 'italic':
            format.setFontItalic(True)
    return format
    
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
    return None
    if shift and u"$" in nemonic:
        nemonic.append(key)
        nemonic.remove(u"$")
    nemonic.append(code)
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
