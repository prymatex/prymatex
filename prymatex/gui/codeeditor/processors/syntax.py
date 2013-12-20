#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import CodeEditorBaseProcessor
from prymatex.support.processor import SyntaxProcessorMixin
from prymatex.gui.codeeditor.userdata import CodeEditorTokenData

def build_userData_hash(scope, text, state):
    return hash("%s:%s:%d" % (scope, text, state))

class CodeEditorSyntaxProcessor(CodeEditorBaseProcessor, SyntaxProcessorMixin):
    NO_STATE = -1
    SINGLE_LINE = 1
    MULTI_LINE = 2

    def __init__(self, editor):
        CodeEditorBaseProcessor.__init__(self, editor)
        self.stack = []
        self.scopes = []

    def managed(self):
        return True

    def beginExecution(self, bundleItem):
        if self.bundleItem == bundleItem:
            return

        self.editor.syntaxHighlighter.stop()
        self.editor.aboutToHighlightChange.emit()
        
        # ------------ Previous syntax
        if self.bundleItem is not None:
            self.endExecution(self.bundleItem)
        
        # Set syntax
        CodeEditorBaseProcessor.beginExecution(self, bundleItem)
        self.stack = [(bundleItem.grammar, None)]
        self.beginParse(bundleItem.scopeName)

        self.editor.syntaxChanged.emit(bundleItem)
        
        # Run
        self.editor.syntaxHighlighter.runAsyncHighlight(self.editor.highlightChanged.emit)

    def endExecution(self, bundleItem):
        self.endParse(bundleItem.scopeName)
        CodeEditorBaseProcessor.endExecution(self, bundleItem)
    
    def restoreState(self, block):
        if block.isValid():
            stack, scopes = self.editor.blockUserData(block).processorState()
            self.stack = stack[:]
            self.scopes = scopes[:]

    def saveState(self, block):
        self.editor.blockUserData(block).setProcessorState((self.stack[:], self.scopes[:]))

    def blockUserData(self, block):
        text = block.text() + "\n"
        userDataHash = build_userData_hash(self.bundleItem.scopeName, 
            text, block.previous().userState())
        userData = self.editor.blockUserData(block)
        if not userData.testStateHash(userDataHash):
            self.restoreState(block.previous())
            self.bundleItem.parseLine(self.stack, text, self)
            
            userData.setTokens(self.__tokens)
            userData.setBlank(text.strip() == "")
            self.editor.processBlockUserData(text, block, userData)

            userData.setStateHash(userDataHash)

            # Store stack and state
            block.setUserState(len(self.stack) > 1 and self.MULTI_LINE or self.SINGLE_LINE)
            self.saveState(block)
        return userData

    # -------- Parsing
    def beginParse(self, scopeName):
        self.scopes = [ scopeName ]

    def endParse(self, scopeName):
        self.scopes.pop()

    # -------- Line
    def beginLine(self, line):
        self.line = line
        self.__tokens = []
        self.__indexes = []
        for _ in self.scopes:
            self.openToken(0)

    def endLine(self, line):
        self.closeToken(len(self.line), closeAll=True)

    # -------- Tag
    def openTag(self, scopeName, position):
        #Open token
        self.openToken(position)
        self.scopes.append(scopeName)

    def closeTag(self, scopeName, position):
        self.closeToken(position)
        self.scopes.pop()

    # --------- Create tokens
    def openToken(self, start):
        self.__tokens.append(None)
        self.__indexes.append((start, len(self.__tokens) - 1))

    def closeToken(self, end, closeAll=False):
        while self.__indexes:
            start, index = self.__indexes.pop()
            data = self.editor.flyweightScopeDataFactory(
                tuple(self.scopes))
            self.__tokens[index] = CodeEditorTokenData(
                start=start,
                end=end,
                data=data,
                chunk=self.line[start:end]
            )
            if not closeAll:
                break
