#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui

from .base import CodeEditorBaseProcessor
from prymatex.support.processor import SnippetProcessorMixin

class CodeEditorSnippetProcessor(CodeEditorBaseProcessor, SnippetProcessorMixin):
    def configure(self, **kwargs):
        CodeEditorBaseProcessor.configure(self, **kwargs)
        self.tabKeyBehavior = kwargs.get("tabKeyBehavior",
            self.editor.tabKeyBehavior())
        self.indentation = kwargs.get("indentation", 
            self.editor.blockUserData(self.cursorWrapper.block()).indent)
        
    # ---------- Override SnippetProcessorMixin API
    def managed(self):
        return True

    def beginRender(self):
        self.output = ""
        self.__startPosition = self.caretPosition()

    def endRender(self):
        self.__endPosition = self.caretPosition()
        self.editor.updatePlainText(self.output, self.cursorWrapper)

    def caretPosition(self):
        return self.cursorWrapper.selectionStart() + len(self.output)

    def insertText(self, text):
        # Replace new lines and tabs
        text = text.replace('\n', '\n' + self.indentation)
        self.output += text.replace('\t', self.tabKeyBehavior)
    
    def selectHolder(self):
        start, end = self.bundleItem.currentPosition()
        self.editor.setTextCursor(self.editor.newCursorAtPosition(start, end))
        #if hasattr(holder, 'options'):
        #    self.editor.showFlatPopupMenu(
        #        holder.options, 
        #        lambda index, holder = holder: self.setSnippetHolderOption(holder, index), 
        #        cursorPosition = True)

    def runShellScript(self, script):
        context = self.editor.application.supportManager.runSystemCommand(
            shellCommand = script,
            environment = self.environmentVariables(),
            shellVariables = self.shellVariables()
        )
        return context.outputValue.strip()
    
    def setSnippetHolderOption(self, holder, index):
        if index >= 0:
            holder.setOptionIndex(index)
            # Wrap snippet
            wrapCursor = self.editor.newCursorAtPosition(
                self.startPosition(), self.endPosition())
            #Insert snippet
            self.render(wrapCursor)
            holder = self.nextHolder(holder)
            if holder is not None:
                self.selectHolder(holder)
    
    def endPosition(self):
        return self.__endPosition

    def startPosition(self):
        return self.__startPosition

    # ---------- Public API
    def stop(self):
        self.endExecution(self.bundleItem)

    def render(self, cursor):
        self.cursorWrapper = cursor
        self.bundleItem.render(self)
    
    # ---------- Holder navigation
    def nextHolder(self):
        return self.bundleItem.nextHolder()

    def previousHolder(self):
        return self.bundleItem.previousHolder()
    
    def lastHolder(self):
        return self.bundleItem.lastHolder()

    def setHolder(self, start, end):
        return self.bundleItem.setHolder(start, end)
    
    def hasHolderContent(self):
        return self.bundleItem.hasHolderContent()
        
    def setHolderContent(self, content):
        self.bundleItem.setHolderContent(content)

    # -------------- Snippet position
    def currentPosition(self):
        return self.bundleItem.currentPosition()