#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Preferences's module
    http://manual.macromates.com/en/preferences_items.html
    
    completions � an array of additional candidates when cycling through completion candidates from the current document.
    completionCommand � a shell command (string) which should return a list of candidates to complete the current word (obtained via the TM_CURRENT_WORD variable).
    disableDefaultCompletion � set to 1 if you want to exclude matches from the current document when asking for completion candidates (useful when you provide your own completion command).

    decreaseIndentPattern � regular expression.
    increaseIndentPattern � regular expression.
    indentNextLinePattern � regular expression.
    unIndentedLinePattern � regular expression.

    showInSymbolList � set to 1 to include in the symbol list.
    symbolTransformation � a �program� consisting of one or more s/�regexp�/�format�/�options�; transformations which will be applied to the extracted �symbol�.

    highlightPairs � an array of arrays, each containing a pair of characters where, when the caret moves over the second, the first one will be highlighted for a short moment, if found.
    smartTypingPairs � an array of arrays, each containing a pair of characters where when the first is typed, the second will be inserted. An example is shown below. For more information see auto-paired characters.

    shellVariables � an array of key/value pairs. See context dependent variables.
    spellChecking � set to 0/1 to disable/enable spell checking.
'''
import ponyguruma as onig
from ponyguruma.constants import OPTION_CAPTURE_GROUP
from prymatex.bundles.base import PMXBundleItem

onig_compile = onig.Regexp.factory(flags = OPTION_CAPTURE_GROUP)

class PMXSetting(dict):
    def __init__(self, hash):
        for key in [    'decreaseIndentPattern', 'increaseIndentPattern', 'indentNextLinePattern', 'unIndentedLinePattern' ]:
            if hash.has_key(key):
                hash[key] = onig_compile( hash[key] )

        super(PMXSetting, self).__init__(hash)

class PMXPreference(PMXBundleItem):
    def __init__(self, hash, name_space = "default"):
        super(PMXPreference, self).__init__(hash, name_space)
        for key in [ 'settings' ]:
            if key == 'settings':
                setattr(self, key, PMXSetting(hash.pop(key)))

    @staticmethod
    def buildSettings(preferences):
        settings = {}
        for p in preferences:
            settings.update(p.settings)
        return settings