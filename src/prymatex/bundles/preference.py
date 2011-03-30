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
import ponyguruma as onig
from ponyguruma.constants import OPTION_CAPTURE_GROUP
from prymatex.bundles.base import PMXBundleItem

onig_compile = onig.Regexp.factory(flags = OPTION_CAPTURE_GROUP)
DEFAULT_SETTINGS = { 'completions': [],
                     'completionCommand': '',
                     'disableDefaultCompletion': 0,
                     'showInSymbolList': 0,
                     'symbolTransformation': '',
                     'highlightPairs': [],
                     'smartTypingPairs': [],
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
    def __init__(self, hash):
        for key in self.KEYS:
            value = hash.get(key, None)
            if value != None:
                if key in [ 'decreaseIndentPattern', 'increaseIndentPattern', 'indentNextLinePattern', 'unIndentedLinePattern' ]:
                    value = onig_compile( value )
                elif key in [ 'shellVariables' ]:
                    value = dict(map(lambda d: (d['name'], d['value']), value))
            setattr(self, key, value)
            
    def combine(self, other):
        for key in self.KEYS:
            value = getattr(other, key, None)
            if value != None:
                setattr(self, key, value)
    
    def indent(self, line):
        #IncreasePattern on return indent nextline
        #DecreasePattern evaluate line to decrease, no requiere del return
        #IncreaseOnlyNextLine on return indent nextline only
        #IgnoringLines evaluate line to unindent, no require el return
        if self.decreaseIndentPattern != None and self.decreaseIndentPattern.match(line):
            return self.INDENT_DECREASE
        elif self.increaseIndentPattern != None and self.increaseIndentPattern.match(line):
            return self.INDENT_INCREASE
        elif self.indentNextLinePattern != None and self.indentNextLinePattern.match(line):
            return self.INDENT_NEXTLINE
        elif self.unIndentedLinePattern != None and self.unIndentedLinePattern.match(line):
            return self.UNINDENT
        else:
            return self.INDENT_NONE
    
class PMXPreference(PMXBundleItem):
    path_patterns = ['Preferences/*.tmPreferences', 'Preferences/*.plist']
    bundle_collection = 'preferences'
    def __init__(self, hash, name_space = "default", path = None):
        super(PMXPreference, self).__init__(hash, name_space, path)
        for key in [ 'settings' ]:
            if key == 'settings':
                setattr(self, key, PMXPreferenceSettings(hash.get(key, {})))

    def setBundle(self, bundle):
        super(PMXPreference, self).setBundle(bundle)
        bundle.PREFERENCES.setdefault(self.scope, []).append(self)
    
    @staticmethod
    def buildSettings(preferences):
        settings = PMXPreferenceSettings(DEFAULT_SETTINGS)
        for p in preferences:
            settings.combine(p.settings)
        return settings