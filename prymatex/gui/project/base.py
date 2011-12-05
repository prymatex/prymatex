#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtCore, QtGui

"""
currentDocument: Documento actual en el editor
documents: lista de documentos o carpetas, no se muy bien, creo que son los grupos de tm
    {'expanded': True,
     'name': 'source',
     'regexFolderFilter': '!.*/(\\.[^/]*|CVS|_darcs|_MTN|\\{arch\\}|blib|.*~\\.nib|.*\\.(framework|app|pbproj|pbxproj|xcode(proj)?|bundle))$',
     'selected': True,
     'sourceDirectory': ''}
fileHierarchyDrawerWidth: en ancho de la docker de proyectos
metaData: Datos de los editores por cada documento abierto, es un diccionario indexado por la ruta del documento
    {'Classes/MDSettings.h': {'caret': {'column': 20, 'line': 52},
                                       'columnSelection': False,
                                       'firstVisibleColumn': 0,
                                       'firstVisibleLine': 4,
                                       'selectFrom': {'column': 15,
                                                      'line': 52},
                                       'selectTo': {'column': 33,
                                                    'line': 52}},
openDocuments: Documentos abiertos en el editor es una lista, cada entrada de aca tiene una en metaData
showFileHierarchyDrawer: Mostrar la docker
windowFrame: El Tampaño del a ventana de projecto en tm
"""
class PMXProject(object):
    KEYS = [    'currentDocument', 'documents', 'fileHierarchyDrawerWidth', 'metaData', 'openDocuments', 'showFileHierarchyDrawer', 'windowFrame' ]
    def __init__(self, name, path, hash):
        self._name = name
        self.rootPath = path
        self.workspace = None
        self.load(hash)
        self.children = []
    
    def load(self, hash):
        for key in PMXBundle.KEYS:
            value = hash.get(key, None)
            setattr(self, key, value)
    
    @property
    def fileSystem(self):
        return self.workspace.fileSystem
    
    def setWorkspace(self, workspace):
        self.workspace = workspace
        self.rootIndex = workspace.fileSystem.index(self.rootPath)

    #==================================================
    # Tree Node interface
    #==================================================
    def icon(self):
        return None
        
    def name(self):
        return self._name
    
    def child(self, row, column):
        child = self.rootIndex.child(row, column)
        path = self.fileSystem.filePath(child)
        item = PMXProjectItem(path, self)
        item.setParent(self)
        self.children.append(item)
        return item
    
    def row(self):
        return self.parent().projects.index(self)
    
    def parent(self):
        return self.workspace
    
    def childCount(self):
        return self.fileSystem.rowCount(self.rootIndex)

class PMXProjectItem(object):
    def __init__(self, path, project):
        self.path = path
        self.project = project
        self._parent = None
        self.children = []

    @property
    def fileSystem(self):
        return self.project.fileSystem
        
    def setParent(self, parent):
        self._parent = parent

    #==================================================
    # Tree Node interface
    #==================================================
    def icon(self):
        index = self.fileSystem.index(self.path)
        return self.fileSystem.fileIcon(index)
        
    def name(self):
        index = self.fileSystem.index(self.path)
        return self.fileSystem.fileName(index)
    
    def childCount(self):
        index = self.fileSystem.index(self.path)
        return self.fileSystem.rowCount(index)
    
    def child(self, row, column):
        index = self.fileSystem.index(self.path)
        child = index.child(row, column)
        path = self.fileSystem.filePath(child)
        item = PMXProjectItem(path, self.project)
        item.setParent(self)
        self.children.append(item)
        return item
    
    def row(self):
        return self.parent().children.index(self)
    
    def parent(self):
        return self._parent