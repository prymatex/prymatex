#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

from prymatex.qt import QtGui
from prymatex.support import Scope

from prymatex.support import PreferenceMasterSettings

class CodeEditorToken(namedtuple('CodeEditorToken', 'start end scope chunk')):
    __slots__ = ()
    @property
    def group(self):
        return self.scope.rootGroupName()

_empty_token = CodeEditorToken(0, 0, Scope(), "")

class CodeEditorBlockUserData(QtGui.QTextBlockUserData):
    __slots__ = ('tokens', 'state', 'revision', 'indentation', 'blank')
    def __init__(self, tokens, state, revision, indentation, blank):
        super(CodeEditorBlockUserData, self).__init__()
        self.tokens = tokens
        self.state = state
        self.revision = revision
        self.indentation = indentation
        self.blank = blank

    @property
    def foldingMark(self):
        return PreferenceMasterSettings.FOLDING_NONE

    def tokenAt(self, pos):
        for token in self.tokens[::-1]:
            if token.start <= pos < token.end:
                return token
        return _empty_token

_empty_user_data = CodeEditorBlockUserData((), -1, -1, "", True)
