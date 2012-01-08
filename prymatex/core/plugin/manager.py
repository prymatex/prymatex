#!/usr/bin/env python
# -*- coding: utf-8 -*-
from logging import getLogger

from PyQt4 import QtGui, QtCore

class PMXPluginManager(object):
    def __init__(self, application):
        self.application = application
        self.editors = []
        self.dockers = []
        self.statusBars = []
        self.instances = {}
        
    def registerEditor(self, editorClass):
        self.application.settings.registerConfigurable(editorClass)
        editorClass.application = self.application
        editorClass.logger = getLogger('.'.join([editorClass.__module__, editorClass.__name__]))
        self.editors.append(editorClass)
 
    def registerDocker(self, dockerClass):
        self.application.settings.registerConfigurable(dockerClass)
        dockerClass.application = self.application
        dockerClass.logger = getLogger('.'.join([dockerClass.__module__, dockerClass.__name__]))
        self.dockers.append(dockerClass)
        
    def registerStatusBar(self, statusBarClass):
        self.application.settings.registerConfigurable(statusBarClass)
        statusBarClass.application = self.application
        statusBarClass.logger = getLogger('.'.join([statusBarClass.__module__, statusBarClass.__name__]))
        self.statusBars.append(statusBarClass)
    
    def registerKeyHelper(self, widgetClass, helperClass):
        helperClass.application = self.application
        helperClass.logger = getLogger('.'.join([helperClass.__module__, helperClass.__name__]))
        widgetClass.addKeyHelper(helperClass())
        
    def createEditor(self, filePath, project, mainWindow):
        editorClass = self.editors[0]
        editor = editorClass(filePath, project, mainWindow)
        editor.initialize(mainWindow)
        
        self.application.settings.configure(editor)
        
        instances = self.instances.setdefault(editorClass, [])
        instances.append(editor)
        return editor
    
    def populateMainWindow(self, mainWindow):
        mainWindow.setDockOptions(QtGui.QMainWindow.AllowTabbedDocks | QtGui.QMainWindow.AllowNestedDocks | QtGui.QMainWindow.AnimatedDocks)
        
        for dockClass in self.dockers:
            dock = dockClass(mainWindow)
            dock.initialize(mainWindow)
            self.application.settings.configure(dock)
            instances = self.instances.setdefault(dockClass, [])
            instances.append(dock)
            mainWindow.addDock(dock, dock.PREFERED_AREA)
            
        for statusBarClass in self.statusBars:
            status = statusBarClass(mainWindow)
            status.initialize(mainWindow)
            self.application.settings.configure(status)
            instances = self.instances.setdefault(statusBarClass, [])
            instances.append(dock)
            mainWindow.addStatusBar(status)
        
    def load(self):
        from prymatex.gui.codeeditor import setup
        setup(self)
        from prymatex.gui.dockers import setup
        setup(self)