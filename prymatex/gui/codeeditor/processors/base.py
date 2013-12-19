#!/usr/bin/env python
# -*- coding: utf-8 -*-

class CodeEditorBaseProcessor(object):
    def __init__(self, editor):
        self.editor = editor
        self.cursorWrapper = None
        self.bundleItem = None

    def type(self):
        return self.bundleItem is not None and self.bundleItem.TYPE

    def configure(self, settings):
        self.asynchronous = settings.get("asynchronous", True)
        self.cursorWrapper = settings.get("cursorWrapper", 
            self.editor.textCursor())
        self.disableIndent = settings.get("disableIndent", False)
        self.baseEnvironment = settings.get("environment", {})
        self.errorCommand = settings.get("errorCommand", False)
        self.tabKeyBehavior = settings.get("tabKeyBehavior",
            self.editor.tabKeyBehavior())
        self.indentation = settings.get("indentation", 
            self.editor.blockUserData(self.cursorWrapper.block()).indent)

    def beginExecution(self, bundleItem):
        self.bundleItem = bundleItem
        self.__env = None
        self.editor.beginProcessor.emit(self)

    def endExecution(self, bundleItem):
        self.bundleItem = None
        self.editor.endProcessor.emit(self)

    def environmentVariables(self):
        if self.__env is None:
            # TODO No es mejor que tambien el editor saque de la mainwindow para
            # preservar la composision?
            self.__env = {}
            envs = [ self.bundleItem.environmentVariables(),
                self.editor.mainWindow.environmentVariables(),
                self.editor.environmentVariables(),
                self.baseEnvironment ]
            for env in envs:
                self.__env.update(env)
        return self.__env

    def shellVariables(self):
        leftSettings, rightSettings = self.editor.settings(self.cursorWrapper)
        return rightSettings.shellVariables
