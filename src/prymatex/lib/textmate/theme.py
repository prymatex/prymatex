#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os #, #glob, 
import plistlib
from os.path import join, abspath
from glob import glob
from PyQt4.Qt import QTextCharFormat, QColor, QFont
from xml.parsers.expat import ExpatError

TM_THEMES = {}

class TMTheme(object):
    def __init__(self, hash):
        self.uuid = self.name = hash.get('uuid')
        self.name = self.name = hash.get('name')
        TM_THEMES[self.name] = self
        self.author = self.name = hash.get('author')
        
        settings = hash.get('settings')
        default = settings.pop(0)
        
        self.default = QTextCharFormat()
        if 'foreground' in default:
            self.default.setForeground(QColor(default['foreground']))
        if 'background' in default:
            self.default.setBackground(QColor(default['background']))
        
        self.formats = {}
        for setting in settings:
            if 'scope' not in setting:
                continue
            format = QTextCharFormat()
            if 'fontStyle' in setting:
                format.setFontWeight(QFont.Light)
            if 'foreground' in setting:
                format.setForeground(QColor(setting['foreground']))
            if 'background' in setting:
                format.setBackground(QColor(setting['background']))
            setting['format'] = format
            self.formats[setting['scope']] = setting

def load_textmate_themes(path):
    search_path = join(abspath(path), '*.tmTheme')
    paths = glob(search_path)
    counter = 0
    for path in paths:
        try:
            data = plistlib.readPlist(os.path.abspath(path))
            TMTheme(data)
        except ExpatError:
            pass
        counter += 1
    return counter
