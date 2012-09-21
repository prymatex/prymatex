#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os, shutil

from prymatex import resources
from prymatex.core import exceptions
from prymatex.models.tree import TreeNode
from prymatex.utils import plist
from prymatex.core.exceptions import ProjectExistsException, FileException
from prymatex.utils.pyqtdebug import ipdb_set_trace

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

class FileSystemTreeNode(TreeNode):
    def __init__(self, name, parent = None):
        TreeNode.__init__(self, name, parent)
        self.isdir = os.path.isdir(self.path)
        self.isfile = os.path.isfile(self.path)
        self.ishidden = name.startswith('.')
        self.isproject = isinstance(self, PMXProject)

    @property
    def project(self):
        if not hasattr(self, "_project"):
            self._project = self
            while not isinstance(self._project, PMXProject):
                self._project = self._project.parentNode
        return self._project    

    @property
    def path(self):
        return os.path.join(self.parentNode.path, self.nodeName)
    
    @property
    def icon(self):
        return resources.getIcon(self.path)
    
class PMXProject(FileSystemTreeNode):
    KEYS = [    'name', 'description', 'currentDocument', 'documents', 'fileHierarchyDrawerWidth', 'metaData', 
                'openDocuments', 'showFileHierarchyDrawer', 'windowFrame', 'shellVariables', 'bundleMenu' ]
    FILE = 'info.plist'
    FOLDER = '.pmxproject'
    SUPPORT = 'Support'
    BUNDLES = 'Bundles'
    THEMES = 'Themes'
    BASH_INIT = os.path.join(SUPPORT, 'lib', 'bash_init.sh')
    
    def __init__(self, directory, hash):
        self.directory = directory
        self.projectPath = os.path.join(self.path, self.FOLDER)
        FileSystemTreeNode.__init__(self, hash.get("name"))
        self.workingSet = None
        self.manager = None
        self.support = None
        self.bundles = None
        self.themes = None
        self.namespace = None
        self.load(hash)
    
    def hasSupport(self):
        return self.support is not None
    
    def hasBundles(self):
        return self.bundles is not None

    def hasThemes(self):
        return self.themes is not None

    def setThemes(self, themes):
        self.themes = themes

    def setBundles(self, bundles):
        self.bundles = bundles
        
    def setSupport(self, support):
        self.support = support

    @property
    def environment(self):
        env = {
            'TM_PROJECT_DIRECTORY': self.directory,
            'TM_PROJECT_NAME': self.nodeName,
            'TM_PROJECT_PATH': self.projectPath }
        if self.namespace is not None:
            env['TM_PROJECT_NAMESPACE'] = self.namespace
        if self.support is not None:
            env['TM_PROJECT_SUPPORT'] = self.support
        if self.bundles is not None:
            env['TM_PROJECT_BUNDLES'] = self.bundles
        if self.themes is not None:
            env['TM_PROJECT_THEMES'] = self.themes
        return env

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
        
    def update(self, hash):
        for key in hash.keys():
            setattr(self, key, hash[key])

    def save(self):
        path = self.projectPath
        
        if not os.path.exists(path):
            os.makedirs(path)
        filePath = os.path.join(self.projectPath, self.FILE)
        plist.writePlist(self.hash, filePath)

    def delete(self, removeFiles = False):
        shutil.rmtree(self.projectPath)
        if removeFiles:
            try:
                shutil.rmtree(self.directory)
            except OSError:
                pass
    
    def buildEnvironment(self):
        env = self.manager.buildEnvironment()
        if isinstance(self.shellVariables, list):
            for var in self.shellVariables:
                if var['enabled']:
                    env[var['variable']] = var['value']
        env.update(self.environment)
        return env

    @classmethod
    def loadProject(cls, path, manager):
        projectPath = os.path.join(path, cls.FOLDER)
        fileInfo = os.path.join(projectPath, cls.FILE)
        if not os.path.isfile(fileInfo):
            raise exceptions.FileNotExistsException(fileInfo)
        try:
            data = plist.readPlist(fileInfo)
            project = cls(path, data)
            if os.path.exists(os.path.join(projectPath, cls.SUPPORT)):
                project.ensureSupport()
            if os.path.exists(os.path.join(projectPath, cls.BUNDLES)):
                project.ensureBundles()
            if os.path.exists(os.path.join(projectPath, cls.THEMES)):
                project.ensureThemes()
            manager.addProject(project)
            return project
        except Exception, e:
            print "Error in project %s (%s)" % (filePath, e)
    
    def setManager(self, manager):
        self.manager = manager
    
    def setWorkingSet(self, workingSet):
        self.workingSet = set

    @property
    def path(self):
        return self.directory
    
    @property
    def icon(self):
        if self.manager.isOpen(self):
            return resources.getIcon("project-development")

    #==========================================
    # Bundle Menu 
    #==========================================
    def addBundleMenu(self, bundle):
        if not isinstance(self.bundleMenu, list):
            self.bundleMenu = []
        self.bundleMenu.append(bundle.uuidAsUnicode())
        
    def removeBundleMenu(self, bundle):
        uuid = bundle.uuidAsUnicode()
        if uuid in self.bundleMenu:
            self.bundleMenu.remove(uuid)
        if not self.bundleMenu:
            self.bundleMenu = None
            
    def hasBundleMenu(self, bundle):
        if self.bundleMenu is None: return False
        return bundle.uuidAsUnicode() in self.bundleMenu

    def bashInit(self):
        bashInitPath = os.path.join(self.projectPath, self.BASH_INIT)
        if not os.path.exists(bashInitPath):
            self.ensureSupport()
            open(bashInitPath, 'w').close()
        return bashInitPath
    
    def ensureSupport(self):
        supportPath = os.path.join(self.projectPath, self.SUPPORT)
        if not os.path.exists(supportPath):
            os.makedirs(supportPath)
        self.setSupport(supportPath)
        for subNames in ['lib', 'bin']:
            subPath = os.path.join(supportPath, subNames)
            if not os.path.exists(subPath):
                os.makedirs(subPath)

    def ensureBundles(self):
        bundlesPath = os.path.join(self.projectPath, self.BUNDLES)
        if not os.path.exists(bundlesPath):
            os.makedirs(bundlesPath)
        self.setBundles(bundlesPath)
            
    def ensureThemes(self):
        themesPath = os.path.join(self.projectPath, self.THEMES)
        if not os.path.exists(themesPath):
            os.makedirs(themesPath)
        self.setThemes(themesPath)
