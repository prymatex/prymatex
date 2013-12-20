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
from prymatex.utils import osextra

from .base import BundleItem
from ..regexp import compileRegexp, SymbolTransformation

class PreferenceSettings(object):
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

    def __init__(self, dataHash = {}, preference = None):
        self.preference = preference
        self.update(dataHash)

    @property
    def bundle(self):
        return self.preference.bundle

    def dump(self):
        dataHash = {}
        for key in PreferenceSettings.KEYS:
            value = getattr(self, key, None)
            if value is not None:
                if key in self.INDENT_KEYS or key in self.FOLDING_KEYS:
                    value = value.pattern
                elif key == 'shellVariables':
                    value = [ {'name': name, 'value': value } for name, value in  value ]
                elif key == 'symbolTransformation':
                    value = "%s" % value
                elif key == 'showInSymbolList':
                    value = value and "1" or "0"
                elif key == 'spellChecking':
                    value = value and "1" or "0"
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

class PreferenceMasterSettings(object):
    INDENT_INCREASE = 0
    INDENT_DECREASE = 1
    INDENT_NEXTLINE = 2
    UNINDENT = 3
    FOLDING_NONE = 0
    FOLDING_START = 1
    FOLDING_STOP = 2
    FOLDING_INDENTED_START = 3
    FOLDING_INDENTED_IGNORE = 4
    TRANSFORMATION_PATTERN = compileRegexp(r"s(/.+/.+/\w*);")

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
        for index, settings in enumerate(self.settings):
            if settings.showInSymbolList is not None:
                return settings.showInSymbolList
        return False

    @property
    def symbolTransformation(self):
        for index, settings in enumerate(self.settings):
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
        shellVariables = []
        variableNames = set()
        for settings in self.settings:
            if settings.shellVariables:
                # Only if not has all variables
                if all([ name not in variableNames for name, _ in settings.shellVariables]):
                    context = settings.bundle.variables
                    for name, value in settings.shellVariables:
                        value = osextra.path.expand_shell_variables( value,
                            context = context)
                        shellVariables.append((name, value))
                        context[name] = value
                        variableNames.add(name)
        return shellVariables

    @property
    def spellChecking(self):
        for settings in self.settings:
            if settings.spellChecking is not None:
                return settings.spellChecking
        return True
        
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
        return transformation and transformation.transform(text) or ""

    def indent(self, line):
        if not hasattr(self, "_indent_settings"):
            self._indent_settings = None
            for settings in self.settings:
                if any([getattr(settings, indentKey) for indentKey in PreferenceSettings.INDENT_KEYS]):
                    self._indent_settings = settings
                    break
        indent = []
        if self._indent_settings is not None:
            #IncreasePattern on return indent nextline
            #DecreasePattern evaluate line to decrease, no requiere del return
            #IncreaseOnlyNextLine on return indent nextline only
            #IgnoringLines evaluate line to unindent, no require el return
            if self._indent_settings.decreaseIndentPattern is not None and \
                self._indent_settings.decreaseIndentPattern.search(line):
                indent.append(self.INDENT_DECREASE)
            if self._indent_settings.increaseIndentPattern is not None and \
                self._indent_settings.increaseIndentPattern.search(line):
                indent.append(self.INDENT_INCREASE)
            if self._indent_settings.indentNextLinePattern is not None and \
                self._indent_settings.indentNextLinePattern.search(line):
                indent.append(self.INDENT_NEXTLINE)
            if self._indent_settings.unIndentedLinePattern is not None and \
                self._indent_settings.unIndentedLinePattern.search(line):
                indent.append(self.UNINDENT)
        return indent

    def folding(self, line):
        if not hasattr(self, "_folding_settings"):
            self._folding_settings = None
            for settings in self.settings:
                if any([getattr(settings, foldingKey) for foldingKey in PreferenceSettings.FOLDING_KEYS]):
                    self._folding_settings = settings
                    break
        if self._folding_settings is not None:
            start_match = self._folding_settings.foldingStartMarker.search(line) \
                if self._folding_settings.foldingStartMarker is not None else None
            stop_match = self._folding_settings.foldingStopMarker.search(line) \
                if self._folding_settings.foldingStopMarker is not None else None
            if start_match is not None and stop_match is None:
                return self.FOLDING_START
            elif start_match is None and stop_match is not None:
                return self.FOLDING_STOP
            # Ahora probamos los de indented
            if self._folding_settings.foldingIndentedBlockStart is not None and \
                self._folding_settings.foldingIndentedBlockStart.search(line):
                return self.FOLDING_INDENTED_START
            if self._folding_settings.foldingIndentedBlockIgnore is not None and \
                self._folding_settings.foldingIndentedBlockIgnore.search(line):
                return self.FOLDING_INDENTED_IGNORE
        return self.FOLDING_NONE

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
                value = PreferenceSettings(value or {}, self)
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
    def buildSettings(preferences):
        """El orden si importa, las preferences vienen ordenadas por score"""
        return PreferenceMasterSettings([p.settings for p in preferences])
