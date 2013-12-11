#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.support.processor import PMXSyntaxProcessor
from prymatex.gui.codeeditor.userdata import CodeEditorTokenData


class CodeEditorSyntaxProcessor(PMXSyntaxProcessor):
    def __init__(self, editor):
        self.editor = editor

    # -------- Public api
    def tokens(self):
        return self.__tokens

    def setScopes(self, scopes):
        self.stackScopes = scopes

    def scopes(self):
        return self.stackScopes

    # -------- START PARSING
    def startParsing(self, scope):
        self.setScopes([scope])

    # -------- BEGIN NEW LINE
    def beginLine(self, line):
        self.line = line
        self.__tokens = []
        self.__indexes = []
        for _ in self.stackScopes:
            self.openToken(0)

    # -------- OPEN TAG
    def openTag(self, scope, position):
        #Open token
        self.openToken(position)
        self.stackScopes.append(scope)

    # -------- CLOSE TAG
    def closeTag(self, scope, position):
        self.closeToken(position)
        self.stackScopes.pop()

    # --------  END LINE
    def endLine(self, line):
        self.closeToken(len(self.line), closeAll=True)

    # -------- END PARSING
    def endParsing(self, scope):
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
