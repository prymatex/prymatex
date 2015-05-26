#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui

from .base import CodeEditorBaseProcessor
from prymatex.support.processor import SnippetProcessorMixin

class CodeEditorSnippetProcessor(CodeEditorBaseProcessor, SnippetProcessorMixin):
    def __init__(self, editor):
        CodeEditorBaseProcessor.__init__(self, editor)
        self.__output = ""
        
    def lastOutput(self):
        return self.__output
        
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

    def beginExecution(self, bundleItem):
        super(CodeEditorSnippetProcessor, self).beginExecution(bundleItem)
        self.status = self.editor.showMessage("Snippet: %s" % bundleItem.name, timeout=0)
        self.render()

    def endExecution(self, bundleItem):
        super(CodeEditorSnippetProcessor, self).endExecution(bundleItem)
        self.status.close()

    def beginRender(self):
        self.__output = ""
        self.__startPosition = self.caretPosition()

    def endRender(self):
        self.__endPosition = self.caretPosition()
        self.editor.updatePlainText(self.__output, self.snippetWrapper)
        self.snippetWrapper = self.editor.newCursorAtPosition(
            self.__startPosition, self.__endPosition)
        # Select holder
        self.selectHolder()
        self.__render = False
        
    def caretPosition(self):
        return self.snippetWrapper.selectionStart() + len(self.__output)

    def insertText(self, text):
        # Replace new lines and tabs
        text = text.replace('\n', '\n' + self.indentation)
        self.__output += text.replace('\t', self.tabKeyBehavior)
    
    def selectHolder(self):
        start, end = self.bundleItem.currentPosition()
        self.editor.setTextCursor(self.editor.newCursorAtPosition(start, end))
        self.status.setText("Snippet: %s Holder: %d" % (self.bundleItem.name, self.bundleItem.holderNumber()))
        
        # Choices
        choices = self.bundleItem.holderChoices()
        if choices:
            self.editor.showFlatPopupMenu(choices, self.setHolderChoiceIndex)
            
    def runShellScript(self, script):
        command = script
        environment = self.environmentVariables()
        variables = self.shellVariables(environment)
        context = self.editor.application().supportManager.runSystemCommand(
            command = command,
            environment = environment,
            variables = variables
        )
        return context.outputValue.strip()
    
    def setHolderChoiceIndex(self, index):
        if index != -1:
            self.bundleItem.setHolderContent(index)
        self.backward and self.previousHolder() or self.nextHolder()
        self.render()

    # ---------- Public API
    def stop(self):
        self.endExecution(self.bundleItem)

    def render(self):
        self.bundleItem.render(self)

    # ---------- Holder navigation
    def nextHolder(self):
        self.backward = False
        if self.bundleItem.nextHolder():
            self.selectHolder()
        else:
            self.stop()

    def previousHolder(self):
        self.backward = True
        if self.bundleItem.previousHolder():
            self.selectHolder()
        else:
            self.stop()

    def isLastHolder(self):
        return self.isReady() and self.bundleItem.lastHolder()

    def setHolder(self, start, end):
        return self.isReady() and self.bundleItem.setHolder(start, end)

    def hasHolderContent(self):
        return self.isReady() and self.bundleItem.hasHolderContent()

    def setHolderContent(self, content):
        self.bundleItem.setHolderContent(content)

    # -------------- Snippet position
    def currentPosition(self):
        return self.bundleItem.currentPosition()
