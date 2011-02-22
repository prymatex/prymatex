#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
    result = list(nemonic)
    if '^' in nemonic:
        result[result.index('^')] = Qt.ControlModifier
    if '~' in result:
        result[result.index('~')] = Qt.AltModifier
    if '$' in result:
        result[result.index('$')] = Qt.ShiftModifier
    if '@' in result:
        result[result.index('@')] = Qt.MetaModifier
    if result and isinstance(result[-1], (str, unicode)):
        result[-1] = ord(result[-1])
    print result
    return reduce(lambda x, y: x + y, result, 0)
    
def buildKeyEquivalentPattern(key_event):
    value = key_event.text()
    if value != "": return value
    modifiers = key_event.modifiers()
    print modifiers
    key = key_event.key()
    if modifiers & Qt.ControlModifier:
        value += "^"
    if modifiers & Qt.AltModifier:
        value += "~"
    if modifiers & Qt.ShiftModifier:
        value += "$"
    if modifiers & Qt.MetaModifier:
        value += "@"
    if key < 255:
        value += chr(key) 
    return value