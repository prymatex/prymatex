#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import CodeEditorBaseProcessor
from prymatex.support.processor import SyntaxProcessorMixin
from prymatex.gui.codeeditor.userdata import CodeEditorTokenData

def build_userData_hash(scope, text, state):
    return hash("%s:%s:%d" % (scope, text, state))

class CodeEditorSyntaxProcessor(CodeEditorBaseProcessor, SyntaxProcessorMixin):
    def blockUserData(self, block):
        text = block.text() + "/n"
        userDataHash = build_userData_hash(self.bundleItem.scopeName, 
            text, block.previous().userState())
        userData = self.editor.blockUserData(block)
        if not userData.testStateHash(userDataHash):
            self.bundleItem.parseLine(stack, text, self)
            
            userData.setBlank(text.strip() == "")
            
            self.editor.processBlockUserData(text, block, userData)

            userData.setStateHash(userDataHash)

            # Store stack and state
            block.setUserState(len(stack) > 1 and self.MULTI_LINE or self.SINGLE_LINE)
            userData.setProcessorState((stack[:], processor.scopes()[:])) #Store copy
                    
        return userData

    # -------- Public api
    def tokens(self):
        return self.__tokens

    def setScopes(self, scopes):
        self.stackScopes = scopes

    def scopes(self):
        return self.stackScopes

    # -------- Parsing
    def beginParse(self, scopeName):
        self.setScopes([ scopeName ])

    def endParse(self, scopeName):
        pass

    # -------- Line
    def beginLine(self, line):
        self.line = line
        self.__tokens = []
        self.__indexes = []
        for _ in self.stackScopes:
            self.openToken(0)

    def endLine(self, line):
        self.closeToken(len(self.line), closeAll=True)

    # -------- Tag
    def openTag(self, scopeName, position):
        #Open token
        self.openToken(position)
        self.stackScopes.append(scopeName)

    def closeTag(self, scopeName, position):
        self.closeToken(position)
        self.stackScopes.pop()

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
