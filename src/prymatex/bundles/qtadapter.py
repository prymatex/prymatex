#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    caret, foreground, selection, invisibles, lineHighlight, gutter, background
'''

#caret, foreground, selection, invisibles, lineHighlight, gutter, background
def buildQTextFormat(style):
    # isinstance(style, PMXStyle) == True
    format = QTextCharFormat()
    if 'foreground' in style:
        format.setForeground(QColor(style['foreground']))
    if 'background' in style:
        format.setBackground(QColor(style['background']))
    if 'fontStyle' in style:
        if style['fontStyle'] == 'bold':
            format.setFontWeight(QFont.Bold)
        elif style['fontStyle'] == 'underline':
            format.setFontUnderline(True)
        elif style['fontStyle'] == 'italic':
            format.setFontItalic(True)
    return format
    
def buildKeyEquivalentPattern(key_event):
    return "^$K"