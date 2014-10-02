#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import helpers
from prymatex.support import Scope
from prymatex.support.processor import SyntaxProcessorMixin
from prymatex.utils import text

from .base import CodeEditorBaseProcessor
from ..userdata import CodeEditorBlockUserData, CodeEditorToken

class CodeEditorSyntaxProcessor(CodeEditorBaseProcessor, SyntaxProcessorMixin):
    NO_STATE = -1
    SINGLE_LINE = 1
    MULTI_LINE = 2

    def __init__(self, editor):
        CodeEditorBaseProcessor.__init__(self, editor)
        self.stack = []
        self.scope = None
        self.state = self.NO_STATE
        self.stacks = {}

    def managed(self):
        return True

    def beginExecution(self, bundleItem):
        if self.bundleItem == bundleItem:
            return
        
        self.editor.syntaxHighlighter.stop()

        # Get Wrapped Syntax
        syntax = self.editor.application().supportManager.getBundleItem(bundleItem.uuid)

        # ------------ Previous syntax
        if self.bundleItem is not None:
            self.endExecution(self.bundleItem)

        CodeEditorBaseProcessor.beginExecution(self, syntax)

        self.stack = [(syntax.grammar, None)]
        self.beginParse(syntax.scopeName)
        
        self.editor.syntaxHighlighter.start()
        self.editor.syntaxChanged.emit()

    def endExecution(self, bundleItem):
        self.endParse(bundleItem.scopeName)
        CodeEditorBaseProcessor.endExecution(self, bundleItem)
    
    def restore(self, user_data):
        self.state = user_data.state
        if user_data.revision in self.stacks:
            self.stack, self.scope = self.stacks[user_data.revision]
        else:
            self.stack, self.scope = ([(self.bundleItem.grammar, None)], Scope(self.bundleItem.scopeName))

    def save(self, user_data):
        if self.state == self.MULTI_LINE:
            self.stacks[user_data.revision] = (self.stack[:], self.scope.clone())

    def scopeName(self):
        return self.bundleItem.scopeName

    def parseBlock(self, block):
        block_text = block.text() + "\n"
        revision = helpers.qt_int(hash("%s:%s:%d" % (self.scopeName(), block_text,
            self.state)))
        self.bundleItem.parseLine(self.stack, block_text, self)
        self.state = len(self.stack) > 1 and self.MULTI_LINE or self.SINGLE_LINE

        return tuple(self.__tokens), self.state, revision, text.white_space(block_text), block_text.strip() == ""

    def blockUserData(self, block):
        self.restore(self.editor.blockUserData(block.previous()))
        user_data = CodeEditorBlockUserData(*self.parseBlock(block))
        self.save(user_data)
        return user_data

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
