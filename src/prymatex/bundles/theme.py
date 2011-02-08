#!/usr/bin/env python
# -*- coding: utf-8 -*-

import plistlib
from copy import copy
from xml.parsers.expat import ExpatError
# for run as main
if __name__ == "__main__":
    import sys, os
    sys.path.append(os.path.abspath('../..'))
from prymatex.bundles.score import PMXScoreManager
from prymatex.bundles.qtadapter import buildQTextFormat, buildQColor

'''
    caret, foreground, selection, invisibles, lineHighlight, gutter, background
'''

class PMXStyle(object):
    def __init__(self, hash):
        for key in [    'scope', 'name', 'settings' ]:
            setattr(self, key, hash.pop(key, None))
        
        if hash:
            print "Style has more values (%s)" % (', '.join(hash.keys()))

    def __getitem__(self, name):
        return self.settings[name]
    
    def __contains__(self, name):
        return name in self.settings
    
    def __copy__(self):
        values = {'scope': self.scope, 'name': self.name, 'settings': copy(self.settings)}
        obj = PMXStyle(values)
        return obj
        
    def update(self, other):
        self.settings.update(other.settings)
    
    @property
    def QTextFormat(self):
        return buildQTextFormat(self)
    
    def getQColor(self, item):
        return buildQColor(self[item])
    
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

    def getStyle(self, scope = None):
        base = copy(self.default)
        if scope == None:
            return base
        styles = []
        for style in self.sytles:
            if style.scope != None:
                score = self.scores.score(style.scope, scope)
                if score != 0:
                    styles.append((score, style))
        styles.sort(key = lambda t: t[0])
        for score, style in styles:
            base.update(style)
        return base
    
def main():
    import os 
    from glob import glob
    import prymatex.bundles
    for file in glob(os.path.join('../share/Themes/', '*')):
        PMXTheme.loadTheme(file)
    theme = PMXTheme.getThemeByName('Twilight')
    style = theme.getStyle('source.python meta.class.python')
    print style.QTextFormat

if __name__ == '__main__':
    main()
