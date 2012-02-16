#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
from logging import getLogger

from PyQt4 import QtGui, QtCore

class PMXPluginManager(object):
    def __init__(self, application):
        self.application = application
        self.directories = []
        
        self.editors = []
        self.dockers = []
        self.statusBars = []
        self.keyHelpers = {}
        self.overlays = {}
        self.instances = {}
    
    def addPluginDirectory(self, directory):
        self.directories.append(directory)

    #==================================================
    # Cargando clases
    #==================================================
    #TODO: llevar esto al nivel de aplicacion y llamarlo populatedComponent o algo asi
    def preparePlugin(self, pluginClass):
        pluginClass.application = self.application
        pluginClass.logger = self.application.getLogger('.'.join([pluginClass.__module__, pluginClass.__name__]))
        
    def prepareWidgetPlugin(self, widgetClass):
        self.preparePlugin(widgetClass)
        self.application.settings.registerConfigurable(widgetClass)
        for settingClass in widgetClass.contributeToSettings():
            self.preparePlugin(settingClass)
            self.application.settingsDialog.register(settingClass(widgetClass.settings))

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
        
        for overlayClass in self.overlays.get(widgetClass, []):
            overlay = overlayClass(instance)
            instance.addOverlay(overlay)
        
        self.application.settings.configure(instance)

        instances = self.instances.setdefault(widgetClass, [])
        instances.append(instance)
        return instance
    
    def createEditor(self, filePath, mainWindow):
        if filePath is not None:
            mimetype = self.application.fileManager.mimeType(filePath)
            for editorClass in self.editors:
                if editorClass.acceptFile(filePath, mimetype):
                    break
        else:
            editorClass = self.editors[0]
        editor = self.createWidgetInstance(editorClass, filePath, mainWindow)
        editor.initialize()
        return editor
    
    def createCustomActions(self, mainWindow):
        for editorClass in self.editors:
            menus = editorClass.contributeToMainMenu()
            if menus is not None:
                customEditorActions = []
                for name, settings in menus.iteritems():
                    actions = mainWindow.contributeToMainMenu(name, settings)
                    customEditorActions.extend(actions)
            mainWindow.registerEditorClassActions(editorClass, customEditorActions)
        
        for dockClass in self.dockers:
            menus = dockClass.contributeToMainMenu()
            if menus is not None:
                customDockActions = []
                for name, settings in menus.iteritems():
                    actions = mainWindow.contributeToMainMenu(name, settings)
                    customDockActions.extend(actions)
            mainWindow.registerDockClassActions(dockClass, customDockActions)
        
        for statusClass in self.statusBars:
            menus = statusClass.contributeToMainMenu()
            if menus is not None:
                customStatusActions = []
                for name, settings in menus.iteritems():
                    actions = mainWindow.contributeToMainMenu(name, settings)
                    customStatusActions.extend(actions)
            mainWindow.registerStatusClassActions(statusClass, customStatusActions)
            
    def populateMainWindow(self, mainWindow):
        self.createCustomActions(mainWindow)
            
        mainWindow.setDockOptions(QtGui.QMainWindow.AllowTabbedDocks | QtGui.QMainWindow.AllowNestedDocks | QtGui.QMainWindow.AnimatedDocks)
        
        for dockClass in self.dockers:
            dock = self.createWidgetInstance(dockClass, mainWindow)
            dock.initialize()
            mainWindow.addDock(dock, dock.PREFERED_AREA)

        for statusBarClass in self.statusBars:
            status = self.createWidgetInstance(statusBarClass, mainWindow)
            status.initialize()
            mainWindow.addStatusBar(status)
    
    def _import_module(self, name):
        __import__(name)
        return sys.modules[name]
    
    def _load_plugin(self, moduleName, directory = None):
        old_syspath = sys.path[:]
        try:
            if directory is not None:
                sys.path.insert(1, directory)
            module = self._import_module(moduleName)
            module.registerPlugin(self)
        except (ImportError, AttributeError) as reason:
            print(reason)
            raise reason
        finally:
            sys.path = old_syspath
        return None
    
    def loadPlugins(self):
        self._load_plugin('prymatex.gui.codeeditor')
        self._load_plugin('prymatex.gui.dockers')
        for directory in self.directories:
            if not os.path.isdir(directory):
                continue # 
            moduleNames = os.listdir(directory)
            for name in moduleNames:
                self._load_plugin(name, directory)