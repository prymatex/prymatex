#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

from prymatex.qt import QtGui
from prymatex.utils import text as textutils

class CodeEditorToken(namedtuple('CodeEditorToken', 'start end scope chunk')):
    @property
    def group(self):
        return self.scope.rootGroupName()

class CodeEditorBlockUserData(QtGui.QTextBlockUserData):
    __slots__ = ('tokens', 'text', 'state', 'revision', 'indentation', 'blank')
    def __init__(self, tokens, text, state, revision):
        super(CodeEditorBlockUserData, self).__init__()
        self.tokens = tokens
        self.text = text
        self.state = state
        self.revision = revision
        self.indentation = textutils.white_space(text)
        self.blank = text.strip() == ""

    def tokenAt(self, pos):
        for token in self.tokens[::-1]:
            if token.start <= pos < token.end:
                return token
        return self.tokens[0]

    def blockText(self):
        return self.text

    def syntaxScope(self, cursor):
        position = cursor.positionInBlock()
        return (self.tokenAt(position - 1).scope, self.tokenAt(position).scope)

    def scopePosition(self, cursor):
        block = cursor.block()
        token = self.tokenAt(cursor.positionInBlock())
        return (block.position() + token.start, block.position() + token.end)
        
    def isEmpty(self):
        return self.state == -1
