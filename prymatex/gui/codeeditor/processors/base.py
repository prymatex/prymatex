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

    def isReady(self):
        return self.bundleItem is not None

    def currentType(self):
        return self.isReady() and self.bundleItem.type() or ""

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
            self.__env = {}
            for env in (
                self.editor.environmentVariables(),             # From Prymatex 
                self.bundleItem.environmentVariables(),         # From Bundle    
                self.baseEnvironment):                          # Custom
                self.__env.update(env)
        return self.__env

    def shellVariables(self):
        settings = self.editor.preferenceSettings(self.textCursor)
        properties = self.editor.propertiesSettings(self.textCursor)
        print(settings.shellVariables)
        print(properties.shellVariables)
        return settings.shellVariables + \
            properties.shellVariables + \
            list(self.bundleItem.variables().items())
