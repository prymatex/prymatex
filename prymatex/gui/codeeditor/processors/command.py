#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui
import uuid as uuidmodule
from prymatex.support.processor import PMXCommandProcessor
from prymatex.support.snippet import PMXSnippet

class PMXCommandProcessor(PMXCommandProcessor):
    def __init__(self, editor):
        super(PMXCommandProcessor, self).__init__()
        self.editor = editor
        self.settings = {}
        self.tabTriggered = False
        self.disableIndent = True

    def configure(self, settings):
        self.settings = settings
        
    def configure(self, tabTrigger, disableIndent):
        self.tabTriggered = tabTrigger
        self.disableIndent = disableIndent

    def formatAsXml(self, text, firstBlock, lastBlock, startIndex, endIndex):
        result = []
        block = firstBlock
        for line in text.splitlines():
            if block == firstBlock and block == lastBlock:
                scopes = block.userData().getAllScopes(start = startIndex, end = endIndex)
            elif block == firstBlock:
                scopes = block.userData().getAllScopes(start = startIndex)
            elif block == lastBlock:
                scopes = block.userData().getAllScopes(end = endIndex)
            else:
                scopes = block.userData().getAllScopes()
            for scope, start, end in scopes:
                ss = scope.split()
                token = "".join(map(lambda scope: "<" + scope + ">", ss))
                token += line[start:end]
                ss.reverse()
                token += "".join(map(lambda scope: "</" + scope + ">", ss))
                result.append(token)
            if block == lastBlock:
                break
            block = block.next()
        return "\n".join(result)

    #Inputs
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
        return self.environment['TM_CURRENT_LINE']
        
    def character(self, format = None):
        cursor = self.editor.textCursor()
        return cursor.document().characterAt(cursor.position())
        
    def scope(self, format = None):
        return self.environment['TM_SCOPE']
    
    def selection(self, format = None):
        if 'TM_SELECTED_TEXT' in self.environment:
            text = unicode(self.environment['TM_SELECTED_TEXT'])
            if format == "xml":
                cursor = self.editor.textCursor()
                firstBlock, lastBlock = self.editor.getSelectionBlockStartEnd()
                return self.formatAsXml(text, firstBlock, lastBlock, cursor.selectionStart() - firstBlock.position(), cursor.selectionEnd() - lastBlock.position())
            else:
                return text
        
    def selectedText(self, format = None):
        return self.selection
    
    def word(self, format = None):
        if 'TM_CURRENT_WORD' in self.environment:
            return self.environment['TM_CURRENT_WORD']
    
    @property
    def environment(self, format = None):
        return self.__env
    
    #Interface
    def startCommand(self, command):
        self.command = command
        self.__env = self.editor.buildEnvironment(command.buildEnvironment())

    #beforeRunningCommand
    def saveModifiedFiles(self):
        self.editor.mainWindow.actionSaveAll.trigger()
        return True
    
    def saveActiveFile(self):
        self.editor.mainWindow.actionSave.trigger()
        return True
    
    # deleteFromEditor
    def deleteWord(self):
        cursor = self.editor.textCursor()
        cursor.select(QtGui.QTextCursor.WordUnderCursor)
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
        print "borrar documento"
        self.editor.document().clear()
        
    # Outpus function
    def commandError(self, text, code):
        from prymatex.support.utils import makeHyperlinks
        html = '''
            <html>
                <head>
                    <title>Error</title>
                    <style>
                        body {
                            background: #999;
                            
                        }
                        pre {
                            border: 1px dashed #222;
                            background: #ccc;
                            text: #000;
                            padding: 2%%;
                        }
                    </style>
                </head>
                <body>
                <h3>An error has occurred while executing command "%(name)s"</h3>
                <pre>%(output)s</pre>
                <p>Exit code was: %(exit_code)d</p>
                </body>
            </html>
        ''' % {'output': makeHyperlinks(text), 
               'name': self.command.name,
               'exit_code': code}
        self.showAsHTML(html)
        
    def discard(self, text):
        pass
        
    def replaceSelectedText(self, text):
        cursor = self.editor.textCursor()
        if cursor.hasSelection():
            position = cursor.selectionStart()
            cursor.insertText(text)
            cursor.setPosition(position, position + len(text))
        else:
            cursor.insertText(text)
        self.editor.setTextCursor(cursor)
        
    def replaceDocument(self, text):
        self.editor.document().setPlainText(text)
        
    def insertText(self, text):
        cursor = self.editor.textCursor()
        cursor.insertText(text)
        
    def afterSelectedText(self, text):
        cursor = self.editor.textCursor()
        position = cursor.selectionEnd()
        cursor.setPosition(position)
        cursor.insertText(text)
        
    def insertAsSnippet(self, text):
        hash = {    'content': text, 
                       'name': self.command.name,
                 'tabTrigger': self.command.tabTrigger,
              'keyEquivalent': self.command.keyEquivalent }
        snippet = PMXSnippet(self.command.manager.uuidgen(), "internal", hash = hash)
        snippet.bundle = self.command.bundle
        self.editor.insertBundleItem(snippet, tabTriggered = self.tabTriggered, disableIndent = self.disableIndent)
            
    def showAsHTML(self, text):
        self.editor.mainWindow.paneBrowser.setHtml(text, self.command)
        self.editor.mainWindow.paneBrowser.show()
        
    def showAsTooltip(self, text):
        cursor = self.editor.textCursor()
        point = self.editor.viewport().mapToGlobal(self.editor.cursorRect(cursor).bottomRight())
        QtGui.QToolTip.showText(point, text.strip(), self.editor, self.editor.rect())
        
    def createNewDocument(self, text):
        print "Nuevo documento", text
        
    def openAsNewDocument(self, text):
        editor_widget = self.editor.mainWindow.currentTabWidget.appendEmptyTab()
        editor_widget.codeEdit.setPlainText(text)