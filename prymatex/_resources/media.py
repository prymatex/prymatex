#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

from collections import namedtuple

from prymatex.qt import QtGui

from prymatex.utils import encoding
from prymatex.widgets import glyph

from .base import build_resource_key

IconTheme = namedtuple("IconTheme", "name type path")

def load_media(resourcesPath):
    resources = { "Images": {}, "Icons": {}, "Themes": {}, "Mapping": {}, "Glyphs": {}, "External": {} }
    # Load Icons
    iconsPath = os.path.join(resourcesPath, "Media", "Icons")
    if os.path.exists(iconsPath):
        for dirpath, dirnames, filenames in os.walk(iconsPath):
            for filename in filenames:
                iconPath = os.path.join(dirpath, filename)
                name = build_resource_key(iconPath[len(iconsPath):])
                resources["Icons"][name] = iconPath

    # Load Images
    imagesPath = os.path.join(resourcesPath, "Media", "Images")
    if os.path.exists(imagesPath):
        for dirpath, dirnames, filenames in os.walk(imagesPath):
            for filename in filenames:
                imagePath = os.path.join(dirpath, filename)
                name = build_resource_key(imagePath[len(imagesPath):])
                resources["Images"][name] = imagePath
                
    # Load Themes
    themesPath = os.path.join(resourcesPath, "Media", "Themes")
    if os.path.exists(themesPath):
        themePaths = [ themesPath ] + QtGui.QIcon.themeSearchPaths()
        for themePath in themePaths:
            if not os.path.exists(themePath):
                continue
            for name in os.listdir(themePath):
                descriptor = os.path.join(themePath, name, "index.theme")
                if os.path.exists(descriptor):
                    resources["Themes"][name] = IconTheme(name, "pix", os.path.join(themePath, name))
    
    # Load Glyphs
    glyphsPath = os.path.join(resourcesPath, "Media", "Glyphs")
    if os.path.exists(glyphsPath):
        for glyphFileName in os.listdir(glyphsPath):
            name = os.path.splitext(glyphFileName)[0]
            glyphPath = os.path.join(glyphsPath, glyphFileName)
            gly = glyph.QtGlyph.initGlyph(glyphPath)
            resources["Glyphs"][gly.name()] = gly
            resources["Themes"][gly.name()] = IconTheme(gly.name(), "glyph", glyphPath)
    
    # Load Mapping
    mappingsPath = os.path.join(resourcesPath, "Media", "Mapping")
    if os.path.exists(mappingsPath):
        for mappingFileName in os.listdir(mappingsPath):
            name = os.path.splitext(mappingFileName)[0]
            file_content, _ = encoding.read(os.path.join(mappingsPath, mappingFileName))
            resources["Mapping"][name] = json.loads(file_content)

    return resources
