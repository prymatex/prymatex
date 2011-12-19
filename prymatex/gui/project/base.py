#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os

from prymatex.utils import plist
from prymatex import resources

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

#TODO: Utiles
def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

class PMXProject(object):
    KEYS = [    'currentDocument', 'documents', 'fileHierarchyDrawerWidth', 'metaData', 'openDocuments', 'showFileHierarchyDrawer', 'windowFrame' ]
    def __init__(self, name, directory, filePath, hash):
        self.name = name
        self.directory = directory
        self.filePath = filePath
        self.workingSet = None
        self.manager = None
        self.load(hash)
        
        self.populated = False
        self.parent = None
        self.children = []
    
    def load(self, hash):
        for key in PMXProject.KEYS:
            value = hash.get(key, None)
            setattr(self, key, value)
    
    @property
    def hash(self):
        hash = {}
        for key in PMXProject.KEYS:
            value = getattr(self, key)
            if value != None:
                hash[key] = value
        return hash

    def save(self):
        file = os.path.join(self.filePath)
        plist.writePlist(self.hash, file)

    def delete(self, hard = False):
        os.unlink(os.path.join(self.filePath))
        if hard:
            try:
                os.rmdir(self.directory)
            except os.OSError:
                pass

    def buildEnvironment(self):
        return {}

    @classmethod
    def loadProject(cls, filePath, manager):
        name = os.path.splitext(os.path.basename(filePath))[0]
        directory = os.path.dirname(filePath)
        try:
            data = plist.readPlist(filePath)
            project = cls(name, directory, filePath, data)
            manager.addProject(project)
        except Exception, e:
            print "Error in project %s (%s)" % (filePath, e)
    
    @property
    def fileWatcher(self):
        return self.manager.fileWatcher
    
    def setManager(self, manager):
        self.manager = manager
    
    def setWorkingSet(self, workingSet):
        self.workingSet = set

    #==================================================
    # Tree Node interface
    #==================================================
    def populate(self):
        self.fileWatcher.addPath(self.directory)
        for name in os.listdir(self.directory):
            node = PMXProjectItem(name, self)
            node.parent = self
            self.children.append(node)
        self.populated = True
        
    @property
    def path(self):
        return self.directory

    @property
    def icon(self):
        if self.manager.isOpen(self):
            return resources.getIcon("projectopen")
        else:
            return resources.getIcon("projectclose")

    def child(self, row, column):
        return self.children[row]
    
    def childCount(self):
        if not self.populated:
            self.populate()
        return len(self.children)
    
    def row(self):
        return self.parent.children.index(self)
    
    def findDirectoryNode(self, path):
        current = self
        for part in path.split(os.path.sep):
            nodes = filter(lambda node: node.isdir and node.name == part, current.children)
            assert len(nodes) <= 1, "More than one node"
            #TODO: Arregrlar el detalle del split con cadena vacia
            if len(nodes):
                current = nodes.pop()
        return current
    
class PMXProjectItem(object):
    def __init__(self, name, project):
        self.name = name
        self.project = project
        
        self.populated = False
        self.parent = None
        self.children = []

    @property
    def fileWatcher(self):
        return self.project.fileWatcher
    
    #==================================================
    # Tree Node interface
    #==================================================
    def populate(self):
        self.isdir = os.path.isdir(self.path)
        if self.isdir:
            self.fileWatcher.addPath(self.path)
            for name in os.listdir(self.path):
                node = PMXProjectItem(name, self)
                node.parent = self
                self.children.append(node)
        self.populated = True
        
    @property
    def path(self):
        return os.path.join(self.parent.path, self.name)
    
    @property
    def icon(self):
        return resources.getIcon(self.path)
        
    def childCount(self):
        if not self.populated:
            self.populate()
        return len(self.children)
    
    def child(self, row, column):
        return self.children[row]
    
    def row(self):
        return self.parent.children.index(self)