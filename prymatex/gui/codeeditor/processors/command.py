#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui

from .base import CodeEditorBaseProcessor
from prymatex.support.processor import CommandProcessorMixin

class CodeEditorCommandProcessor(CodeEditorBaseProcessor, CommandProcessorMixin):
    def configure(self, **kwargs):
        CodeEditorBaseProcessor.configure(self, **kwargs)
        self.inputWrapper = QtGui.QTextCursor(self.textCursor)
        self.asynchronous = kwargs.get("asynchronous", True)
        self.disableIndent = kwargs.get("disableIndent", False)
        self.errorCommand = kwargs.get("errorCommand", False)
        
    def formatAsXml(self, text, firstBlock, lastBlock, startIndex, endIndex):
        result = []
        block = firstBlock
        for line in text.splitlines(True):
            userData = self.editor.blockUserData(block)
            if block == firstBlock and block == lastBlock:
                ranges = userData.ranges(start = startIndex, end = endIndex)
            elif block == firstBlock:
                ranges = userData.ranges(start = startIndex)
            elif block == lastBlock:
                ranges = userData.ranges(end = endIndex)
            else:
                ranges = userData.ranges()
            lineXML = ""
            start = ranges.pop(0)
            token = userData.tokenAtPosition(start)
            for index in ranges:
                lineXML += token.scope.to_xml(line[start:index])
                token = userData.tokenAtPosition(index)
                start = index
            # TODO Ver si esta bien esto del replace
            result.append(lineXML.replace('\n', ''))
            if block == lastBlock:
                break
            block = block.next()
        return "\n".join(result)
    
    # --------------------- Inputs
    def selection(self, inputFormat = None):
        if self.inputWrapper.hasSelection():
            text = self.editor.selectedTextWithEol(self.inputWrapper)
            if inputFormat == "xml":
                firstBlock, lastBlock = self.editor.selectionBlockStartEnd()
                return self.formatAsXml(text, firstBlock, lastBlock,
                    self.inputWrapper.selectionStart() - firstBlock.position(),
                    self.inputWrapper.selectionEnd() - lastBlock.position())
            else:
                return text

    def document(self, inputFormat = None):
        self.inputWrapper.select(QtGui.QTextCursor.Document)
        return self.selection(inputFormat)

    def line(self, inputFormat = None):
        self.inputWrapper.select(QtGui.QTextCursor.LineUnderCursor)
        return self.selection(inputFormat)

    def character(self, inputFormat = None):
        self.inputWrapper.movePosition(QtGui.QTextCursor.NextCharacter, QtGui.QTextCursor.KeepAnchor)
        return self.selection(inputFormat)

    def scope(self, inputFormat = None):
        token = self.editor.tokenAtPosition(self.inputWrapper.position())
        return token.chunk

    def selectedText(self, inputFormat = None):
        return self.selection(inputFormat)

    def word(self, inputFormat = None):
        word, start, end = self.editor.currentWord()
        self.inputWrapper.setPosition(start)
        self.inputWrapper.setPosition(end, QtGui.QTextCursor.KeepAnchor)
        return word

    # ----------------- Before Running Command
    def saveModifiedFiles(self):
        ret = True
        for editor in self.editor.mainWindow.editors():
            if editor.isModified():
                self.editor.mainWindow.saveEditor(editor = editor)
                ret = ret and not editor.isModified()
            if ret == False:
                break
        return ret

    def saveActiveFile(self):
        self.editor.mainWindow.saveEditor(editor = self.editor)
        return not (self.editor.isModified() or self.editor.isNew())

    # ------------------- Outpus function
    def error(self, context, outputFormat = None):
        if self.errorCommand:
            raise Exception(context.errorValue)
        else:
            self.editor.mainWindow.showErrorInBrowser(
                context.description(),
                context.errorValue,
                context.outputType,
                errorCommand = True
            )

    def discard(self, context, outputFormat = None):
        pass

    def replaceSelectedText(self, context, outputFormat = None):
        print(context.outputValue)
        self.editor.updatePlainText(context.outputValue, cursor = self.inputWrapper)

    def replaceDocument(self, context, outputFormat = None):
        self.editor.updatePlainText(context.outputValue)

    def replaceSelection(self, context, outputFormat = None):
        print("replaceSelection")

    # ------------ Version 2
    def replaceInput(self, context, outputFormat = None):
        if outputFormat == "text":
            self.inputWrapper.insertText(context.outputValue)
        elif outputFormat == "html":
            self.inputWrapper.appendHtml(context.outputValue)
        elif outputFormat == "snippet":
            self.insertAsSnippet(context)

    def insertText(self, context, outputFormat = None):
        self.inputWrapper.insertText(context.outputValue)

    def atCaret(self, context, outputFormat = None):
        print("atCaret")

    def afterInput(self, context, outputFormat = None):
        print("afterInput")

    def afterSelectedText(self, context, outputFormat = None):
        self.inputWrapper.setPosition(self.inputWrapper.selectionEnd())
        self.inputWrapper.insertText(context.outputValue)

    def insertAsSnippet(self, context, outputFormat = None):
        # Build Snippet
        snippet = self.editor.application.supportManager.buildAdHocSnippet(
            context.outputValue, context.bundleItem.bundle,
            tabTrigger = context.bundleItem.tabTrigger)
        # Insert snippet
        self.editor.insertBundleItem(snippet,
            textCursor = self.textCursor,
            disableIndent = self.disableIndent)

    def showAsHTML(self, context, outputFormat = None):
        self.editor.browserDock.setRunningContext(context)

    def showAsTooltip(self, context, outputFormat = None):
        message = context.outputValue.strip()
        timeout = len(message) * 20
        if timeout > 2000:
            timeout = 2000

        point = self.editor.cursorRect(self.inputWrapper).bottomRight()
        point = self.editor.mapToGlobal(point)
        callbacks = {
            'copy': lambda s = message: QtGui.qApp.instance().clipboard().setText(s)
        }

        self.editor.mainWindow.showMessage(message,
            frmt = outputFormat or "text", timeout = timeout, point = point,
            linkMap = callbacks)

    def toolTip(self, context, outputFormat = None):
        self.showAsTooltip(context, outputFormat)

    def createNewDocument(self, context, outputFormat = None):
        editor= self.editor.mainWindow.addEmptyEditor()
        editor.setPlainText(context.outputValue)

    def newWindow(self, context, outputFormat = None):
        if outputFormat == "html":
            self.editor.browserDock.newRunningContext(context)
        elif outputFormat == "text":
            # TODO: Quiza una mejor forma de crear documentos con texto
            editor = self.editor.mainWindow.addEmptyEditor()
            editor.setPlainText(context.outputValue)

    def openAsNewDocument(self, context, outputFormat = None):
        editor = self.editor.mainWindow.addEmptyEditor()
        editor.setPlainText(context.outputValue)
