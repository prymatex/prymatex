#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex.support.processor import CommandProcessorMixin

#Este es un processor de commands para la Main Window
class PrymatexMainCommandProcessor(CommandProcessorMixin):
    def __init__(self, main_window):
        super(PrymatexMainCommandProcessor, self).__init__()
        self._main_window = main_window

    def mainWindow(self):
        return self._main_window

    def beginExecution(self, command):
        self.command = command
        self.__env = None
        
    def endExecution(self, command):
        self.command = None
        
    def environmentVariables(self):
        if self.__env is None:
            self.__env = {}
            envs = [ self.command.environmentVariables(),
                self.mainWindow().environmentVariables(),
                self.baseEnvironment ]
            for env in envs:
                self.__env.update(env)
        return self.__env
        
    def shellVariables(self):
        settings = self.mainWindow().application.supportManager.getPreferenceSettings()
        return settings.shellVariables

    def configure(self, settings):
        self.asynchronous = settings.get("asynchronous", True)
        self.baseEnvironment = settings.get("environment", {})
        self.errorCommand = settings.get("errorCommand", False)

    # ------------ Before Running Command
    def saveModifiedFiles(self):
        ret = True
        for editor in self.mainWindow().editors():
            if editor.isModified():
                self.mainWindow().saveEditor(editor = editor)
                ret = ret and not editor.isModified()
            if ret == False:
                break
        return ret
    
    def saveActiveFile(self):
        editor = self.mainWindow().currentEditor()
        if editor is not None:
            self.mainWindow().saveEditor(editor = editor)
            return not (editor.isModified() or editor.isNew())
        return True
    
    # --------------- Outpus function
    def error(self, context, outputFormat = None):
        if self.errorCommand:
            raise Exception(context.errorValue)
        else:
            print(context.workingDirectory)
            self.mainWindow().showErrorInBrowser(
                context.description(),
                context.errorValue,
                context.outputType,
                errorCommand = True
            )

    def showAsHTML(self, context, outputFormat = None):
        self.mainWindow().browserDock.setRunningContext(context)

    def showAsTooltip(self, context, outputFormat = None):
        message = context.outputValue.strip()
        timeout = len(message) * 20

        self.mainWindow().showTooltip(message, timeout = timeout)
    
    def toolTip(self, context, outputFormat = None):
        print("toolTip")

    def createNewDocument(self, context, outputFormat = None):
        editor = self.mainWindow().addEmptyEditor()
        editor.setPlainText(context.outputValue)
        
    def newWindow(self, context, outputFormat = None):
        if outputFormat == "html":
            self.mainWindow().browserDock.newRunningContext(context)
        elif outputFormat == "text":
            # TODO: Quiza una mejor forma de crear documentos con texto
            editor = self.mainWindow().addEmptyEditor()
            editor.setPlainText(context.outputValue)

    def openAsNewDocument(self, context, outputFormat = None):
        editor = self.mainWindow().addEmptyEditor()
        editor.setPlainText(context.outputValue)
