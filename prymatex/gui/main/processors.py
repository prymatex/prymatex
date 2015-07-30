#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore
from prymatex.utils import html

from prymatex.support.processor import CommandProcessorMixin

#Este es un processor de commands para la Main Window
class PrymatexMainCommandProcessor(CommandProcessorMixin, QtCore.QObject):
    def window(self):
        return self.parent()

    def beginExecution(self, command):
        self.command = command
        self.__env = None
        
    def endExecution(self, command):
        self.command = None
        
    def environmentVariables(self):
        if self.__env is None:
            self.__env = {}
            envs = [ self.window().environmentVariables(), 
                self.command.environmentVariables(),
                self.baseEnvironment ]
            for env in envs:
                self.__env.update(env)
        return self.__env
        
    def shellVariables(self, environment):
        settings = self.window().application().supportManager.getPreferenceSettings()
        properties = self.window().application().supportManager.getPropertiesSettings()
        return settings.shellVariables(environment) + properties.shellVariables(environment)

    def configure(self, settings):
        self.asynchronous = settings.get("asynchronous", True)
        self.baseEnvironment = settings.get("environment", {})
        self.errorCommand = settings.get("errorCommand", False)

    # ------------ Before Running Command
    def saveModifiedFiles(self):
        ret = True
        for editor in self.window().editors():
            if editor.isModified():
                self.window().saveEditor(editor = editor)
                ret = ret and not editor.isModified()
            if ret == False:
                break
        return ret
    
    def saveActiveFile(self):
        editor = self.window().currentEditor()
        if editor is not None:
            self.window().saveEditor(editor = editor)
            return not (editor.isModified() or editor.isNew())
        return True
    
    # --------------- Outpus function
    def error(self, context, outputFormat = None):
        if self.errorCommand:
            raise Exception(context.errorValue)
        else:
            def show_error(window, desc, value, _type):
                def _show_error():
                    window.showErrorInBrowser(desc, value, _type,
                        errorCommand=True)
                return _show_error
            QtCore.QTimer.singleShot(0, show_error(
                self.window(),
                context.description(),
                context.errorValue,
                context.outputType           
            ))

    def showAsHTML(self, context, outputFormat = None):
        self.window().browserDock.setRunningContext(context)

    def showAsTooltip(self, context, outputFormat = None):
        message = html.escape(context.outputValue.strip())
        timeout = len(message) * 20
        if timeout > 2000:
            timeout = 2000

        self.window().showTooltip(message, timeout = timeout)
    
    def toolTip(self, context, outputFormat = None):
        print("toolTip")

    def createNewDocument(self, context, outputFormat = None):
        editor = self.window().addEmptyEditor()
        editor.setPlainText(context.outputValue)
        
    def newWindow(self, context, outputFormat = None):
        if outputFormat == "html":
            self.window().browserDock.newRunningContext(context)
        elif outputFormat == "text":
            # TODO: Quiza una mejor forma de crear documentos con texto
            editor = self.window().addEmptyEditor()
            editor.setPlainText(context.outputValue)

    def openAsNewDocument(self, context, outputFormat = None):
        editor = self.window().addEmptyEditor()
        editor.setPlainText(context.outputValue)
