#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import CodeEditorBaseProcessor

from prymatex.support import Scope
from prymatex.support.processor import SyntaxProcessorMixin
from prymatex.gui.codeeditor.userdata import CodeEditorToken

def build_userData_revision(scope, text, state):
    return hash("%s:%s:%d" % (scope, text, state))

class CodeEditorSyntaxProcessor(CodeEditorBaseProcessor, SyntaxProcessorMixin):
    NO_STATE = -1
    SINGLE_LINE = 1
    MULTI_LINE = 2

    def __init__(self, editor):
        CodeEditorBaseProcessor.__init__(self, editor)
        self.stack = []
        self.scope = None

    def managed(self):
        return True

    def beginExecution(self, bundleItem):
        if self.bundleItem == bundleItem:
            return

        self.editor.syntaxHighlighter.stop()
        # ------------ Previous syntax
        if self.bundleItem is not None:
            self.endExecution(self.bundleItem)
        
        # Set syntax
        CodeEditorBaseProcessor.beginExecution(self, bundleItem)
        syntax = self.editor.application().supportManager.getBundleItem(bundleItem.uuid)

        self.stack = [(syntax.grammar, None)]
        self.beginParse(syntax.scopeName)
        
        self.editor.syntaxHighlighter.start()
        self.editor.syntaxChanged.emit(syntax)

    def endExecution(self, bundleItem):
        self.endParse(bundleItem.scopeName)
        CodeEditorBaseProcessor.endExecution(self, bundleItem)
    
    def restoreState(self, block):
        if block.isValid():
            self.stack, self.scope = self.editor.blockUserData(block).processorState()

    def saveState(self, block):
        self.editor.blockUserData(block).setProcessorState((self.stack[:], self.scope.clone()))

    def blockUserData(self, block):
        text = block.text() + "\n"
        revision = build_userData_revision(self.bundleItem.scopeName, 
            text, block.previous().userState())

        userData = self.editor.blockUserData(block)
        if block.revision() != revision:

            self.restoreState(block.previous())
            self.bundleItem.parseLine(self.stack, text, self)
            
            userData.setTokens(self.__tokens)
            userData.setBlank(text.strip() == "")
            self.editor.processBlockUserData(text, block, userData)

            block.setRevision(revision)

            # Store stack and state
            block.setUserState(len(self.stack) > 1 and self.MULTI_LINE or self.SINGLE_LINE)
            self.saveState(block)
        return userData

    # -------- Parsing
    def beginParse(self, scopeName):
        self.scope = Scope(scopeName)

    def endParse(self, scopeName):
        self.scope.pop_scope()

    # -------- Line
    def beginLine(self, line):
        self.line = line
        self.__tokens = []
        self.__indexes = []
        for _ in range(self.scope.size()):
            self.openToken(0)

    def endLine(self, line):
        self.closeToken(len(self.line), closeAll=True)

    # -------- Tag
    def openTag(self, scopeName, position):
        #Open token
        self.openToken(position)
        self.scope.push_scope(scopeName)

    def closeTag(self, scopeName, position):
        self.closeToken(position)
        self.scope.pop_scope()

    # --------- Create tokens
    def openToken(self, start):
        self.__tokens.append(None)
        self.__indexes.append((start, len(self.__tokens) - 1))

    def closeToken(self, end, closeAll=False):
        while self.__indexes:
            start, index = self.__indexes.pop()
            self.__tokens[index] = CodeEditorToken(
                start=start,
                end=end,
                scope=self.scope.clone(),
                chunk=self.line[start:end]
            )
            if not closeAll:
                break
