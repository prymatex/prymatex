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

from prymatex.utils import osextra

from .base import PMXBundleItem
from ..regexp import compileRegexp, Transformation

class PMXPreferenceSettings(object):
    KEYS = (
        'completions', 'completionCommand', 'disableDefaultCompletion',
        'showInSymbolList', 'symbolTransformation', 'highlightPairs',
        'smartTypingPairs', 'shellVariables', 'spellChecking', 'softWrap',
        'indentedSoftWrap', 'foldingIndentedBlockStart',
        'foldingIndentedBlockIgnore', 'foldingStartMarker', 'foldingStopMarker',
        'decreaseIndentPattern', 'increaseIndentPattern',
        'indentNextLinePattern', 'unIndentedLinePattern' )
    INDENT_KEYS = ( 
        'decreaseIndentPattern', 'increaseIndentPattern',
        'indentNextLinePattern', 'unIndentedLinePattern' )
    FOLDING_KEYS = ( 
        'foldingIndentedBlockStart', 'foldingIndentedBlockIgnore',
        'foldingStartMarker', 'foldingStopMarker' )
    INDENT_INCREASE = 0
    INDENT_DECREASE = 1
    INDENT_NEXTLINE = 2
    UNINDENT = 3
    FOLDING_NONE = 0
    FOLDING_START = 1
    FOLDING_STOP = 2
    FOLDING_INDENTED_START = 3
    FOLDING_INDENTED_IGNORE = 4
    def __init__(self, dataHash = {}, preference = None):
        self.preference = preference
        self.update(dataHash)
    
    @property
    def bundle(self):
        return self.preference.bundle
    
    def dump(self):
        dataHash = {}
        for key in PMXPreferenceSettings.KEYS:
            value = getattr(self, key, None)
            if value != None:
                if key in self.INDENT_KEYS or key in self.FOLDING_KEYS:
                    value = value.pattern
                elif key in [ 'shellVariables' ]:
                    value = [ {'name': t[0], 'value': t[1] } for t in  value.items() ]
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
                if key in self.INDENT_KEYS or key in self.FOLDING_KEYS:
                    value = compileRegexp( value )
                elif key in [ 'shellVariables' ]:
                    value = dict([(d['name'], d['value']) for d in value])
                elif key in [ 'symbolTransformation' ]:
                    value = [value for value in [value.strip() for value in value.split(";")] if bool(value)]
                elif key in [ 'showInSymbolList' ]:
                    value = bool(int(value))
                elif key in [ 'spellChecking' ]:
                    value = bool(int(value))
            setattr(self, key, value)
    
class PMXPreferenceMasterSettings(object):
    def __init__(self, settings):
        self.settings = settings
    
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
    def disableDefaultCompletion(self):
        for settings in self.settings:
            if settings.disableDefaultCompletion is not None:
                return settings.disableDefaultCompletion
        
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
        return []
                
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
            if settings.shellVariables:
                for key, value in settings.shellVariables.items():
                    shellVariables[key] = osextra.path.expand_shell_variables(
                        value, context = settings.bundle.variables)
        return shellVariables
        
    @property
    def spellChecking(self):
        for settings in self.settings:
            if settings.spellChecking is not None:
                return settings.spellChecking
        return True
        
    @property
    def decreaseIndentPattern(self):
        settings = self.__findIndentSettings()
        if settings is not None:
            return settings.decreaseIndentPattern

    @property
    def increaseIndentPattern(self):
        settings = self.__findIndentSettings()
        if settings is not None:
            return settings.increaseIndentPattern

    @property
    def indentNextLinePattern(self):
        settings = self.__findIndentSettings()
        if settings is not None:
            return settings.indentNextLinePattern

    @property
    def unIndentedLinePattern(self):
        settings = self.__findIndentSettings()
        if settings is not None:
            return settings.unIndentedLinePattern
    @property
    def foldingIndentedBlockStart(self):
        if not hasattr(self, "_folding_indented_block_start"):
            for settings in self.settings:
                self._folding_indented_block_start = settings.foldingIndentedBlockStart
                if self._folding_indented_block_start is not None:
                    break
        return self._folding_indented_block_start
            
    @property
    def foldingIndentedBlockIgnore(self):
        if not hasattr(self, "_folding_indented_block_ignore"):
            for settings in self.settings:
                self._folding_indented_block_ignore = settings.foldingIndentedBlockIgnore
                if self._folding_indented_block_ignore is not None:
                    break
        return self._folding_indented_block_ignore
        
    @property
    def foldingStartMarker(self):
        if not hasattr(self, "_folding_start_marker"):
            for settings in self.settings:
                self._folding_start_marker = settings.foldingStartMarker
                if self._folding_start_marker is not None:
                    break
        return self._folding_start_marker
    
    @property
    def foldingStopMarker(self):
        if not hasattr(self, "_folding_stop_marker"):
            for settings in self.settings:
                self._folding_stop_marker = settings.foldingStopMarker
                if self._folding_stop_marker is not None:
                    break
        return self._folding_stop_marker
        
    def __findIndentSettings(self):
        #TODO: Algo de cache?
        for settings in self.settings:
            if any([getattr(settings, indentKey) is not None for indentKey in PMXPreferenceSettings.INDENT_KEYS]):
                return settings

    def _getBundle(self, attrKey):
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
        settings = self.__findIndentSettings()
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
        self._symbolTransformation = []
        for trans in self.symbolTransformation:
            if trans:
                self._symbolTransformation.append(Transformation(trans[2:]))
    
    def transformSymbol(self, text):
        if not hasattr(self, '_symbolTransformation'):
            self.compileSymbolTransformation()
        for trans in self._symbolTransformation:
            tt = trans.transform(text)
            if tt is not None:
                return tt
    
    def folding(self, line):
        start_match = self.foldingStartMarker.search(line) if self.foldingStartMarker is not None else None
        stop_match = self.foldingStopMarker.search(line) if self.foldingStopMarker is not None else None
        if start_match != None and stop_match == None:
            return PMXPreferenceSettings.FOLDING_START
        elif start_match == None and stop_match != None:
            return PMXPreferenceSettings.FOLDING_STOP
        # Ahora probamos los de indented
        if self.foldingIndentedBlockStart is not None and self.foldingIndentedBlockStart.search(line):
            return PMXPreferenceSettings.FOLDING_INDENTED_START
        if self.foldingIndentedBlockIgnore is not None and self.foldingIndentedBlockIgnore.search(line):
            return PMXPreferenceSettings.FOLDING_INDENTED_IGNORE
        return PMXPreferenceSettings.FOLDING_NONE
    
class PMXPreference(PMXBundleItem):
    KEYS = ( 'settings', )
    TYPE = 'preference'
    FOLDER = 'Preferences'
    EXTENSION = 'tmPreferences'
    PATTERNS = ('*.tmPreferences', '*.plist')
    DEFAULTS = {
        'name': 'untitled',
    }
    def load(self, dataHash):
        PMXBundleItem.load(self, dataHash)
        for key in PMXPreference.KEYS:
            value = dataHash.get(key, None)
            if key == 'settings':
                value = PMXPreferenceSettings(value or {}, self)
            setattr(self, key, value)
    
    def update(self, dataHash):
        PMXBundleItem.update(self, dataHash)
        for key in PMXPreference.KEYS:
            if key in dataHash:
                value = dataHash.get(key)
                if key == 'settings':
                    self.settings.update(value)
                else:
                    setattr(self, key, value)
    
    def dump(self, includeNone = False):
        dataHash = PMXBundleItem.dump(self, includeNone)
        for key in PMXPreference.KEYS:
            value = getattr(self, key, None)
            if includeNone or value != None:
                if key == 'settings' and value != None:
                    value = value.dump()
                dataHash[key] = value
        return dataHash

    @staticmethod
    def buildSettings(preferences):
        """El orden si importa, las preferences vienen ordenadas por score"""
        return PMXPreferenceMasterSettings([p.settings for p in preferences])
