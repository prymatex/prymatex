#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from prymatex.qt import QtGui

if sys.platform == 'darwin':
    BIG = MEDIUM = SMALL = 12
elif os.name == 'nt':
    BIG = 12    
    MEDIUM = 10
    SMALL = 9
else:
    BIG = 12    
    MEDIUM = 9
    SMALL = 9

def font_is_installed(font):
    """Check if font is installed"""
    return [fam for fam in QtGui.QFontDatabase().families() if str(fam) == font]
    
def get_family(families):
    """Return the first installed font family in family list"""
    if not isinstance(families, list):
        families = [ families ]
    for family in families:
        if font_is_installed(family):
            return family
    else:
        print("Warning: None of the following fonts is installed: %r" % families)
        return QtGui.QFont().family()
        
def loadGlyphs(resourcesPath):
    glyphs = {}
    glyphsPath = os.path.join(resourcesPath, "Glyphs")
    if os.path.exists(glyphsPath):
        for glyphFileName in os.listdir(glyphsPath):
            name = os.path.splitext(glyphFileName)[0]
            glyphs[name] = os.path.join(glyphsPath, glyphFileName)
    return {"Glyphs": glyphs}
