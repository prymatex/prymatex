#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os #, #glob, 
import plistlib
from os.path import join, abspath
from glob import glob
from xml.parsers.expat import ExpatError
# for run as main
if __name__ == "__main__":
    import sys
    sys.path.append(os.path.abspath('../..'))
from prymatex.bundles.score import PMXScoreManager

'''
    caret, foreground, selection, invisibles, lineHighlight, gutter, background
'''

class PMXStyle(object):
    def __init__(self, hash):
        for key in [    'scope', 'name', 'settings' ]:
            setattr(self, key, hash.pop(key, None))
        
        if hash:
            print "Style has more values (%s)" % (', '.join(hash.keys()))

class PMXTheme(object):
    THEMES = {}
    scores = PMXScoreManager()
    
    def __init__(self, hash):
        self.sytles = []
        for key in [    'uuid', 'name', 'comment', 'author', 'settings' ]:
            value = hash.pop(key, None)
            if key == 'settings':
                self.default = PMXStyle(value[0])
                for setting in value[1:]:
                    self.sytles.append(PMXStyle(setting))
            else:
                setattr(self, key, value)

        if hash:
            print "Bundle '%s' has more values (%s)" % (self.name, ', '.join(hash.keys()))

    @staticmethod
    def loadTheme(path):
        try:
            data = plistlib.readPlist(path)
            theme = PMXTheme(data)
        except Exception, e:
            print "Error en bundle %s (%s)" % (path, e)

        PMXTheme.THEMES[theme.uuid] = theme
        return theme
        
    @classmethod
    def getThemeByName(cls, name):
        for uuid, theme in cls.THEMES.iteritems():
            if theme.name == name:
                return theme

    def getStyle(self, scope):
        base = self.default.settings
        styles = []
        for style in self.sytles:
            if style.scope != None:
                score = self.scores.score(scope, style.scope)
                if score != 0:
                    styles.append((score, style))
        styles.sort(key = lambda t: t[0])
        for score, style in styles:
            base.update(style.settings)
        return base
    
def main():
    for file in glob(os.path.join('../share/Themes/', '*')):
        PMXTheme.loadTheme(file)
    theme = PMXTheme.getThemeByName('Twilight')
    print theme.getStyle('source.python meta.class.python')

if __name__ == '__main__':
    main()
