#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import CodeEditorBaseProcessor
from prymatex.support.processor import SyntaxProcessorMixin
from prymatex.gui.codeeditor.userdata import CodeEditorTokenData

class CodeEditorSyntaxProcessor(CodeEditorBaseProcessor, SyntaxProcessorMixin):
    # -------- Public api
    def tokens(self):
        return self.__tokens

    def setScopes(self, scopes):
        self.stackScopes = scopes

    def scopes(self):
        return self.stackScopes

    # -------- START PARSING
    def beginExecution(self, syntax):
        self.setScopes([ syntax.name ])

    # -------- BEGIN NEW LINE
    def beginLine(self, line):
        self.line = line
        self.__tokens = []
        self.__indexes = []
        for _ in self.stackScopes:
            self.openToken(0)

    # -------- OPEN TAG
    def openTag(self, scopeName, position):
        #Open token
        self.openToken(position)
        self.stackScopes.append(scopeName)

    # -------- CLOSE TAG
    def closeTag(self, scopeName, position):
        self.closeToken(position)
        self.stackScopes.pop()

    # --------  END LINE
    def endLine(self, line):
        self.closeToken(len(self.line), closeAll=True)

    # -------- END PARSING
    def endExecution(self, syntax):
        pass

    # --------- Create tokens
    def openToken(self, start):
        self.__tokens.append(None)
        self.__indexes.append((start, len(self.__tokens) - 1))

    def closeToken(self, end, closeAll=False):
        while self.__indexes:
            start, index = self.__indexes.pop()
            data = self.editor.flyweightScopeDataFactory(
                tuple(self.stackScopes))
            self.__tokens[index] = CodeEditorTokenData(
                start=start,
                end=end,
                data=data,
                chunk=self.line[start:end]
            )
            if not closeAll:
                break
