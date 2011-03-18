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
        if char in string.ascii_uppercase:
            sequence.append(Qt.SHIFT)
        sequence.append(ord(char.upper()))
    elif len(values) > 1:
        raise Exception("mal")
    return sum(sequence)

CHARACTER_REPLACES = {'&': '&&'}

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
        if char in string.ascii_uppercase:
            equivalent.append(u"Shift")
        char = char.upper()
        if char in CHARACTER_REPLACES:
            char = CHARACTER_REPLACES[char]
        equivalent.append(char)
    elif len(values) > 1:
        raise Exception("mal") 
    return "+".join(equivalent)