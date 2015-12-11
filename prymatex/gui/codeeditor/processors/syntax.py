#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.support import Scope
from prymatex.support.processor import SyntaxProcessorMixin

from .base import CodeEditorBaseProcessor
from ..userdata import CodeEditorBlockUserData, CodeEditorToken

def _revision(scope, text, state):
    return hash("%s:%s:%d" % (scope, text, state))

class CodeEditorSyntaxProcessor(CodeEditorBaseProcessor, SyntaxProcessorMixin):
    NOT_STATE = -1
    NOT_REVISION = -1
    CACHE = {}
    def __init__(self, editor):
        super().__init__(editor)
        self.stack = []
        self.scope = None
        self.stacks = {}
        node = self.editor.application().supportManager.getBundleItem(self.editor.default_syntax)
        print(node)
        self.setScopeName(node and node.bundleItem().scopeName or "")
    
    def setScopeName(self, name):
        self.scope_name = name
        self.empty_scope = Scope(self.scope_name)
        self.empty_token = CodeEditorToken(0, 0, self.empty_scope, "")
        self.empty_user_data = CodeEditorBlockUserData(
            (self.empty_token, ), "", self.NOT_STATE, self.NOT_REVISION
        )
    
    def scopeName(self):
        return self.scope_name

    def emptyUserData(self):
        return self.empty_user_data

    def managed(self):
        return True

    def beginExecution(self, bundleItem):
        if self.bundleItem is not None and self.bundleItem == bundleItem:
            return
        
        self.editor.syntaxHighlighter.stop()

        # Get Wrapped Syntax
        super().beginExecution(bundleItem)
        
        self.beginParse(bundleItem.scopeName)
        
        self.editor.syntaxHighlighter.start()
        self.editor.syntaxHighlighter.rehighlight()
        self.editor.showMessage("Syntax changed to <b>%s</b>" % bundleItem.name)
        self.editor.syntaxChanged.emit(bundleItem)

    def endExecution(self, bundleItem):
        self.endParse(bundleItem.scopeName)
        CodeEditorBaseProcessor.endExecution(self, bundleItem)

    def textRevision(self, text, previous_state):
        return _revision(self.scope_name, text, previous_state)

    def blockRevision(self, block):
        return self.textRevision(block.text() + "\n", block.previous().userState())

    def testRevision(self, block):
        return block.userData() is not None and block.userData().revision == self.blockRevision(block)
        
    def textUserData(self, text, previous_state=NOT_STATE, previous_revision=NOT_REVISION):
        if not self.isReady():
            return self.empty_user_data

        revision = _revision(self.scope_name, text, previous_state)
        if revision not in self.CACHE:
            # ------ Restore Stack State
            if previous_revision in self.stacks:
                self.stack, self.scope = self.stacks[previous_revision]
            else:
                self.stack, self.scope = ([(self.bundleItem.grammar, None)], Scope(self.bundleItem.scopeName))
    
            self.bundleItem.parseLine(self.stack, text, self)
            # ------- Save Stack State
            if len(self.stack) > 1:
                self.stacks[revision] = (self.stack[:], self.scope.clone())
            self.CACHE[revision] = (tuple(self.__tokens), text,
                hash(self.scope.back()) & (0xFFFFFFFF >> 2), revision
            )
        return CodeEditorBlockUserData(*self.CACHE[revision])
        
    def blockUserData(self, block, previous_user_data=None):
        user_data = previous_user_data or block.previous().userData()
        return self.textUserData(
            block.text() + "\n",
            block.previous().userState(),
            user_data and user_data.revision or self.NOT_REVISION
        )

    # -------- Parsing
    def beginParse(self, scopeName):
        self.setScopeName(scopeName)
        self.scope = Scope(scopeName)
        self.stack = [(self.bundleItem.grammar, None)]

    def endParse(self, scopeName):
        self.scope.pop_scope()
        self.stack = []

    # -------- Line
    def beginLine(self, line):
        self.line = line
        self.__tokens = []
        self.__indexes = []
        for _ in range(self.scope.size()):
            self.openToken(0)

    def endLine(self, line):
        while self.__indexes:
            self.closeToken(len(self.line))

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

    def closeToken(self, end):
        start, index = self.__indexes.pop()
        self.__tokens[index] = CodeEditorToken(
            start=start,
            end=end,
            scope=self.scope.clone(),
            chunk=self.line[start:end]
        )
