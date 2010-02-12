#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os #, #glob, 
import plistlib
from os.path import join, abspath
from glob import glob
from PyQt4.Qt import QTextCharFormat, QColor, QFont
from xml.parsers.expat import ExpatError

TM_THEMES = {}
#TODO: No me gusta como esta este temes muy pegado al parser y como se arman los estilos, 
#quiza dejar esto como un themes de textmate y crear un objeto que los interprete y cree nuestro sistema de estilos
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
            if 'fontStyle' in setting['settings']:
                if setting['settings']['fontStyle'] == 'bold':
                    format.setFontWeight(QFont.Bold)
                elif setting['settings']['fontStyle'] == 'underline':
                    format.setFontUnderline(True)
                elif setting['settings']['fontStyle'] == 'italic':
                    format.setFontItalic(True)
            if 'foreground' in setting['settings']:
                format.setForeground(QColor(setting['settings']['foreground']))
            if 'background' in setting['settings']:
                format.setBackground(QColor(setting['settings']['background']))
            setting['format'] = format
            self.formats[setting['scope']] = setting
    
    def get_format(self, scope):
        format = None
        tags = scope.split('.')
        while format == None and tags:
            format = self.formats.get('.'.join(tags), None)
            tags.pop()
        if format:
            return format['format']
        return self.default

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
