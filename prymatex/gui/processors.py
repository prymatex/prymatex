#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from prymatex.gui import utils
from prymatex.support.processor import PMXCommandProcessor

#Este es un processor de commands para la Main Window
class MainWindowCommandProcessor(PMXCommandProcessor):
    def __init__(self, mainWindow):
        super(PMXCommandProcessor, self).__init__()
        self.mainWindow = mainWindow

    def environment(self, command):
        environment = command.buildEnvironment()
        environment.update(self.mainWindow.buildEnvironment())
        environment.update(self.baseEnvironment)
        return environment

    def configure(self, settings):
        self.asynchronous = settings.get("asynchronous", True)
        self.baseEnvironment = settings.get("environment", {})
        self.errorCommand = settings.get("errorCommand", False)

    #beforeRunningCommand
    def saveModifiedFiles(self):
        ret = True
        for editor in self.mainWindow.editors():
            if editor.isModified():
                self.mainWindow.saveEditor(editor = editor)
                ret = ret and not editor.isModified()
            if ret == False:
                break
        return ret
    
    def saveActiveFile(self):
        editor = self.mainWindow.currentEditor()
        if editor is not None:
            self.mainWindow.saveEditor(editor = editor)
            return not (editor.isModified() or editor.isNew())
        return True
    
    # Outpus function
    def error(self, context):
        if self.errorCommand:
            raise Exception(context.errorValue)
        else:
            self.mainWindow.showErrorInBrowser(
                context.description(),
                context.errorValue,
                context.outputType,
                errorCommand = True
            )
        
    def showAsHTML(self, context):
        self.mainWindow.browser.setRunningContext(context)

    def showAsTooltip(self, context):
        # TODO Otra forma de mostrar como tooltip si no hay editor
        linesToRead = context.outputValue.count('\n') or context.outputValue.count('<br')
        if linesToRead > 10:
            timeout = 8000
        else:
            timeout = linesToRead * 700
            
        self.mainWindow.currentEditor().showMessage(html, timeout = timeout)
        
    def createNewDocument(self, context):
        editor = self.mainWindow.addEmptyEditor()
        editor.setPlainText(context.outputValue)
        
    def openAsNewDocument(self, context):
        editor = self.mainWindow.addEmptyEditor()
        editor.setPlainText(context.outputValue)