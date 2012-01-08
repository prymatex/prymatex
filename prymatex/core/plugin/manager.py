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
        self.keyHelpers = {}
        self.overlays = {}
        self.instances = {}
        
    def preparePlugin(self, pluginClass):
        pluginClass.application = self.application
        pluginClass.logger = getLogger('.'.join([pluginClass.__module__, pluginClass.__name__]))
        
    def prepareWidgetPlugin(self, widgetClass):
        self.preparePlugin(widgetClass)
        self.application.settings.registerConfigurable(widgetClass)
        
    def registerEditor(self, editorClass):
        self.prepareWidgetPlugin(editorClass)
        self.editors.append(editorClass)
 
    def registerDocker(self, dockerClass):
        self.prepareWidgetPlugin(dockerClass)
        self.dockers.append(dockerClass)
        
    def registerStatusBar(self, statusBarClass):
        self.prepareWidgetPlugin(statusBarClass)
        self.statusBars.append(statusBarClass)
    
    def registerKeyHelper(self, editorClass, helperClass):
        self.preparePlugin(helperClass)
        editorClass.addKeyHelper(helperClass())
        
    def registerOverlay(self, widgetClass, overlayClass):
        self.preparePlugin(overlayClass)
        overlayClasses = self.overlays.setdefault(widgetClass, [])
        overlayClasses.append(overlayClass)
        
    def createWidgetInstance(self, widgetClass, *largs, **kwargs):
        instance = widgetClass(*largs, **kwargs)
        instance.initialize()
        
        for overlayClass in self.overlays.get(widgetClass, []):
            overlay = overlayClass(instance)
            overlay.initialize()
            instance.addOverlay(overlay)
        
        self.application.settings.configure(instance)

        instances = self.instances.setdefault(widgetClass, [])
        instances.append(instance)
        return instance
    
    def createEditor(self, filePath, project, mainWindow):
        editorClass = self.editors[0]
        return self.createWidgetInstance(editorClass, filePath, project, mainWindow)
    
    def populateMainWindow(self, mainWindow):
        mainWindow.setDockOptions(QtGui.QMainWindow.AllowTabbedDocks | QtGui.QMainWindow.AllowNestedDocks | QtGui.QMainWindow.AnimatedDocks)
        
        for dockClass in self.dockers:
            dock = self.createWidgetInstance(dockClass, mainWindow)
            mainWindow.addDock(dock, dock.PREFERED_AREA)
            
        for statusBarClass in self.statusBars:
            status = self.createWidgetInstance(statusBarClass, mainWindow)
            mainWindow.addStatusBar(status)
        
    def load(self):
        from prymatex.gui.codeeditor import setup
        setup(self)
        from prymatex.gui.dockers import setup
        setup(self)