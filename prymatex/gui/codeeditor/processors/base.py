#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore

class CodeEditorBaseProcessor(QtCore.QObject):
    begin = QtCore.Signal()
    end = QtCore.Signal()

    def __init__(self, editor):
        QtCore.QObject.__init__(self, editor)
        self.editor = editor
        self.textCursor = None
        self.bundleItem = None

    def currentType(self):
        return self.bundleItem is not None and self.bundleItem.type() or ""

    def configure(self, **kwargs):
        self.textCursor = kwargs.get("textCursor", 
            self.editor.textCursor())
        self.baseEnvironment = kwargs.get("environment", {})

    def beginExecution(self, bundleItem):
        self.bundleItem = bundleItem
        self.__env = None
        self.begin.emit()

    def endExecution(self, bundleItem):
        self.end.emit()
        self.bundleItem = None

    def environmentVariables(self):
        if self.__env is None:
            # TODO No es mejor que tambien el editor saque de la mainwindow para
            # preservar la composision?
            self.__env = {}
            envs = [ self.bundleItem.environmentVariables(),
                self.editor.mainWindow().environmentVariables(),
                self.editor.environmentVariables(),
                self.baseEnvironment ]
            for env in envs:
                self.__env.update(env)
        return self.__env

    def shellVariables(self):
        settings = self.editor.settings(self.textCursor)
        return settings.shellVariables + list(self.bundleItem.variables().items())
