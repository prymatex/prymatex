#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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

from prymatex.core import constants
from prymatex.utils import osextra

from .base import BundleItem
from ..regexp import compileRegexp, SymbolTransformation

class Settings(object):
    KEYS = (
        'completions', 'completionCommand', 'disableDefaultCompletion',
        'disableIndentCorrections', 'indentOnPaste',
        'characterClass', 'bold', 'italic', 'underline',
        'background', 'fontName', 'fontSize', 'foreground',
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

    def __init__(self, dataHash = {}, preference = None):
        self.preference = preference
        self.update(dataHash)


    @property
    def bundle(self):
        return self.preference.bundle

    def dump(self):
        dataHash = {}
        for key in Settings.KEYS:
            value = getattr(self, key, None)
            if value is not None:
                if key in self.INDENT_KEYS or key in self.FOLDING_KEYS:
                    value = value.pattern
                elif key == 'shellVariables':
                    value = [ {'name': name, 'value': value } for name, value in  value ]
                elif key == 'symbolTransformation':
                    value = "%s" % value
                elif key == 'showInSymbolList':
                    value = value and 1 or 0
                elif key == 'spellChecking':
                    value = value and 1 or 0
                dataHash[key] = value
        return dataHash

    def update(self, dataHash):
        for key in self.KEYS:
            value = dataHash.get(key, None)
            if value is not None:
                if key in self.INDENT_KEYS or key in self.FOLDING_KEYS:
                    value = compileRegexp( value )
                elif key == 'shellVariables':
                    value = [(d['name'], d['value']) for d in value]
                elif key == 'symbolTransformation':
                    value = SymbolTransformation(value)
                elif key == 'showInSymbolList':
                    value = bool(int(value))
                elif key == 'spellChecking':
                    value = bool(int(value))
            setattr(self, key, value)

class ContextSettings(object):
    def __init__(self, settings):
        self.settings = settings

    def _first(self, key, default=None):
        for settings in self.settings:
            attr = getattr(settings, key, None)
            if attr is not None:
                return attr
        return default
    
    completions = property(lambda self: self._first("completions", []))
    completionCommand = property(lambda self: self._first("completionCommand"))
    disableDefaultCompletion = property(lambda self: self._first("disableDefaultCompletion"))
    showInSymbolList = property(lambda self: self._first("showInSymbolList", False))
    symbolTransformation = property(lambda self: self._first("symbolTransformation"))
    highlightPairs = property(lambda self: self._first("highlightPairs"))
    smartTypingPairs = property(lambda self: self._first("smartTypingPairs"))

    def shellVariables(self):
        shellVariables = []
        takenNames = set()
        for settings in self.settings:
            variables = settings.shellVariables
            if variables is not None:
                names = [ variable[0] for variable in variables if variable[0].startswith("TM_") ]
                if not any([ name in takenNames for name in names ]):
                    shellVariables.extend(settings.preference.variables().items())
                    shellVariables.extend(variables)
                    takenNames.update(names)
        return shellVariables

    spellChecking = property(lambda self: self._first("spellChecking", True))
    decreaseIndentPattern = property(lambda self: self._first("decreaseIndentPattern"))
    increaseIndentPattern = property(lambda self: self._first("increaseIndentPattern"))
    indentNextLinePattern = property(lambda self: self._first("indentNextLinePattern"))
    unIndentedLinePattern = property(lambda self: self._first("unIndentedLinePattern"))
    foldingIndentedBlockStart = property(lambda self: self._first("foldingIndentedBlockStart"))
    foldingIndentedBlockIgnore = property(lambda self: self._first("foldingIndentedBlockIgnore"))
    foldingStartMarker = property(lambda self: self._first("foldingStartMarker"))
    foldingStopMarker = property(lambda self: self._first("foldingStopMarker"))
    
    def _getBundle(self, attrKey):
        for settings in self.settings:
            if getattr(settings, attrKey) is not None:
                return settings.preference.bundle

    def getManager(self, attrKey):
        for settings in self.settings:
            if getattr(settings, attrKey) is not None:
                return settings.preference.manager
    
    def transformSymbol(self, text):
        transformation = self.symbolTransformation
        return transformation and transformation.transform(text)

    def indentationFlag(self, line):
        #IncreasePattern on return indent nextline
        #DecreasePattern evaluate line to decrease, no requiere del return
        #IncreaseOnlyNextLine on return indent nextline only
        #IgnoringLines evaluate line to unindent, no require el return
        if self.decreaseIndentPattern and \
            self.decreaseIndentPattern.search(line):
            return constants.INDENT_DECREASE
        if self.increaseIndentPattern and \
            self.increaseIndentPattern.search(line):
            return constants.INDENT_INCREASE
        if self.indentNextLinePattern and \
            self.indentNextLinePattern.search(line):
            return constants.INDENT_NEXTLINE
        if self.unIndentedLinePattern and \
            self.unIndentedLinePattern.search(line):
            return constants.INDENT_UNINDENT
        return constants.INDENT_NONE

    def folding(self, line):
        start_match = self.foldingStartMarker.search(line) \
            if self.foldingStartMarker is not None else None
        stop_match = self.foldingStopMarker.search(line) \
            if self.foldingStopMarker is not None else None
        if start_match is not None and stop_match is None:
            return constants.FOLDING_START
        elif start_match is None and stop_match is not None:
            return constants.FOLDING_STOP
        # Ahora probamos los de indented
        if self.foldingIndentedBlockStart is not None and \
            self.foldingIndentedBlockStart.search(line):
            return constants.FOLDING_INDENTED_START
        if self.foldingIndentedBlockIgnore is not None and \
            self.foldingIndentedBlockIgnore.search(line):
            return constants.FOLDING_INDENTED_IGNORE
        return constants.FOLDING_NONE

class Preference(BundleItem):
    KEYS = ( 'settings', )
    FOLDER = 'Preferences'
    EXTENSION = 'tmPreferences'
    PATTERNS = ('*.tmPreferences', '*.plist')
    DEFAULTS = {
        'name': 'untitled',
    }
    def load(self, dataHash):
        BundleItem.load(self, dataHash)
        for key in Preference.KEYS:
            value = dataHash.get(key, None)
            if key == 'settings':
                value = Settings(value or {}, self)
            setattr(self, key, value)

    def update(self, dataHash):
        BundleItem.update(self, dataHash)
        for key in Preference.KEYS:
            if key in dataHash:
                value = dataHash.get(key)
                if key == 'settings':
                    self.settings.update(value)
                else:
                    setattr(self, key, value)

    def dump(self, allKeys = False):
        dataHash = BundleItem.dump(self, allKeys)
        for key in Preference.KEYS:
            value = getattr(self, key, None)
            if allKeys or value is not None:
                if key == 'settings' and value is not None:
                    value = value.dump()
                dataHash[key] = value
        return dataHash

    @staticmethod
    def buildSettings(settings):
        """El orden si importa, las preferences vienen ordenadas por score de mayor a menor"""
        return ContextSettings(settings)
