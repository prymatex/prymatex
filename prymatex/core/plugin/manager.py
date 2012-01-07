#!/usr/bin/env python
# -*- coding: utf-8 -*-

class PMXPluginManager(object):
    def __init__(self, application):
        self.application = application
        self.editors = []
        self.dockers = []
        self.instances = {}
        
    def registerEditor(self, editorClass):
        settingsGroup =  editorClass.pop('SETTINGS_GROUP', editorClass.__name__)
        editorClass.settings = self.application.settings.getGroup(settingsGroup)
        self.editors.append(editorClass)
 
    def registerDocker(self, dockClass, preferedArea = None):
        self.dockers.append(dockClass)
        
    def createEditor(self, filePath, project):
        editorClass = self.editors[0]
        editor = editorClass.newInstance(filePath, project)
        
        editorClass.settings.addListener(editor)
        editorClass.settings.configure(editor)
        
        self.instances.setdefault(editorClass, [])
        self.instances[editorClass].append(editor)
        return editor
    
    def load(self):
        from prymatex.gui.codeeditor import setup
        setup(self)
        from prymatex.gui.dockers import setup
        setup(self)