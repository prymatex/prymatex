#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.support import Scope
from prymatex.support.processor import SyntaxProcessorMixin
from prymatex.utils import text as textutils

from .base import CodeEditorBaseProcessor
from ..userdata import CodeEditorBlockUserData, CodeEditorToken

def _revision(scope, text, state):
    return hash("%s:%s:%d" % (scope, text, state))

class CodeEditorSyntaxProcessor(CodeEditorBaseProcessor, SyntaxProcessorMixin):
    NO_STATE = -1
    SINGLE_LINE = 1
    MULTI_LINE = 2
    NO_REVISION = -1

    def __init__(self, editor):
        CodeEditorBaseProcessor.__init__(self, editor)
        self.stack = []
        self.scope = None
        self.state = self.NO_STATE
        self.stacks = {}
        default_syntax = self.editor.application().supportManager.getBundleItem(self.editor.default_syntax)
        self.setScopeName(default_syntax.scopeName)
    
    def setScopeName(self, name):
        self.scope_name = name
        self.empty_scope = Scope(self.scope_name)
        self.empty_token = CodeEditorToken(0, 0, self.empty_scope, "")
        self.empty_user_data = CodeEditorBlockUserData((self.empty_token, ), self.NO_STATE, self.NO_REVISION, "", True)
    
    def scopeName(self):
        return self.scope_name

    def emptyUserData(self):
        return self.empty_user_data

    def managed(self):
        return True

    def beginExecution(self, bundleItem):
        if self.bundleItem == bundleItem:
            return
        
        self.editor.syntaxHighlighter.stop()

        # Get Wrapped Syntax
        syntax = self.editor.application().supportManager.getBundleItem(bundleItem.uuid)

        # ------------ Previous syntax
        if self.isReady():
            self.endExecution(self.bundleItem)

        CodeEditorBaseProcessor.beginExecution(self, syntax)
        
        self.beginParse(syntax.scopeName)
        
        self.editor.syntaxHighlighter.start()
        self.editor.syntaxChanged.emit(syntax)

    def endExecution(self, bundleItem):
        self.endParse(bundleItem.scopeName)
        CodeEditorBaseProcessor.endExecution(self, bundleItem)
    
    def restore(self, state, revision):
        self.state = state
        if revision in self.stacks:
            self.stack, self.scope = self.stacks[revision]
        elif self.isReady():
            self.stack, self.scope = ([(self.bundleItem.grammar, None)], Scope(self.bundleItem.scopeName))

    def save(self, state, revision):
        if state == self.MULTI_LINE:
            self.stacks[revision] = (self.stack[:], self.scope.clone())

    def textRevision(self, text, previous_state):
        return _revision(self.scope_name, text, previous_state)

    def blockRevision(self, block):
        return self.textRevision(block.text() + "\n", block.previous().userState())

    def testRevision(self, block):
        return block.userData() is not None and block.userData().revision == self.blockRevision(block)
            
    def textUserData(self, text, previous_state=NO_STATE, previous_revision=NO_REVISION):
        if not self.isReady():
            return self.empty_user_data

        # ------ Restore State
        self.restore(previous_state, previous_revision)
                
        revision = _revision(self.scope_name, text, self.state)
        self.bundleItem.parseLine(self.stack, text, self)
        self.state = len(self.stack) > 1 and self.MULTI_LINE or self.SINGLE_LINE

        user_data = CodeEditorBlockUserData(tuple(self.__tokens), self.state, 
            revision, textutils.white_space(text), text.strip() == "")
        
        # ------- Save State
        self.save(self.state, revision)
        return user_data
        
    def blockUserData(self, block, previous_user_data=None):
        user_data = previous_user_data or block.previous().userData()
        return self.textUserData(
            block.text() + "\n",
            block.previous().userState(),
            user_data and user_data.revision or self.NO_REVISION
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
