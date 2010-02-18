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
        self.name = hash.get('name')
        self.author = hash.get('author')
        self.styles = hash.get('settings')
        self.default = self.styles.pop(0)
        TM_THEMES[self.name] = self
        
    def get_style(self, scope):
        for style in self.styles:
            if style['scope'] == scope: 
                return style['settings']
    
    def get_default_style(self):
        return self.default['settings']
    
    def get_style_or_default(self, scope):
        return self.get_style(scope) or self.get_default_style()
    
    @property
    def scopes(self):
        return map(lambda style: style['scope'], self.styles)
    
    def items(self):
        return map(lambda style: (style['scope'], style['settings']), self.styles)
        
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

def main():
    from pprint import pprint
    print load_textmate_themes('../../resources/Themes')
    pprint(TM_THEMES['Blackboard'].scopes)
if __name__ == '__main__':
    main()