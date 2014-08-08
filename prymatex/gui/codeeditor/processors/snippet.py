#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui

from .base import CodeEditorBaseProcessor
from prymatex.support.processor import SnippetProcessorMixin

class CodeEditorSnippetProcessor(CodeEditorBaseProcessor, SnippetProcessorMixin):
    def configure(self, **kwargs):
        CodeEditorBaseProcessor.configure(self, **kwargs)
        self.snippetWrapper = QtGui.QTextCursor(self.textCursor)
        self.tabKeyBehavior = kwargs.get("tabKeyBehavior",
            self.editor.tabKeyBehavior())
        self.indentation = kwargs.get("indentation", 
            self.editor.indentation())
        self.backward = False

    # ---------- Override SnippetProcessorMixin API
    def managed(self):
        return True

    def beginRender(self):
        self.output = ""
        self.__startPosition = self.caretPosition()

    def endRender(self):
        self.__endPosition = self.caretPosition()
        self.editor.updatePlainText(self.output, self.snippetWrapper)
        self.snippetWrapper = self.editor.newCursorAtPosition(
                self.__startPosition, self.__endPosition
        )

    def caretPosition(self):
        return self.snippetWrapper.selectionStart() + len(self.output)

    def insertText(self, text):
        # Replace new lines and tabs
        text = text.replace('\n', '\n' + self.indentation)
        self.output += text.replace('\t', self.tabKeyBehavior)
    
    def selectHolder(self):
        start, end = self.bundleItem.currentPosition()
        self.editor.setTextCursor(self.editor.newCursorAtPosition(start, end))
        choices = self.bundleItem.holderChoices()
        if choices:
            self.editor.showFlatPopupMenu(choices, self.setHolderChoiceIndex)

    def runShellScript(self, script):
        context = self.editor.application.supportManager.runSystemCommand(
            shellCommand = script,
            environment = self.environmentVariables(),
            shellVariables = self.shellVariables()
        )
        return context.outputValue.strip()
    
    def setHolderChoiceIndex(self, index):
        if index != -1:
            self.bundleItem.setHolderContent(index)
            self.render()
            if self.nextHolder():
                self.selectHolder()
        elif self.backward and self.previousHolder() or self.nextHolder():
            self.selectHolder()

    # ---------- Public API
    def stop(self):
        self.endExecution(self.bundleItem)

    def render(self):
        self.bundleItem.render(self)
    
    # ---------- Holder navigation
    def nextHolder(self):
        self.backward = False
        return self.bundleItem.nextHolder()

    def previousHolder(self):
        self.backward = True
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