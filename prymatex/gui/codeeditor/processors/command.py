#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from subprocess import Popen, PIPE
from prymatex.support.processor import PMXCommandProcessor
from prymatex.support.snippet import PMXSnippet
from prymatex.support.command import PMXCommand

class PMXCommandProcessor(PMXCommandProcessor):
    def __init__(self, editor):
        super(PMXCommandProcessor, self).__init__()
        self.editor = editor

    def environment(self, command):
        environment = self.editor.buildEnvironment(command.buildEnvironment())
        environment.update(self.baseEnvironment)
        return environment

    def configure(self, settings):
        self.asynchronous = settings.get("asynchronous", True)
        self.tabTriggered = settings.get("tabTriggered", False)
        self.disableIndent = settings.get("disableIndent", False)
        self.baseEnvironment = settings.get("environment", {})

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
        return self.editor.textCursor().block().text()
        
    def character(self, format = None):
        cursor = self.editor.textCursor()
        return cursor.document().characterAt(cursor.position())
        
    def scope(self, format = None):
        return self.editor.getCurrentScope()
    
    def selection(self, format = None):
        if self.editor.textCursor().hasSelection():
            text = self.editor.textCursor().selectedText()
            if format == "xml":
                cursor = self.editor.textCursor()
                firstBlock, lastBlock = self.editor.getSelectionBlockStartEnd()
                return self.formatAsXml(text, firstBlock, lastBlock, cursor.selectionStart() - firstBlock.position(), cursor.selectionEnd() - lastBlock.position())
            else:
                return text
        
    def selectedText(self, format = None):
        return self.selection
    
    def word(self, format = None):
        word, start, end = self.editor.getCurrentWord()
        return word
    
    def runCommand(self, context, shellCommand, callback):
        if self.asynchronous:
            return self.runQProcessCommand(context, shellCommand, callback)
        else:
            return self.runPopenCommand(context, shellCommand, callback)
    
    def runPopenCommand(self, context, shellCommand, callback):
        process = Popen(shellCommand, stdin=PIPE, stdout=PIPE, stderr=PIPE, env = context.environment)
        
        if context.inputType != None:
            process.stdin.write(unicode(context.inputValue).encode("utf-8"))
        process.stdin.close()
        try:
            context.outputValue = process.stdout.read()
            context.errorValue = process.stderr.read()
        except IOError, e:
            context.errorValue = str(e).decode("utf-8")
        process.stdout.close()
        process.stderr.close()
        context.outputType = process.wait()
        callback(self, context)
    
    #Interface
    def runQProcessCommand(self, context, shellCommand, callback):
        process = QtCore.QProcess(self.editor)
        #TODO: context.environment ya tiene las variables de system ver que hacer
        env = QtCore.QProcessEnvironment.systemEnvironment()
        for key, value in context.environment.iteritems():
            env.insert(key, value)
        process.setProcessEnvironment(env)

        def onQProcessFinished(process, context, callback):
            def runCallback(exitCode):
                context.errorValue = str(process.readAllStandardError()).decode("utf-8")
                context.outputValue = str(process.readAllStandardOutput()).decode("utf-8")
                context.outputType = exitCode
                callback(self, context)
            return runCallback

        process.finished[int].connect(onQProcessFinished(process, context, callback))

        if context.inputType != None:
            process.start(shellCommand, QtCore.QIODevice.ReadWrite)
            if not process.waitForStarted():
                raise Exception("No puedo correr")
            process.write(unicode(context.inputValue).encode("utf-8"))
            process.closeWriteChannel()
        else:
            process.start(shellCommand, QtCore.QIODevice.ReadOnly)

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
    def error(self, context):
        from prymatex.support.utils import makeHyperlinks
        command = '''
            source "$TM_SUPPORT_PATH/lib/webpreview.sh" 
            
            html_header "An error has occurred while executing command %(name)s"
            echo -e "<pre>%(output)s</pre>"
            echo -e "<p>Exit code was: %(exitcode)d</p>"
            html_footer
        ''' % {'output': context.errorValue, 
               'name': context.command.name,
               'exitcode': context.outputType}
        hash = {    'command': command, 
                       'name': "Error" + context.command.name,
                      'input': 'none',
                     'output': 'showAsHTML' }
        command = PMXCommand(self.editor.application.supportManager.uuidgen(), "internal", hash = hash)
        command.bundle = context.command.bundle
        self.editor.insertBundleItem(command)
        #FIXME: Esto no hace falta porque el que muestra el error por html es el insertBundleItem
        self.showAsHTML(context)
        
    def discard(self, context):
        pass
        
    def replaceSelectedText(self, context):
        cursor = self.editor.textCursor()
        if cursor.hasSelection():
            position = cursor.selectionStart()
            cursor.insertText(context.outputValue)
            cursor.setPosition(position, position + len(context.outputValue))
        else:
            cursor.insertText(context.outputValue)
        self.editor.setTextCursor(cursor)
        
    def replaceDocument(self, context):
        self.editor.document().setPlainText(context.outputValue)
        
    def insertText(self, context):
        cursor = self.editor.textCursor()
        cursor.insertText(context.outputValue)
        
    def afterSelectedText(self, context):
        cursor = self.editor.textCursor()
        position = cursor.selectionEnd()
        cursor.setPosition(position)
        cursor.insertText(context.outputValue)
        
    def insertAsSnippet(self, context):
        hash = {    'content': context.outputValue, 
                       'name': context.command.name,
                 'tabTrigger': context.command.tabTrigger,
              'keyEquivalent': context.command.keyEquivalent }
        snippet = PMXSnippet(self.editor.application.supportManager.uuidgen(), "internal", hash = hash)
        snippet.bundle = context.command.bundle
        self.editor.insertBundleItem(snippet, tabTriggered = self.tabTriggered, disableIndent = self.disableIndent)
            
    def showAsHTML(self, context):
        self.editor.mainWindow.browser.setHtml(context.outputValue, context.command)
        self.editor.mainWindow.browser.show()

    timespanFactor = 1        
    def showAsTooltip(self, context):
        # Chicho's sense of statistics
        linesToRead = context.outputValue.count('\n') or context.outputValue.count('<br')
        if linesToRead > 10:
            timeout = 8000
        else:
            timeout = linesToRead * 700
            
        #TODO: Una mejor forma de mostrar en html la salida 
        cursor = self.editor.textCursor()
        point = self.editor.cursorRect(cursor).bottomRight()
        html = """
            <span>%s</span><hr>
            <div style='text-align: right; font-size: small;'><a href='copy'>Copy</a>
            </div>""" % context.outputValue.strip().replace('\n', '<br/>').replace(' ', '&nbsp;')
        timeout = timeout * self.timespanFactor
        callbacks = {
                   'copy': lambda s = context.outputValue: QtGui.qApp.instance().clipboard().setText(s)
        }
        pos = (point.x() + 30, point.y() + 5)
        timeout = timeout * self.timespanFactor
        
        self.editor.showMessage(html, timeout = timeout, pos = pos, hrefCallbacks = callbacks)
        
    def createNewDocument(self, context):
        print "Nuevo documento", context.outputValue
        
    def openAsNewDocument(self, context):
        editor_widget = self.editor.mainWindow.currentTabWidget.appendEmptyTab()
        editor_widget.codeEdit.setPlainText(context.outputValue)