#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from PyQt4.Qt import QTextCharFormat, QColor, QFont, QKeySequence, Qt
except:
    from prymatex.bundles.qtmock import Qt, QKeySequence
from prymatex.bundles.modmap import get_keymap_table
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

def buildKeyEquivalentString(nemonic):
    return buildKeySequence(nemonic).toString()

def buildKeyEquivalentCode(nemonic):
    return int(buildKeySequence(nemonic))

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
        sequence.extend(keys)
    return QKeySequence(sum(sequence))

if __name__ == '__main__':
    tests = ['@r', '^~P', '@&', '@~)']
    for test in tests:
        sequence = buildKeySequence(test)
        print "code %d in Qt and your Keyboar Layout is %s" % (sequence, sequence)