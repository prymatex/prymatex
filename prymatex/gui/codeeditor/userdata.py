#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

from prymatex.qt import QtGui
from prymatex.support import Scope

class CodeEditorToken(namedtuple('CodeEditorToken', 'start end scope chunk')):
    __slots__ = ()
    @property
    def group(self):
        return self.scope.rootGroupName()

class CodeEditorBlockUserData(QtGui.QTextBlockUserData):
    __slots__ = ('tokens', 'state', 'revision', 'indentation', 'blank')
    def __init__(self, tokens, state, revision, indentation, blank):
        super(CodeEditorBlockUserData, self).__init__()
        self.tokens = tokens
        self.state = state
        self.revision = revision
        self.indentation = indentation
        self.blank = blank

    def tokenAt(self, pos):
        for token in self.tokens[::-1]:
            if token.start <= pos < token.end:
                return token
        return self.tokens[0]

    def syntaxScope(self, cursor):
        left = cursor.position() - cursor.selectionStart() - 1
        right = cursor.position() - cursor.selectionStart()
        return (self.tokenAt(left).scope, self.tokenAt(right).scope)

    def isEmpty(self):
        return self.state == -1
