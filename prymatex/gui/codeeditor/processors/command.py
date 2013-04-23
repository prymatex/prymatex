#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui

from prymatex.support.processor import PMXCommandProcessor
from prymatex.support.snippet import PMXSnippet

class PMXCommandProcessor(PMXCommandProcessor):
    def __init__(self, editor):
        super(PMXCommandProcessor, self).__init__()
        self.editor = editor
        self.__env = {}

    def startCommand(self, command):
        self.command = command
        self.__env = command.environmentVariables()
        self.__env.update(self.editor.mainWindow.environmentVariables())
        self.__env.update(self.editor.environmentVariables())
        self.__env.update(self.baseEnvironment)
        
    def endCommand(self, command):
        self.command = None
        
    def environmentVariables(self):
        return self.__env
        
    def configure(self, settings):
        self.asynchronous = settings.get("asynchronous", True)
        self.tabTriggered = settings.get("tabTriggered", False)
        self.disableIndent = settings.get("disableIndent", False)
        self.baseEnvironment = settings.get("environment", {})
        self.errorCommand = settings.get("errorCommand", False)

    def formatAsXml(self, text, firstBlock, lastBlock, startIndex, endIndex):
        result = []
        block = firstBlock
        for line in text.splitlines():
            if block == firstBlock and block == lastBlock:
                scopes = block.userData().scopeRanges(start = startIndex, end = endIndex)
            elif block == firstBlock:
                scopes = block.userData().scopeRanges(start = startIndex)
            elif block == lastBlock:
                scopes = block.userData().scopeRanges(end = endIndex)
            else:
                scopes = block.userData().scopeRanges()
            lineXML = ""
            print scopes
            for (start, end), scope in scopes:
                ss = scope.split()
                token = "".join(map(lambda scope: "<" + scope + ">", ss))
                token += line[start:end]
                ss.reverse()
                token += "".join(map(lambda scope: "</" + scope + ">", ss))
                lineXML += token
            result.append(lineXML)
            if block == lastBlock:
                break
            block = block.next()
        return "\n".join(result)

    # --------------------- Inputs
    def document(self, format = None):
        #TODO: ver si pone los \n
        text = unicode(self.editor.document().toPlainText())
        if format == "xml":
            firstBlock = self.editor.document().firstBlock()
            lastBlock = self.editor.document().lastBlock()
            return self.formatAsXml(text, firstBlock, lastBlock, firstBlock.position(), lastBlock.position() + lastBlock.length())
        else:
            return text
        
    def line(self, format = None):
        return self.editor.textCursor().block().text()
        
    def character(self, format = None):
        cursor = self.editor.textCursor()
        return cursor.document().characterAt(cursor.position())
        
    def scope(self, format = None):
        return self.editor.scope()
    
    def selection(self, format = None):
        cursor = self.editor.textCursor()
        if cursor.hasSelection():
            text = cursor.selectedText().replace(u"\u2029", '\n').replace(u"\u2028", '\n')
            if format == "xml":
                firstBlock, lastBlock = self.editor.selectionBlockStartEnd()
                return self.formatAsXml(text, firstBlock, lastBlock, cursor.selectionStart() - firstBlock.position(), cursor.selectionEnd() - lastBlock.position())
            else:
                return text
        
    def selectedText(self, format = None):
        return self.selection(format)
    
    def word(self, format = None):
        word, start, end = self.editor.currentWord()
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
    
    # ----------------- Delete From Editor
    def deleteWord(self):
        _, start, end = self.editor.currentWord()
        cursor = self.editor.textCursor()
        cursor.setPosition(start)
        cursor.setPosition(end, QtGui.QTextCursor.KeepAnchor)
        cursor.removeSelectedText()
        
    def deleteSelection(self):
        cursor = self.editor.textCursor()
        cursor.removeSelectedText()

    def deleteLine(self):
        cursor = self.editor.textCursor()
        block = cursor.block()
        cursor.setPosition(block.position())
        cursor.setPosition(block.position() + block.length() - 1, QtGui.QTextCursor.KeepAnchor)
        cursor.removeSelectedText()
        
    def deleteCharacter(self):
        cursor = self.editor.textCursor()
        cursor.deleteChar()
    
    def deleteDocument(self):
        self.editor.document().clear()
       
    # ------------------- Outpus function
    def error(self, context, format = None):
        if self.errorCommand:
            raise Exception(context.errorValue)
        else:
            print context.workingDirectory
            self.editor.mainWindow.showErrorInBrowser(
                context.description(),
                context.errorValue,
                context.outputType,
                errorCommand = True
            )

    def discard(self, context, format = None):
        pass
        
    def replaceSelectedText(self, context, format = None):
        cursor = self.editor.textCursor()
        if cursor.hasSelection():
            position = cursor.selectionStart()
            cursor.insertText(context.outputValue)
            cursor.setPosition(position, position + len(context.outputValue))
        else:
            cursor.insertText(context.outputValue)
        self.editor.setTextCursor(cursor)
        
    def replaceDocument(self, context, format = None):
        self.editor.updatePlainText(context.outputValue)
        
    def replaceSelection(self, context, format = None):
        print "replaceSelection"

    def replaceInput(self, context, format = None):
        self.editor.textCursor().insertText(context.outputValue)

    def insertText(self, context, format = None):
        cursor = self.editor.textCursor()
        cursor.insertText(context.outputValue)
    
    def atCaret(self, context, format = None):
        print "atCaret"

    def afterInput(self, context, format = None):
        print "afterInput"

    def afterSelectedText(self, context, format = None):
        cursor = self.editor.textCursor()
        cursor.setPosition(cursor.selectionEnd())
        cursor.insertText(context.outputValue)
        
    def insertAsSnippet(self, context, format = None):
        snippet = self.editor.application.supportManager.buildAdHocSnippet(context.outputValue, context.bundleItem.bundle, tabTrigger = context.bundleItem.tabTrigger)
        self.editor.insertBundleItem(snippet, tabTriggered = self.tabTriggered, disableIndent = self.disableIndent)
            
    def showAsHTML(self, context, format = None):
        self.editor.browserDock.setRunningContext(context)

    def showAsTooltip(self, context, format = None):
        message = context.outputValue.strip()
        timeout = len(message) * 20
        if timeout > 2000:
            timeout = 2000

        point = self.editor.cursorRect(self.editor.textCursor()).bottomRight()
        point = self.editor.mapToGlobal(point)
        # TODO: Ver que pasa sin usar el html con los replace
        html = """
            <span>%s</span><hr>
            <div style='text-align: right; font-size: small;'><a href='copy'>Copy</a>
            </div>""" % context.outputValue.strip().replace('\n', '<br/>').replace(' ', '&nbsp;')
        callbacks = {
            'copy': lambda s = context.outputValue: QtGui.qApp.instance().clipboard().setText(s)
        }
        
        self.editor.mainWindow.showMessage(message, timeout = timeout, point = point, linkMap = callbacks)
        
    def toolTip(self, context, format = None):
        print "toolTip"

    def createNewDocument(self, context, format = None):
        editor= self.editor.mainWindow.addEmptyEditor()
        editor.setPlainText(context.outputValue)
        
    def newWindow(self, context, format = None):
        print context.outputValue, format
        print "newWindow"

    def openAsNewDocument(self, context, format = None):
        editor= self.editor.mainWindow.addEmptyEditor()
        editor.setPlainText(context.outputValue)
