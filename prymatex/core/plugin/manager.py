#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore

class PMXPluginManager(object):
    def __init__(self, application):
        self.application = application
        self.editors = []
        self.dockers = []
        self.instances = {}
        
    def registerEditor(self, editorClass):
        self.application.settings.registerConfigurable(editorClass)
        self.editors.append(editorClass)
 
    def registerDocker(self, dockClass, preferedArea = QtCore.Qt.RightDockWidgetArea):
        self.application.settings.registerConfigurable(dockClass)
        self.dockers.append((dockClass, preferedArea))
        
    def createEditor(self, filePath, project, parent = None):
        editorClass = self.editors[0]
        editor = editorClass.newInstance(filePath, project, parent)
        
        self.application.settings.configure(editor)
        
        instances = self.instances.setdefault(editorClass, [])
        instances.append(editor)
        return editor
    
    def createDockers(self, mainWindow):
        for dockClass, preferedArea in self.dockers:
            dock = dockClass(mainWindow)
            self.application.settings.configure(dock)
            instances = self.instances.setdefault(dockClass, [])
            instances.append(dock)
            mainWindow.addDock(dock, preferedArea)
            
    def load(self):
        from prymatex.gui.codeeditor import setup
        setup(self)
        from prymatex.gui.dockers import setup
        setup(self)