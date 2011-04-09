#!/usr/bin/env python
# -*- coding: utf-8 -*-
import string
from PyQt4.Qt import QTextCharFormat, QColor, QFont
from PyQt4.QtCore import Qt

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
               127: Qt.Key_Delete,
               63232: Qt.Key_F1,
               63233: Qt.Key_F3,
               63234: Qt.Key_F2,
               63235: Qt.Key_F3,
               63236: Qt.Key_F3,
               63238: Qt.Key_F3,
               63240: Qt.Key_F5,
               63272: Qt.Key_F7,
               63302: Qt.Key_F3}

def buildKeySequence(nemonic):
    values = list(nemonic)
    sequence = []
    if '^' in nemonic:
        sequence.append(Qt.CTRL)
        values.remove('^')
    if '~' in nemonic:
        sequence.append(Qt.ALT)
        values.remove('~')
    if '$' in nemonic:
        sequence.append(Qt.SHIFT)
        values.remove('$')
    if '@' in nemonic:
        sequence.append(Qt.META)
        values.remove('@')
    if len(values) == 1:
        char = values.pop()
        code = ord(char)
        if char in string.ascii_uppercase:
            sequence.append(Qt.SHIFT)
        elif char in string.ascii_lowercase:
            code = ord(char.upper())
        elif not (0x20 <= code <= 0x7E):
            if not code in QTCHARCODES:
                print "need map", code, char
            else:
                code = QTCHARCODES[code]
        sequence.append(code)
    if nemonic == "$\n":
        print 'es el comando', sequence
    return sum(sequence)

CHARACTER_REPLACES = { ' ': u'Space',
                       '&': u'&&',
                       9: u'←',
                       10: u'↩',
                       127: u'⌫',
                       63232: u'F1',
                       63233: u'F1',
                       63234: u'F1',
                       63235: u'F1',
                       63236: u'F1',
                       63238: u'F3',
                       63240: u'F5',
                       63272: u'F7',
                       63302: u'F1'}

def buildKeyEquivalentString(key):
    values = list(key)
    equivalent = []
    if u"^" in key:
        equivalent.append(u"Ctrl")
        values.remove(u"^")
    if u"~" in key:
        equivalent.append(u"Alt")
        values.remove(u"~")
    if u"$" in key:
        equivalent.append(u"Shift")
        values.remove(u"$")
    if u"@" in key:
        equivalent.append(u"Meta")
        values.remove(u"@")
    if len(values) == 1:
        char = values.pop()
        code = ord(char)
        if char in string.ascii_uppercase:
            equivalent.append(u"Shift")
        elif char in string.ascii_lowercase:
            char = char.upper()
        elif char in CHARACTER_REPLACES:
            char = CHARACTER_REPLACES[char]
        elif code in CHARACTER_REPLACES:
            char = CHARACTER_REPLACES[code]
        equivalent.append(char)
    return u"+".join(equivalent)