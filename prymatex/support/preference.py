#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Preferences's module
    http://manual.macromates.com/en/preferences_items.html
    
    completions, an array of additional candidates when cycling through completion candidates from the current document.
    completionCommand, a shell command (string) which should return a list of candidates to complete the current word (obtained via the TM_CURRENT_WORD variable).
    executeCompletionCommand, a command item
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
from copy import copy
import uuid as uuidmodule

from prymatex.support.bundle import PMXBundleItem
from prymatex.support.utils import compileRegexp
from prymatex.support.snippet import PMXSnippet
from prymatex.support.processor import PMXDebugSnippetProcessor

class PMXPreferenceSettings(object):
    KEYS = [    'completions', 'completionCommand', 'executeCompletionCommand', 'disableDefaultCompletion', 'showInSymbolList', 'symbolTransformation', 
                'highlightPairs', 'smartTypingPairs', 'shellVariables', 'spellChecking',
                'decreaseIndentPattern', 'increaseIndentPattern', 'indentNextLinePattern', 'unIndentedLinePattern' ]
    INDENT_KEYS = [ 'decreaseIndentPattern', 'increaseIndentPattern', 'indentNextLinePattern', 'unIndentedLinePattern' ]
    INDENT_INCREASE = 0
    INDENT_DECREASE = 1
    INDENT_NEXTLINE = 2
    UNINDENT = 3
    def __init__(self, dataHash = {}, preference = None):
        self.preference = preference
        self.update(dataHash)
    
    @property
    def hash(self):
        dataHash = {}
        for key in PMXPreferenceSettings.KEYS:
            value = getattr(self, key)
            if value != None:
                if key in [ 'decreaseIndentPattern', 'increaseIndentPattern', 'indentNextLinePattern', 'unIndentedLinePattern' ]:
                    value = value.pattern
                elif key in [ 'shellVariables' ]:
                    value = [ {'name': t[0], 'value': t[1] } for t in  value.iteritems() ]
                elif key in [ 'symbolTransformation' ]:
                    value = ";".join(value) + ";"
                elif key in [ 'showInSymbolList' ]:
                    value = value and "1" or "0"
                elif key in [ 'spellChecking' ]:
                    value = value and "1" or "0"
                dataHash[key] = value
        return dataHash

    def update(self, dataHash):
        for key in self.KEYS:
            value = dataHash.get(key, None)
            if value != None:
                if key in [ 'decreaseIndentPattern', 'increaseIndentPattern', 'indentNextLinePattern', 'unIndentedLinePattern' ]:
                    value = compileRegexp( value )
                elif key in [ 'shellVariables' ]:
                    value = dict(map(lambda d: (d['name'], d['value']), value))
                elif key in [ 'symbolTransformation' ]:
                    value = map(lambda value: value.strip(), value.split(";"))
                elif key in [ 'showInSymbolList' ]:
                    value = bool(int(value))
                elif key in [ 'spellChecking' ]:
                    value = bool(int(value))
            setattr(self, key, value)
    
class PMXPreferenceMasterSettings(object):
    def __init__(self):
        """docstring for __init__"""
        self.settings = []
    
    @property
    def completions(self):
        for settings in self.settings:
            if settings.completions is not None:
                return settings.completions[:]
        return []
        
    @property
    def completionCommand(self):
        for settings in self.settings:
            if settings.completionCommand is not None:
                return settings.completionCommand
                
    @property
    def executeCompletionCommand(self):
        for settings in self.settings:
            if settings.executeCompletionCommand is not None:
                return settings.executeCompletionCommand
                
    @property
    def disableDefaultCompletion(self):
        for settings in self.settings:
            if settings.executeCompletionCommand is not None:
                return settings.executeCompletionCommand
        
    @property
    def showInSymbolList(self):
        for settings in self.settings:
            if settings.showInSymbolList is not None:
                return settings.showInSymbolList
        return False
        
    @property
    def symbolTransformation(self):
        for settings in self.settings:
            if settings.symbolTransformation is not None:
                return settings.symbolTransformation
                
    @property
    def highlightPairs(self):
        for settings in self.settings:
            if settings.highlightPairs is not None:
                return settings.highlightPairs[:]
                
    @property
    def smartTypingPairs(self):
        for settings in self.settings:
            if settings.smartTypingPairs is not None:
                return settings.smartTypingPairs[:]
        
    @property
    def shellVariables(self):
        shellVariables = {}
        for settings in self.settings:
            if isinstance(settings.shellVariables, dict) and all(map(lambda shellKey: shellKey not in shellVariables, settings.shellVariables.keys())):
                shellVariables.update(settings.shellVariables)
        return shellVariables
        
    @property
    def spellChecking(self):
        for settings in self.settings:
            if settings.spellChecking is not None:
                return settings.spellChecking
        return True
        
    @property
    def decreaseIndentPattern(self):
        settings = self._findIndentSettings()
        if settings is not None:
            return settings.decreaseIndentPattern
            
    @property
    def increaseIndentPattern(self):
        settings = self._findIndentSettings()
        if settings is not None:
            return settings.increaseIndentPattern
            
    @property
    def indentNextLinePattern(self):
        settings = self._findIndentSettings()
        if settings is not None:
            return settings.indentNextLinePattern
            
    @property
    def unIndentedLinePattern(self):
        settings = self._findIndentSettings()
        if settings is not None:
            return settings.unIndentedLinePattern
        
    def append(self, otherSettings):
        self.settings.append(otherSettings)

    def _findIndentSettings(self):
        #TODO: Algo de cache?
        for settings in self.settings:
            if any(map(lambda indentKey: getattr(settings, indentKey) is not None, PMXPreferenceSettings.INDENT_KEYS)):
                return settings
                
    def getBundle(self, attrKey):
        for settings in self.settings:
            if getattr(settings, attrKey) is not None:
                return settings.preference.bundle
    
    def getManager(self, attrKey):
        for settings in self.settings:
            if getattr(settings, attrKey) is not None:
                return settings.preference.manager
                
    def indent(self, line):
        #IncreasePattern on return indent nextline
        #DecreasePattern evaluate line to decrease, no requiere del return
        #IncreaseOnlyNextLine on return indent nextline only
        #IgnoringLines evaluate line to unindent, no require el return
        settings = self._findIndentSettings()
        indent = []
        if settings.decreaseIndentPattern != None and settings.decreaseIndentPattern.search(line):
            indent.append(PMXPreferenceSettings.INDENT_DECREASE)
        if settings.increaseIndentPattern != None and settings.increaseIndentPattern.search(line):
            indent.append(PMXPreferenceSettings.INDENT_INCREASE)
        if settings.indentNextLinePattern != None and settings.indentNextLinePattern.search(line):
            indent.append(PMXPreferenceSettings.INDENT_NEXTLINE)
        if settings.unIndentedLinePattern != None and settings.unIndentedLinePattern.search(line):
            indent.append(PMXPreferenceSettings.UNINDENT)
        return indent
    
    def compileSymbolTransformation(self):
        self._snippetsTransformation = []
        for symbol in self.symbolTransformation:
            symbol = "${SYMBOL" + symbol[1:] + "}"
            dataHash = {    'content': symbol, 
                            'name': symbol }
            snippet = PMXSnippet(uuidmodule.uuid1(), "internal", dataHash = dataHash)
            self._snippetsTransformation.append(snippet)
    
    def transformSymbol(self, text):
        #TODO: Hacer la transformacion de los simbolos
        return text
        if not hasattr(self, '_snippetsTransformation'):
            self.compileSymbolTransformation()
        pro = PMXDebugSnippetProcessor()
        for snippet in self._snippetsTransformation:
            snippet.execute(pro)
            text = pro.text
            if text:
                return text
        return text
    
class PMXPreference(PMXBundleItem):
    KEYS = [ 'settings' ]
    TYPE = 'preference'
    FOLDER = 'Preferences'
    EXTENSION = 'tmPreferences'
    PATTERNS = ['*.tmPreferences', '*.plist']

    def load(self, dataHash):
        super(PMXPreference, self).load(dataHash)
        for key in PMXPreference.KEYS:
            value = dataHash.get(key, None)
            if key == 'settings':
                value = PMXPreferenceSettings(value or {}, self)
            setattr(self, key, value)
    
    @property
    def hash(self):
        dataHash = super(PMXPreference, self).hash
        for key in PMXPreference.KEYS:
            value = getattr(self, key)
            if key == 'settings':
                value = value.hash
            dataHash[key] = 'value'
        return dataHash

    def update(self, dataHash):
        for key in dataHash.keys():
            value = dataHash.get(key, None)
            if key == 'settings':
                self.settings.update(value)
            else:
                setattr(self, key, value)
            
    @staticmethod
    def buildSettings(preferences):
        settings = PMXPreferenceMasterSettings()
        if preferences:
            for p in preferences:
                settings.append(p.settings)
        return settings
