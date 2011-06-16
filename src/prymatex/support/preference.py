#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Preferences's module
    http://manual.macromates.com/en/preferences_items.html
    
    completions, an array of additional candidates when cycling through completion candidates from the current document.
    completionCommand, a shell command (string) which should return a list of candidates to complete the current word (obtained via the TM_CURRENT_WORD variable).
    disableDefaultCompletion, set to 1 if you want to exclude matches from the current document when asking for completion candidates (useful when you provide your own completion command).

    decreaseIndentPattern, regular expression.
    increaseIndentPattern, regular expression.
    indentNextLinePattern, regular expression.
    unIndentedLinePattern, regular expression.

    showInSymbolList, set to 1 to include in the symbol list.
    symbolTransformation, 

    highlightPairs, an array of arrays, each containing a pair of characters where, when the caret moves over the second, the first one will be highlighted for a short moment, if found.
    smartTypingPairs, an array of arrays, each containing a pair of characters where when the first is typed, the second will be inserted. An example is shown below. For more information see auto-paired characters.

    shellVariables, an array of key/value pairs. See context dependent variables.
    spellChecking, set to 0/1 to disable/enable spell checking.
'''
import re
try:
    from ponyguruma import sre
except Exception, e:
    sre = re
from prymatex.support.bundle import PMXBundleItem

def compileRegexp(string):
    #Muejejejeje
    try:
        restring = string.replace('?i:', '(?i)')
        return re.compile(unicode(restring))
    except:
        try:
            return sre.compile(unicode(string))
        except:
            #Mala leche
            pass
        
DEFAULT_SETTINGS = { 'completions': [],
                     'completionCommand': '',
                     'disableDefaultCompletion': 0,
                     'showInSymbolList': None,
                     'symbolTransformation': None,
                     'highlightPairs': [],
                     'smartTypingPairs': [],
                     'decreaseIndentPattern': None,
                     'increaseIndentPattern': None,
                     'indentNextLinePattern': None,
                     'unIndentedLinePattern': None,
                     'shellVariables': {},
                     'spellChecking': 0
                      }

class PMXPreferenceSettings(object):
    KEYS = [    'completions', 'completionCommand', 'disableDefaultCompletion', 'showInSymbolList', 'symbolTransformation', 
                'highlightPairs', 'smartTypingPairs', 'shellVariables', 'spellChecking',
                'decreaseIndentPattern', 'increaseIndentPattern', 'indentNextLinePattern', 'unIndentedLinePattern' ]
    INDENT_NONE = 0
    INDENT_INCREASE = 1
    INDENT_DECREASE = 2
    INDENT_NEXTLINE = 3
    UNINDENT = 4
    TRANSFORMATIONPATTERN = re.compile('s/(.*)/(.*)/([mg]?);?')
    def __init__(self, hash):
        for key in self.KEYS:
            value = hash.get(key, None)
            if value != None:
                if key in [ 'decreaseIndentPattern', 'increaseIndentPattern', 'indentNextLinePattern', 'unIndentedLinePattern' ]:
                    value = compileRegexp( value )
                elif key in [ 'shellVariables' ]:
                    value = dict(map(lambda d: (d['name'], d['value']), value))
                elif key in [ 'symbolTransformation' ]:
                    value = [ self.TRANSFORMATIONPATTERN.findall(value) ]
            setattr(self, key, value)
    
    @property
    def hash(self):
        hash = {}
        for key in PMXPreferenceSettings.KEYS:
            value = getattr(self, key)
            if value != None:
                if key in [ 'decreaseIndentPattern', 'increaseIndentPattern', 'indentNextLinePattern', 'unIndentedLinePattern' ]:
                    value = value.pattern
                elif key in [ 'shellVariables' ]:
                    value = [ {'name': t[0], 'value': t[1] } for t in  value.iteritems() ]
                hash[key] = value
        return hash
    
    def combine(self, other):
        for key in PMXPreferenceSettings.KEYS:
            value = getattr(other, key, None)
            if value != None:
                if key == 'shellVariables':
                    self.shellVariables.update(value)
                if key == 'showInSymbolList' and self.showInSymbolList == None:
                    self.showInSymbolList = other.showInSymbolList
                elif not getattr(self, key):
                    setattr(self, key, value)
    
    def update(self, other):
        for key in PMXPreferenceSettings.KEYS:
            value = getattr(other, key, None)
            if value is not None and not getattr(self, key):
                setattr(self, key, value)

    def indent(self, line):
        #IncreasePattern on return indent nextline
        #DecreasePattern evaluate line to decrease, no requiere del return
        #IncreaseOnlyNextLine on return indent nextline only
        #IgnoringLines evaluate line to unindent, no require el return
        line = line.encode('utf-8')
        if self.decreaseIndentPattern != None and self.decreaseIndentPattern.search(line):
            return self.INDENT_DECREASE
        elif self.increaseIndentPattern != None and self.increaseIndentPattern.search(line):
            return self.INDENT_INCREASE
        elif self.indentNextLinePattern != None and self.indentNextLinePattern.search(line):
            return self.INDENT_NEXTLINE
        elif self.unIndentedLinePattern != None and self.unIndentedLinePattern.search(line):
            return self.UNINDENT
        return self.INDENT_NONE
    
class PMXPreference(PMXBundleItem):
    KEYS = [ 'settings' ]
    TYPE = 'preference'
    FOLDER = 'Preferences'
    EXTENSION = 'tmPreferences'
    PATTERNS = ['*.tmPreferences', '*.plist']

    def __init__(self, namespace, hash = None, path = None):
        super(PMXPreference, self).__init__(namespace, hash, path)

    def load(self, hash):
        super(PMXPreference, self).load(hash)
        for key in PMXPreference.KEYS:
            if key == 'settings':
                setattr(self, key, PMXPreferenceSettings(hash.get(key, {})))
            else:
                setattr(self, key, hash.get(key, None))
    
    @property
    def hash(self):
        hash = super(PMXPreference, self).hash
        for key in PMXPreference.KEYS:
            value = self.settings.hash
            if value != None:
                hash['settings'] = value
        return hash

    @staticmethod
    def buildSettings(preferences):
        settings = PMXPreferenceSettings(DEFAULT_SETTINGS)
        if preferences:
            bundle = preferences[0].bundle
            for p in preferences:
                if p.bundle == bundle:
                    settings.combine(p.settings)
                else:
                    settings.update(p.settings)
        return settings