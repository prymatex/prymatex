#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from prymatex.support.processor import PMXCommandProcessor

#Este es un processor de commands para la Main Window
class MainWindowCommandProcessor(PMXCommandProcessor):
    def __init__(self, mainWindow):
        super(PMXCommandProcessor, self).__init__()
        self.mainWindow = mainWindow
        self.__env = {}

    def startCommand(self, command):
        self.command = command
        self.__env = command.environmentVariables()
        self.__env.update(self.mainWindow.environmentVariables())
        self.__env.update(self.baseEnvironment)
        
    def endCommand(self, command):
        self.command = None
        
    def environmentVariables(self):
        return self.__env
        
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
        browser = self.mainWindow.componentByName("browserdock")
        browser.setRunningContext(context)

    def showAsTooltip(self, context):
        message = context.outputValue.strip()
        timeout = len(message) * 20

        self.mainWindow.showMessage(context.outputValue, timeout = timeout)
        
    def createNewDocument(self, context):
        editor = self.mainWindow.addEmptyEditor()
        editor.setPlainText(context.outputValue)
        
    def openAsNewDocument(self, context):
        editor = self.mainWindow.addEmptyEditor()
        editor.setPlainText(context.outputValue)