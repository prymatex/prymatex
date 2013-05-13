#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string

from prymatex.qt import QtGui

""" caret, foreground, selection, invisibles, lineHighlight, gutter, background """

#======================
# Colors
#======================
def rgba2color(rgba):
    '''
    @param rgba: A html formated color string i.e.: #RRGGBB or #RRGGBBAA
    @return: If rgba is a valid color, a QColor isntance
    ''' 
    rgba = str(rgba).strip('#')
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
        color = hex(int(color))[2:-1]
    if isinstance(color, str) and len(color) in [ 6, 7, 8 ]:
        color = color.upper()
        if len(color) == 8:
            color = color[2:] + color[0:2] if color[0:2] != 'FF' else color[2:]
        elif len(color) == 7:
            color = color[1:] + '0' + color[0]
        return "#%s" % color
    else:
        raise ValueError("Invalid color value %s" % color)
