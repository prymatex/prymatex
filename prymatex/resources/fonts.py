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
    return [fam for fam in QtGui.QFontDatabase().families() if fam == font]
    
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

def load_fonts(resourcesPath):
    resources = { "Fonts": {} }
    
    # Load Fonts
    fontsPath = os.path.join(resourcesPath, "Media", "Fonts")
    if os.path.exists(fontsPath):
        for fontFileName in os.listdir(fontsPath):
            name = os.path.splitext(fontFileName)[0]
            fontPath = os.path.join(fontsPath, fontFileName)
            fid = QtGui.QFontDatabase.addApplicationFont(fontPath)
            families = QtGui.QFontDatabase.applicationFontFamilies(fid)
            for f in families:
                resources["Fonts"].setdefault(f, []).append(fontPath)
    return resources