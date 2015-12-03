#!/usr/bin/env python
import os
from prymatex.core import config
from prymatex.utils import json

class Project(object):
    KEYS = ( 'name', 'description', 'licence', 'keywords', 'source_folders', 
            'shell_variables', 'bundles', 'namespace_folders' )
    def __init__(self, path, manager):
        self.path = path
        self.manager = manager
        self.namespaces = []
        self.namespace_folders = []
        self.bundles = []
        self.source_folders = []
    
    # ---------------- Load, update, dump
    def __load_update(self, data_hash, initialize):
        dirname = os.path.dirname(self.path())
        for key in Project.KEYS:
            if key in data_hash or initialize:
                value = data_hash.pop(key, None)
                if value is None and key in ('source_folders', 'bundles', 'namespace_folders'):
                    value = []
                if key in ('source_folders', 'namespace_folders'):
                    value = [
                        os.path.normpath(
                            os.path.join(dirname, os.path.expanduser(v))
                        ) for v in value ]
                setattr(self, key, value)

    def load(self, data_hash):
        self.__load_update(data_hash, True)

    def update(self, data_hash):
        self.__load_update(data_hash, False)

    def dump(self, allKeys=False):
        data_hash = { }
        dirname = os.path.dirname(self.path )
        for key in Project.KEYS:
            value = getattr(self, key, None)
            if allKeys or value:
                if key in ("source_folders", "namespace_folders"):
                    value = [
                        re.sub(
                            "^%s" % config.USER_HOME_PATH, "~", os.path.relpath(v, dirname)
                        ) for v in value ]
                data_hash[key] = value
        return data_hash
    
    # ---------------- Variables
    @property
    def variables(self):
        return {
            'TM_PROJECT_FOLDERS': " ".join(["'%s'" % folder for folder in self.source_folders ]),
            'TM_PROJECT_NAMESPACES': " ".join(["'%s'" % folder for folder in self.namespace_folders ]),
            'TM_PROJECT_NAME': self.name,
            'TM_PROJECT_PATH': self.path }
            
    def save(self):
        directory = os.path.dirname(self.path())
        if not os.path.exists(directory):
            os.makedirs(directory)
        json.write_file(self.dump(), self.path())

    def delete(self, removeFiles=False):
        shutil.rmtree(self.path())
        if removeFiles:
            try:
                for folder in self.source_folders:
                    shutil.rmtree(folder)
            except OSError:
                pass
    
    def environmentVariables(self):
        environment = self.manager.environmentVariables()
        if isinstance(self.shell_variables, list):
            for var in self.shell_variables:
                if var['enabled']:
                    environment[var['variable']] = var['value']
        environment.update(self.variables)
        return environment

    def reload(self):
        data = json.read_file(self.path())
        self.setNodeName(data["name"])
        self.update(data)
        
    @classmethod
    def loadProject(cls, project_path, manager):
        if not os.path.isfile(project_path):
            raise exceptions.FileNotExistsException(project_path)
        try:
            data = json.read_file(project_path)
            project = cls(project_path, manager)
            project.load(data)
            manager.addProject(project)
            return project
        except Exception as e:
            import traceback
            traceback.print_exc()
            print("Error in project %s (%s)" % (project_path, e))
    
    def setManager(self, manager):
        self.manager = manager
    
    # --------------- Source folders
    def addSourceFolder(self, path):
        if path not in self.source_folders:
            self.source_folders.append(path)

    def removeSourceFolder(self, path):
        if path in self.source_folders:
            self.source_folders.remove(path)

    # --------------- namespace folders
    def addNamespace(self, namespace):
        if namespace.path not in self.namespace_folders: 
            self.namespace_folders.append(namespace.path)
        if namespace not in self.namespaces:
            self.namespaces.append(namespace)

    def removeNamespace(self, namespace):
        if path in self.namespace_folders:
            self.namespace_folders.remove(namespace.path)
        if namespace in self.namespaces:
            self.namespaces.remove(namespace)

    # --------------- Bundle Menu
    def addBundleMenu(self, bundle):
        if not isinstance(self.bundles, list):
            self.bundles = []
        self.bundles.append(bundle.uuidAsText())
        
    def removeBundleMenu(self, bundle):
        uuid = bundle.uuidAsText()
        if uuid in self.bundles:
            self.bundles.remove(uuid)
            
    def hasBundleMenu(self, bundle):
        if self.bundles is None: return False
        return bundle.uuidAsText() in self.bundles
