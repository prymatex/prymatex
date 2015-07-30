#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui
from prymatex.utils import html

from .base import CodeEditorBaseProcessor
from prymatex.support.processor import CommandProcessorMixin

class CodeEditorCommandProcessor(CodeEditorBaseProcessor, CommandProcessorMixin):
    def configure(self, **kwargs):
        CodeEditorBaseProcessor.configure(self, **kwargs)
        self.inputWrapper = QtGui.QTextCursor(self.textCursor)
        self.asynchronous = kwargs.get("asynchronous", True)
        self.disableIndent = kwargs.get("disableIndent", False)
        self.errorCommand = kwargs.get("errorCommand", False)
        
    def _format_input(self, source, f):
        if f == "xml":
            # TODO Terminar la salida en XML, esta mal, hay que usar xml_difference de scope
            firstBlock, lastBlock = self.editor.selectionBlockStartEnd(self.inputWrapper)
            startIndex = self.inputWrapper.selectionStart() - firstBlock.position()
            endIndex = self.inputWrapper.selectionEnd() - lastBlock.position()
            result = []
            block = firstBlock
            for line in source.splitlines(True):
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
                token = userData.tokenAt(start)
                for index in ranges:
                    lineXML += token.scope.to_xml(line[start:index])
                    token = userData.tokenAt(index)
                    start = index
                result.append(lineXML)
                if block == lastBlock:
                    break
                block = block.next()
            return self.editor.lineSeparator().join(result)
        return source
    
    # --------------------- Inputs
    def _get_input(self, inputMode):
        source = self.editor.selectedTextWithEol(self.inputWrapper)
        if inputMode == "fallback":
            self.textCursor = self.inputWrapper
        return source

    def selection(self, inputFormat = None, inputMode = None):
        return self._format_input(self._get_input(inputMode), inputFormat)

    def document(self, inputFormat = None, inputMode = None):
        self.inputWrapper.select(QtGui.QTextCursor.Document)
        return self._format_input(self._get_input(inputMode), inputFormat)

    def line(self, inputFormat = None, inputMode = None):
        self.inputWrapper.select(QtGui.QTextCursor.LineUnderCursor)
        return self._format_input(self._get_input(inputMode), inputFormat)

    def character(self, inputFormat = None, inputMode = None):
        self.inputWrapper.movePosition(QtGui.QTextCursor.NextCharacter, QtGui.QTextCursor.KeepAnchor)
        return self._format_input(self._get_input(inputMode), inputFormat)

    def scope(self, inputFormat=None, inputMode=None):
        start, end = self.blockUserData(self.inputWrapper.block()).scopePosition(self.inputWrapper)
        self.inputWrapper.setPosition(start)
        self.inputWrapper.setPosition(end, QtGui.QTextCursor.KeepAnchor)
        return self._format_input(self._get_input(inputMode), inputFormat)

    def selectedText(self, inputFormat = None, inputMode = None):
        return self._format_input(self._get_input(inputMode), inputFormat)

    def word(self, inputFormat = None, inputMode = None):
        _, start, end = self.editor.currentWord()
        self.inputWrapper.setPosition(start)
        self.inputWrapper.setPosition(end, QtGui.QTextCursor.KeepAnchor)
        return self._format_input(self._get_input(inputMode), inputFormat)

    # ----------------- Before Running Command
    def saveModifiedFiles(self):
        ret = True
        for editor in self.editor.window().editors():
            if editor.isModified():
                self.editor.window().saveEditor(editor = editor)
                ret = ret and not editor.isModified()
            if ret == False:
                break
        return ret

    def saveActiveFile(self):
        self.editor.window().saveEditor(editor=self.editor)
        return self.editor.hasFile() and not self.editor.isModified()

    # ------------------- Outpus function
    def error(self, context, outputFormat=None):
        if self.errorCommand:
            raise Exception(context.errorValue)
        else:
            print(context)
            def show_error(window, desc, value, _type):
                def _show_error():
                    window.showErrorInBrowser(desc, value, _type,
                        errorCommand=True)
                return _show_error
            QtCore.QTimer.singleShot(0, show_error(
                self.editor.window(),
                context.description(),
                context.errorValue,
                context.outputType           
            ))

    def discard(self, context, outputFormat = None):
        pass

    def replaceSelectedText(self, context, outputFormat=None):
        self.editor.updatePlainText(context.outputValue, cursor=self.inputWrapper)

    def replaceDocument(self, context, outputFormat=None):
        self.editor.updatePlainText(context.outputValue)

    def replaceSelection(self, context, outputFormat=None):
        print("replaceSelection")

    # ------------ Version 2
    def replaceInput(self, context, outputFormat = None):
        if outputFormat == "text":
            self.inputWrapper.insertText(context.outputValue)
        elif outputFormat == "html":
            self.inputWrapper.appendHtml(context.outputValue)
        elif outputFormat == "snippet":
            self.insertAsSnippet(context)

    def insertText(self, context, outputFormat=None):
        self.inputWrapper.insertText(context.outputValue)

    def atCaret(self, context, outputFormat=None):
        print("atCaret")

    def afterInput(self, context, outputFormat=None):
        print("afterInput")

    def afterSelectedText(self, context, outputFormat=None):
        self.inputWrapper.setPosition(self.inputWrapper.selectionEnd())
        self.inputWrapper.insertText(context.outputValue)

    def insertAsSnippet(self, context, outputFormat=None):
        # Build Snippet
        print(context.outputValue)
        snippet = self.editor.application().supportManager.buildAdHocSnippet(
            context.outputValue, context.bundleItem.bundle,
            tabTrigger = context.bundleItem.tabTrigger)
        # Insert snippet
        self.editor.insertBundleItem(snippet,
            textCursor = self.textCursor,
            disableIndent = self.disableIndent)

    def showAsHTML(self, context, outputFormat=None):
        self.editor.browserDock.setRunningContext(context)

    def showAsTooltip(self, context, outputFormat=None):
        message = html.escape(context.outputValue.strip())
        timeout = len(message) * 20
        if timeout > 2000:
            timeout = 2000
        
        callbacks = {
            'copy': lambda s = message: self.editor.application().clipboard().setText(s)
        }

        point = self.editor.viewport().mapToGlobal(
            self.editor.cursorRect(self.editor.textCursor()).bottomRight()
        )

        self.editor.showMessage(message,
            frmt=outputFormat or "text", 
            timeout=timeout,
            point=point,
            links=callbacks)

    def toolTip(self, context, outputFormat=None):
        self.showAsTooltip(context, outputFormat)

    def createNewDocument(self, context, outputFormat=None):
        editor= self.editor.window().addEmptyEditor()
        editor.setPlainText(context.outputValue)

    def newWindow(self, context, outputFormat=None):
        if outputFormat == "html":
            self.editor.browserDock.newRunningContext(context)
        elif outputFormat == "text":
            # TODO: Quiza una mejor forma de crear documentos con texto
            editor = self.editor.window().addEmptyEditor()
            editor.setPlainText(context.outputValue)

    def openAsNewDocument(self, context, outputFormat=None):
        editor = self.editor.window().addEmptyEditor()
        editor.setPlainText(context.outputValue)
