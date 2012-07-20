#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import string
import unicodedata
import hashlib
import uuid as uuidmodule
import subprocess
from glob import glob

from prymatex.support.bundle import PMXBundle, PMXBundleItem
from prymatex.support.macro import PMXMacro
from prymatex.support.syntax import PMXSyntax
from prymatex.support.snippet import PMXSnippet
from prymatex.support.preference import PMXPreference
from prymatex.support.command import PMXCommand, PMXDragCommand
from prymatex.support.template import PMXTemplate, PMXTemplateFile
from prymatex.support.project import PMXProject
from prymatex.support.theme import PMXTheme, PMXThemeStyle
from prymatex.support.score import PMXScoreManager
from prymatex.support.utils import ensurePath
from prymatex.support.cache import PMXSupportCache

from prymatex.utils.decorators.helpers import printtime
from prymatex.utils.decorators.memoize import dynamic_memoized, remove_memoized_argument, remove_memoized_function

BUNDLEITEM_CLASSES = [ PMXSyntax, PMXSnippet, PMXMacro, PMXCommand, PMXPreference, PMXTemplate, PMXDragCommand, PMXProject ]

def compare(obj, keys, tests):
    if not len(keys):
        return True
    key = keys[0]
    value = getattr(obj, key, None)
    if value == None or key not in tests:
        return False
    elif isinstance(value, (str, unicode)):
        return value.find(tests[key]) != -1 and compare(obj, keys[1:], tests)
    elif isinstance(value, (int)):
        return value == tests[key] and compare(obj, keys[1:], tests)
    else:
        return value == tests[key] and compare(obj, keys[1:], tests)

class PMXSupportBaseManager(object):
    ELEMENTS = ['Bundles', 'Support', 'Themes']
    VAR_PREFIX = 'PMX'
    PROTECTEDNS = 0         #El primero es el protected
    DEFAULTNS = 1           #El segundo es el default
    VALID_PATH_CARACTERS = "-_.() %s%s" % (string.ascii_letters, string.digits)
    
    SETTINGS_CACHE = {}
    
    def __init__(self):
        self.namespaces = {}
        self.nsorder = []
        
        self.ready = False
        self.environment = {}
        self.managedObjects = {}
        self.scores = PMXScoreManager()
    
    #---------------------------------------------------
    # Namespaces
    #---------------------------------------------------
    def addNamespace(self, name, path):
        self.namespaces[name] = {}
        self.nsorder.append(name)
        for element in self.ELEMENTS:
            epath = os.path.join(path, element)
            if not os.path.exists(epath):
                continue
            #Si es el primero es el protegido
            if len(self.nsorder) == 1:
                var = "_".join([ self.VAR_PREFIX, element.upper(), 'PATH' ])
            else:
                var = "_".join([ self.VAR_PREFIX, name.upper(), element.upper(), 'PATH' ])
            self.namespaces[name][element] = self.environment[var] = epath
        return name

    def hasNamespace(self, name):
        return name in self.namespaces

    @property
    def protectedNamespace(self):
        return self.nsorder[self.PROTECTEDNS]
        
    @property
    def defaultNamespace(self):
        if len(self.nsorder) < 2:
            raise Exception("No default namespace")
        return self.nsorder[self.DEFAULTNS]

    def addProjectNamespace(self, project):
        #TODO: Asegurar que no esta ya cargado eso del md5 es medio trucho
        project.ensureBundles()
        path = project.projectPath
        project.namespace = project.name
        while project.namespace in self.namespaces:
            #Crear valores random
            project.namespace = project.namespace + hashlib.md5(project.namespace + path).hexdigest()[:7]
        self.addNamespace(project.namespace, path)
        #Ya esta listo tengo que cargar este namespace
        if self.ready:
            self.loadThemes(project.namespace)
            for bundle in self.loadBundles(project.namespace):
                if bundle.enabled:
                    self.populateBundle(bundle)

    def addToEnvironment(self, name, value):
        self.environment[name] = value

    def updateEnvironment(self, env):
        self.environment.update(env)

    def buildEnvironment(self):
        env = {}
        env.update(os.environ)
        env.update(self.environment)
        return env
    
    def basePath(self, element, namespace):
        if namespace not in self.namespaces:
            raise Exception("The %s namespace is not registered" % namespace)
        if element in self.namespaces[namespace]:
            return self.namespaces[namespace][element]
    
    #---------------------------------------------------
    # Tools
    #---------------------------------------------------
    def uuidgen(self, uuid = None):
        # TODO: ver que el uuid generado no este entre los elementos existentes
        if uuid is None:
            return uuidmodule.uuid1()
        try:
            return uuidmodule.UUID(uuid)
        except ValueError:
            #generate
            return uuidmodule.uuid3(uuidmodule.NAMESPACE_DNS, uuid)

    def convertToValidPath(self, name):
        validPath = []
        for char in unicodedata.normalize('NFKD', unicode(name)).encode('ASCII', 'ignore'):
            char = char if char in self.VALID_PATH_CARACTERS else '-'
            validPath.append(char)
        return ''.join(validPath)

    def runProcess(self, context, callback):
        """ Synchronous run process"""
        origWD = os.getcwd() # remember our original working directory
        if context.workingDirectory is not None:
            os.chdir(context.workingDirectory)

        process = subprocess.Popen(context.shellCommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env = context.environment)
        
        if context.inputType is not None:
            process.stdin.write(unicode(context.inputValue).encode("utf-8"))
        process.stdin.close()
        try:
            context.outputValue = process.stdout.read()
            context.errorValue = process.stderr.read()
        except IOError, e:
            context.errorValue = str(e).decode("utf-8")
        process.stdout.close()
        process.stderr.close()
        context.outputType = process.wait()
        
        if context.workingDirectory is not None:
            os.chdir(origWD)
        
        callback(context)

    #---------------------------------------------------
    # Message Handler
    #---------------------------------------------------
    def showMessage(self, message):
        if self.messageHandler is not None:
            self.messageHandler(message)

    #---------------------------------------------------
    # LOAD ALL SUPPORT
    #---------------------------------------------------
    def loadSupport(self, callback = None):
        # Install message handler
        self.messageHandler = callback
        for ns in self.nsorder[::-1]:
            self.loadThemes(ns)
            self.loadBundles(ns)
        for bundle in self.getAllBundles():
            if bundle.enabled:
                self.populateBundle(bundle)
        # Uninstall message handler
        self.messageHandler = None
        self.ready = True

    #---------------------------------------------------
    # LOAD THEMES
    #---------------------------------------------------
    def loadThemes(self, namespace):
        loadedThemes = set()
        if 'Themes' in self.namespaces[namespace]:
            paths = glob(os.path.join(self.namespaces[namespace]['Themes'], '*.tmTheme'))
            for path in paths:
                theme = PMXTheme.loadTheme(path, namespace, self)
                if theme is not None:
                    loadedThemes.add(theme)
        return loadedThemes
        
    #---------------------------------------------------
    # LOAD BUNDLES
    #---------------------------------------------------
    def loadBundles(self, namespace):
        loadedBundles = set()
        if 'Bundles' in self.namespaces[namespace]:
            paths = glob(os.path.join(self.namespaces[namespace]['Bundles'], '*.tmbundle'))
            for path in paths:
                bundle = PMXBundle.loadBundle(path, namespace, self)
                if bundle is not None:
                    loadedBundles.add(bundle)
        return loadedBundles
        
    #---------------------------------------------------
    # POPULATE BUNDLE AND LOAD BUNDLE ITEMS
    #---------------------------------------------------
    def populateBundle(self, bundle):
        nss = bundle.namespaces[::-1]
        for namespace in nss:
            bpath = bundle.path(namespace)
            # Search for support
            if bundle.support == None and os.path.exists(os.path.join(bpath, 'Support')):
                bundle.setSupport(os.path.join(bpath, 'Support'))
            self.showMessage("Loading bundle %s" % bundle.name)
            for klass in BUNDLEITEM_CLASSES:
                files = reduce(lambda x, y: x + glob(y), [ os.path.join(bpath, klass.FOLDER, file) for file in klass.PATTERNS ], [])
                for path in files:
                    klass.loadBundleItem(path, namespace, bundle, self)
        bundle.populated = True
        self.populatedBundle(bundle)

    #---------------------------------------------------
    # RELOAD SUPPORT
    #---------------------------------------------------
    def reloadSupport(self, callback = None):
        #Reload Implica ver en todos los espacios de nombre instalados por cambios en los items
        # Install message handler
        self.messageHandler = callback
        self.logger.debug("Begin reload support.")
        for namespace in self.nsorder[::-1]:
            self.logger.debug("Search in %s, %s." % (namespace, self.namespaces[namespace]))
            self.reloadThemes(namespace)
            self.reloadBundles(namespace)
        for bundle in self.getAllBundles():
            if bundle.enabled:
                self.repopulateBundle(bundle)
        # Uninstall message handler
        self.messageHandler = None
        self.logger.debug("End reload support.")
    
    #---------------------------------------------------
    # RELOAD THEMES
    #---------------------------------------------------
    def reloadThemes(self, namespace):
        if 'Themes' in self.namespaces[namespace]:
            installedThemes = filter(lambda theme: theme.hasNamespace(namespace), self.getAllThemes())
            themePaths = glob(os.path.join(self.namespaces[namespace]['Themes'], '*.tmTheme'))
            for theme in installedThemes:
                themePath = theme.path(namespace)
                if themePath in themePaths:
                    if namespace == theme.currentNamespace and theme.sourceChanged(namespace):
                        self.logger.debug("Theme %s changed, reload from %s." % (theme.name, themePath))
                        theme.reloadTheme(theme, themePath, namespace, self)
                        theme.updateMtime(namespace)
                        self.modifyTheme(theme)
                    themePaths.remove(themePath)
                else:
                    theme.removeSource(namespace)
                    if not theme.hasSources():
                        self.logger.debug("Theme %s removed." % theme.name)
                        self.removeManagedObject(theme)
                        self.removeTheme(theme)
                    else:
                        theme.setDirty()
            for path in themePaths:
                self.logger.debug("New theme %s." % path)
                PMXTheme.loadTheme(path, namespace, self)
    
    #---------------------------------------------------
    # RELOAD BUNDLES
    #---------------------------------------------------
    def reloadBundles(self, namespace):
        if 'Bundles' in self.namespaces[namespace]:
            installedBundles = filter(lambda theme: theme.hasNamespace(namespace), self.getAllBundles())
            bundlePaths = glob(os.path.join(self.namespaces[namespace]['Bundles'], '*.tmbundle'))
            for bundle in installedBundles:
                bundlePath = bundle.path(namespace)
                if bundlePath in bundlePaths:
                    if namespace == bundle.currentNamespace and bundle.sourceChanged(namespace):
                        self.logger.debug("Bundle %s changed, reload from %s." % (bundle.name, bundlePath))
                        bundle.reloadBundle(bundle, bundlePath, namespace, self)
                        bundle.updateMtime(namespace)
                        self.modifyBundle(bundle)
                    bundlePaths.remove(bundlePath)
                else:
                    bundleItems = self.findBundleItems(bundle = bundle)
                    map(lambda item: item.removeSource(namespace), bundleItems)
                    bundle.removeSource(namespace)
                    if not bundle.hasSources():
                        self.logger.debug("Bundle %s removed." % bundle.name)
                        map(lambda item: self.removeManagedObject(item), bundleItems)
                        map(lambda item: self.removeBundleItem(item), bundleItems)
                        self.removeManagedObject(bundle)
                        self.removeBundle(bundle)
                    else:
                        map(lambda item: item.setDirty(), bundleItems)
                        bundle.support = None
                        bundle.setDirty()
            for path in bundlePaths:
                self.logger.debug("New bundle %s." % path)
                PMXBundle.loadBundle(path, namespace, self)
    
    #---------------------------------------------------
    # REPOPULATED BUNDLE AND RELOAD BUNDLE ITEMS
    #---------------------------------------------------
    def repopulateBundle(self, bundle):
        namespaces = bundle.namespaces[::-1]
        bundleItems = self.findBundleItems(bundle = bundle)
        for namespace in namespaces:
            bpath = bundle.path(namespace)
            # Search for support
            if bundle.support == None and os.path.exists(os.path.join(bpath, 'Support')):
                bundle.setSupport(os.path.join(bpath, 'Support'))
            bundleItemPaths = {}
            for klass in BUNDLEITEM_CLASSES:
                klassPaths = reduce(lambda x, y: x + glob(y), [ os.path.join(bpath, klass.FOLDER, file) for file in klass.PATTERNS ], [])
                bundleItemPaths.update(dict(map(lambda path: (path, klass), klassPaths)))
            for bundleItem in bundleItems:
                if not bundleItem.hasNamespace(namespace):
                    continue
                bundleItemPath = bundleItem.path(namespace)
                if bundleItemPath in bundleItemPaths:
                    if namespace == bundleItem.currentNamespace and bundleItem.sourceChanged(namespace):
                        self.logger.debug("Bundle Item %s changed, reload from %s." % (bundleItem.name, bundleItemPath))
                        bundleItem.reloadBundleItem(bundleItem, bundleItemPath, namespace, self)
                        bundleItem.updateMtime(namespace)
                        self.modifyBundleItem(bundleItem)
                    bundleItemPaths.pop(bundleItemPath)
                else:
                    bundleItem.removeSource(namespace)
                    if not bundleItem.hasSources():
                        self.logger.debug("Bundle Item %s removed." % bundleItem.name)
                        self.removeManagedObject(bundleItem)
                        self.removeBundleItem(bundleItem)
                    else:
                        bundleItem.setDirty()    
            for path, klass in bundleItemPaths.iteritems():
                self.logger.debug("New bundle item %s." % path)
                klass.loadBundleItem(path, namespace, bundle, self)
        self.populatedBundle(bundle)

    #---------------------------------------------------
    # MANAGED OBJECTS INTERFACE
    #---------------------------------------------------
    def setDeleted(self, uuid):
        """
        Marcar un managed object como eliminado
        """
        pass
        
    def isDeleted(self, uuid):
        """
        Retorna si un bundle item esta eliminado
        """
        return False

    def isEnabled(self, uuid):
        """
        Retorna si un bundle item esta activo
        """
        return True
    
    def setDisabled(self, uuid):
        pass
        
    def setEnabled(self, uuid):
        pass
    
    def addManagedObject(self, obj):
        self.managedObjects[obj.uuid] = obj
        
    def removeManagedObject(self, obj):
        self.managedObjects.pop(obj.uuid)
        
    def getManagedObject(self, uuid):
        if not isinstance(uuid, uuidmodule.UUID):
            uuid = uuidmodule.UUID(uuid)
        return self.managedObjects.get(uuid, None)
    
    #---------------------------------------------------
    # BUNDLE INTERFACE
    #---------------------------------------------------
    def addBundle(self, bundle):
        return bundle
        
    def modifyBundle(self, bundle):
        """Llamado luego de modificar un bundle"""
        pass

    def removeBundle(self, bundle):
        """Llamado luego de eliminar un bundle"""
        pass

    def populatedBundle(self, bundle):
        """Llamado luego de popular un bundle"""
        pass
        
    def getAllBundles(self):
        return []
    
    #---------------------------------------------------
    # BUNDLE CRUD
    #---------------------------------------------------
    def findBundles(self, **attrs):
        """
        Retorna todos los bundles que cumplan con attrs
        """
        bundles = []
        for bundle in self.getAllBundles():
            if compare(bundle, attrs.keys(), attrs):
                bundles.append(bundle)
        return bundles
    
    def createBundle(self, name, namespace = None):
        """
        Crea un bundle nuevo lo agrega en los bundles y lo retorna,
        Precondiciones:
            Tenes por lo menos dos espacios de nombre el base o proteguido y uno donde generar los nuevos bundles
            El nombre tipo Title.
            El nombre no este entre los nombres ya cargados.
        Toma el ultimo espacio de nombres creado como espacio de nombre por defecto para el bundle nuevo.
        """
        namespace = namespace or self.defaultNamespace
        basePath = self.basePath("Bundles", namespace)
        path = ensurePath(os.path.join(basePath, "%s.tmbundle"), self.convertToValidPath(name))
        bundle = PMXBundle(self.uuidgen(), { 'name': name })
        bundle.setManager(self)
        bundle.addSource(namespace, path)
        bundle = self.addBundle(bundle)
        self.addManagedObject(bundle)
        return bundle
        
    def readBundle(self, **attrs):
        """
        Retorna un bundle por sus atributos
        """
        bundles = self.findBundles(**attrs)
        if len(bundles) > 1:
            raise Exception("More than one bundle")
        return bundles[0]
    
    def getBundle(self, uuid):
        return self.getManagedObject(uuid)
    
    def updateBundle(self, bundle, namespace = None, **attrs):
        """Actualiza un bundle"""
        if len(attrs) == 1 and "name" in attrs and attrs["name"] == bundle.name:
            #Updates que no son updates
            return bundle

        namespace = namespace or self.defaultNamespace
        
        if bundle.isProtected and not bundle.isSafe:
            #Safe bundle
            basePath = self.basePath("Bundles", namespace)
            path = os.path.join(basePath, os.path.basename(bundle.path(self.protectedNamespace)))
            bundle.addSource(namespace, path)
            self.logger.debug("Add namespace '%s' in source %s for bundle." % (namespace, path))
        elif not bundle.isProtected and "name" in attrs:
            #Move bundle
            path = ensurePath(os.path.join(os.path.dirname(bundle.path(namespace)), "%s.tmbundle"), self.convertToValidPath(attrs["name"]))
            bundle.relocateSource(namespace, path)
        bundle.update(attrs)
        bundle.save(namespace)
        bundle.updateMtime(namespace)
        self.modifyBundle(bundle)
        return bundle
        
    def deleteBundle(self, bundle):
        """Elimina un bundle, si el bundle es del namespace proteguido no lo elimina sino que lo marca como eliminado"""
        #Primero los items
        items = self.findBundleItems(bundle = bundle)
        
        for item in items:
            self.deleteBundleItem(item)
        
        for namespace in bundle.namespaces:
            #Si el espacio de nombres es distinto al protegido lo elimino
            if namespace != self.protectedNamespace:
                bundle.delete(namespace)
            else:
                self.setDeleted(bundle.uuid)
        self.removeManagedObject(bundle)
        self.removeBundle(bundle)
    
    def disableBundle(self, bundle, disabled):
        if disabled:
            self.setDisabled(bundle.uuid)
        else:
            self.setEnabled(bundle.uuid)
            if not bundle.populated:
                self.populateBundle(bundle)
        self.modifyBundle(bundle)
    
    #---------------------------------------------------
    # BUNDLEITEM INTERFACE
    #---------------------------------------------------
    def addBundleItem(self, bundleItem):
        return bundleItem
        
    def modifyBundleItem(self, bundleItem):
        pass

    def removeBundleItem(self, bundleItem):
        pass
    
    def getAllBundleItems(self):
        return []
        
    #---------------------------------------------------
    # BUNDLEITEM CRUD
    #---------------------------------------------------
    def findBundleItems(self, **attrs):
        """
        Retorna todos los items que complan las condiciones en attrs
        """
        items = []
        for item in self.getAllBundleItems():
            if compare(item, attrs.keys(), attrs):
                items.append(item)
        return items

    def createBundleItem(self, name, tipo, bundle, namespace = None):
        """
        Crea un bundle item nuevo lo agrega en los bundle items y lo retorna,
        Precondiciones:
            Tenes por lo menos dos nombres en el espacio de nombres
            El tipo tiene que ser uno de los conocidos
        Toma el ultimo espacio de nombres creado como espacio de nombre por defecto para el bundle item nuevo.
        """
        namespace = namespace or self.defaultNamespace
        if bundle.isProtected and not bundle.isSafe:
            self.updateBundle(bundle, namespace)
        klass = filter(lambda c: c.TYPE == tipo, BUNDLEITEM_CLASSES)
        if len(klass) != 1:
            raise Exception("No class type for %s" % tipo)
        klass = klass.pop()
        path = os.path.join(bundle.path(namespace), klass.FOLDER, "%s.%s" % (self.convertToValidPath(name), klass.EXTENSION))

        item = klass(self.uuidgen(), { 'name': name })
        item.setBundle(bundle)
        item.setManager(self)
        item.addSource(namespace, path)
        item = self.addBundleItem(item)
        self.addManagedObject(item)
        return item
    
    def readBundleItem(self, **attrs):
        """
        Retorna un bundle item por sus atributos
        """
        items = self.findBundleItems(**attrs)
        if len(items) > 1:
            raise Exception("More than one bundle item")
        return items[0]
    
    def getBundleItem(self, uuid):
        return self.getManagedObject(uuid)
    
    def updateBundleItem(self, item, namespace = None, **attrs):
        """
        Actualiza un bundle item
        """
        if len(attrs) == 1 and "name" in attrs and attrs["name"] == item.name:
            #Updates que no son updates
            return item

        #Deprecate keyEquivalent in cache
        if 'keyEquivalent' in attrs and item.keyEquivalent != attrs['keyEquivalent']:
            remove_memoized_argument(item.keyEquivalent)
            remove_memoized_argument(attrs['keyEquivalent'])
            
        #Deprecate tabTrigger in cache
        if 'tabTrigger' in attrs and item.tabTrigger != attrs['tabTrigger']:
            remove_memoized_argument(item.tabTrigger)
            remove_memoized_argument(attrs['tabTrigger'])
            #Delete list of all tabTrigers
            remove_memoized_function(self.getAllTabTriggerItems)

        #TODO: Este paso es importante para obtener el namespace, quiza ponerlo en un metodo para trabajarlo un poco m�s
        namespace = namespace or self.defaultNamespace
        
        if item.bundle.isProtected and not item.bundle.isSafe:
            self.updateBundle(item.bundle, namespace)

        if item.isProtected and not item.isSafe:
            #Safe Bundle Item
            path = os.path.join(item.bundle.path(namespace), item.FOLDER, os.path.basename(item.path(self.protectedNamespace)))
            item.addSource(namespace, path)
            self.logger.debug("Add namespace '%s' in source %s for bundle item." % (namespace, path))
        elif not item.isProtected and "name" in attrs:
            #Move Bundle Item
            namePattern = "%%s.%s" % item.EXTENSION if item.EXTENSION else "%s"
            path = ensurePath(os.path.join(item.bundle.path(namespace), item.FOLDER, namePattern), self.convertToValidPath(attrs["name"]))
            item.relocateSource(namespace, path)
        item.update(attrs)
        item.save(namespace)
        item.updateMtime(namespace)
        self.modifyBundleItem(item)
        return item
    
    def deleteBundleItem(self, item):
        """Elimina un bundle por su uuid,
        si el bundle es del namespace proteguido no lo elimina sino que lo marca como eliminado
        """
        for namespace in item.namespaces:
            #Si el espacio de nombres es distinto al protegido lo elimino
            if namespace != self.protectedNamespace:
                item.delete(namespace)
            else:
                self.setDeleted(item.uuid)
        self.removeManagedObject(item)
        self.removeBundleItem(item)
        
    #---------------------------------------------------
    # TEMPLATEFILE INTERFACE
    #---------------------------------------------------
    def addTemplateFile(self, file):
        return file
    
    def removeTemplateFile(self, file):
        pass
    
    #---------------------------------------------------
    # TEMPLATEFILE CRUD
    #---------------------------------------------------
    def createTemplateFile(self, name, template, namespace = None):
        namespace = namespace or self.defaultNamespace
        if template.isProtected and not template.isSafe:
            self.updateBundleItem(template, namespace)
        path = ensurePath(os.path.join(template.path(namespace), "%s"), self.convertToValidPath(name))
        file = PMXTemplateFile(path, template)
        #No es la mejor forma pero es la forma de guardar el archivo
        file = self.addTemplateFile(file)
        template.files.append(file)
        file.save()
        return file

    def updateTemplateFile(self, templateFile, namespace = None, **attrs):
        namespace = namespace or self.defaultNamespace
        template = templateFile.template
        if template.isProtected and not template.isSafe:
            self.updateBundleItem(template, namespace)
        if "name" in attrs:
            path = ensurePath(os.path.join(template.path(namespace), "%s"), self.convertToValidPath(attrs["name"]))
            templateFile.relocate(path)
        templateFile.update(attrs)
        self.modifyBundleItem(templateFile)
        return templateFile

    def deleteTemplateFile(self, templateFile):
        template = templateFile.template
        if template.isProtected and not template.isSafe:
            self.deleteBundleItem(template)
        self.removeTemplateFile(templateFile)
    
    #---------------------------------------------------
    # THEME INTERFACE
    #---------------------------------------------------
    def addTheme(self, theme):
        return theme
    
    def modifyTheme(self, theme):
        pass
        
    def removeTheme(self, theme):
        pass
        
    def getAllThemes(self):
        return []
    
    #---------------------------------------------------
    # THEME CRUD
    #---------------------------------------------------
    def findThemes(self, **attrs):
        """
        Retorna todos los themes que complan las condiciones en attrs
        """
        items = []
        for item in self.getAllThemes():
            if compare(item, attrs.keys(), attrs):
                items.append(item)
        return items

    def createTheme(self, name, namespace = None):
        if len(self.nsorder) < 2:
            return None
        if namespace is None: namespace = self.defaultNamespace
        path = os.path.join(self.namespaces[namespace]['Themes'], "%s.tmTheme" % self.convertToValidPath(name))
        theme = PMXTheme(self.uuidgen(), namespace, { 'name': name }, path)
        theme = self.addTheme(theme)
        self.addManagedObject(theme)
        return theme

    def readTheme(self, **attrs):
        """
        Retorna un bundle item por sus atributos
        """
        items = self.findThemes(**attrs)
        if len(items) > 1:
            raise Exception("More than one theme")
        return items[0]
    
    def getTheme(self, uuid):
        return self.getManagedObject(uuid)
    
    def updateTheme(self, theme, namespace = None, **attrs):
        """
        Actualiza un themes
        """
        namespace = namespace or self.defaultNamespace
        if theme.isProtected and not theme.isSafe:
            path = os.path.join(self.namespaces[namespace]['Themes'], os.path.basename(theme.path(self.protectedNamespace)))
            theme.addSource(namespace, path)
        elif not theme.isProtected and "name" in attrs:
            path = ensurePath(os.path.join(os.path.dirname(theme.path(namespace)), "%s.tmTheme"), self.convertToValidPath(attrs["name"]))
            theme.relocateSource(namespace, path)
        theme.update(attrs)
        theme.save(namespace)
        theme.updateMtime(namespace)
        self.modifyTheme(theme)
        return theme
        
    def deleteTheme(self, theme):
        """
        Elimina un theme por su uuid
        """
        for namespace in theme.namespaces:
            #Si el espacio de nombres es distinto al protegido lo elimino
            if namespace != self.protectedNamespace:
                theme.delete(namespace)
            else:
                self.setDeleted(theme.uuid)
        self.removeManagedObject(theme)
        self.removeTheme(theme)
    
    #---------------------------------------------------
    # THEMESTYLE INTERFACE
    #---------------------------------------------------
    def addThemeStyle(self, style):
        return style
    
    def removeThemeStyle(self, style):
        pass
    
    #---------------------------------------------------
    # THEMESTYLE CRUD
    #---------------------------------------------------
    def createThemeStyle(self, name, scope, theme, namespace = None):
        namespace = namespace or self.defaultNamespace
        if theme.isProtected and not theme.isSafe:
            self.updateTheme(theme, namespace)
        style = PMXThemeStyle({'name': name, 'scope': scope, 'settings': {}}, theme)
        theme.styles.append(style)
        theme.save(namespace)
        theme.updateMtime(namespace)
        style = self.addThemeStyle(style)
        return style

    def updateThemeStyle(self, style, namespace = None, **attrs):
        namespace = namespace or self.defaultNamespace
        theme = style.theme
        if theme.isProtected and not theme.isSafe:
            self.updateTheme(theme, namespace)
        style.update(attrs)
        theme.save(namespace)
        theme.updateMtime(namespace)
        self.modifyTheme(theme)
        return style

    def deleteThemeStyle(self, style, namespace = None):
        namespace = namespace or self.defaultNamespace
        theme = style.theme
        if theme.isProtected and not theme.isSafe:
            self.updateTheme(theme, namespace)
        theme.styles.remove(style)
        theme.save(namespace)
        theme.updateMtime(namespace)
        self.removeThemeStyle(style)
        
    #---------------------------------------------------
    # PREFERENCES INTERFACE
    #---------------------------------------------------
    def getAllPreferences(self):
        """
        Return a list of all preferences bundle items
        """
        raise NotImplementedError
        
    #---------------------------------------------------------------
    # PREFERENCES
    #---------------------------------------------------------------
    def getPreferences(self, scope):
        with_bundle = []
        with_scope = []
        without_scope = []
        for preference in self.getAllPreferences():
            if not preference.scope:
                without_scope.append(preference)
            else:
                score = self.scores.score(preference.scope, scope)
                if score != 0:
                    with_scope.append((score, preference))
        with_bundle.sort(key = lambda t: t[0], reverse = True)
        with_scope.sort(key = lambda t: t[0], reverse = True)
        return map(lambda item: item[1], with_bundle + with_scope) + without_scope

    @dynamic_memoized
    def getPreferenceSettings(self, scope):
        return PMXPreference.buildSettings(self.getPreferences(scope))
        
    #---------------------------------------------------
    # TABTRIGGERS INTERFACE
    #---------------------------------------------------
    def getAllTabTriggerItems(self):
        """
        Return a list of all tab triggers
        ['class', 'def', ...]
        """
        raise NotImplementedError
    
    def getAllBundleItemsByTabTrigger(self, tabTrigger):
        """Return a list of tab triggers bundle items"""
        raise NotImplementedError
    
    #---------------------------------------------------------------
    # TABTRIGGERS
    #---------------------------------------------------------------
    #@printtime
    def getTabTriggerSymbol(self, line, index):
        line = line[:index][::-1]
        tabTriggerItems = self.getAllTabTriggerItems()
        search = map(lambda item: (item.tabTrigger, line.find(item.tabTrigger[::-1]), len(item.tabTrigger)), tabTriggerItems)
        search = filter(lambda (trigger, value, length): value == 0, search)
        if search:
            best = ("", 0)
            for trigger, value, length in search:
                if length > best[1]:
                    best = (trigger, length)
            return best[0]

    #@printtime
    def getAllTabTiggerItemsByScope(self, scope):
        with_scope = []
        without_scope = []
        for item in self.getAllTabTriggerItems():
            if not item.scope:
                without_scope.append(item)
            else:
                score = self.scores.score(item.scope, scope)
                if score != 0:
                    with_scope.append((score, item))
        with_scope.sort(key = lambda t: t[0], reverse = True)
        with_scope = map(lambda (score, item): item, with_scope)
        return with_scope + without_scope

    #@printtime
    def getTabTriggerItem(self, keyword, scope):
        with_scope = []
        without_scope = []
        for item in self.getAllBundleItemsByTabTrigger(keyword):
            if not item.scope:
                without_scope.append(item)
            else:
                score = self.scores.score(item.scope, scope)
                if score != 0:
                    with_scope.append((score, item))
        with_scope.sort(key = lambda t: t[0], reverse = True)
        with_scope = map(lambda (score, item): item, with_scope)
        return with_scope and with_scope or without_scope
    
    #---------------------------------------------------
    # KEYEQUIVALENT INTERFACE
    #---------------------------------------------------
    def getAllBundleItemsByKeyEquivalent(self, keyEquivalent):
        """Return a list of key equivalent bundle items"""
        raise NotImplementedError
        
    #---------------------------------------------------------------
    # KEYEQUIVALENT
    #---------------------------------------------------------------
    #@printtime
    def getKeyEquivalentItem(self, code, scope):
        with_scope = []
        without_scope = []
        for item in self.getAllBundleItemsByKeyEquivalent(code):
            if not item.scope:
                without_scope.append(item)
            else:
                score = self.scores.score(item.scope, scope)
                if score != 0:
                    with_scope.append((score, item))
        with_scope.sort(key = lambda t: t[0], reverse = True)
        with_scope = map(lambda (score, item): item, with_scope)
        return with_scope and with_scope or without_scope
    
    #---------------------------------------------------
    # FILE EXTENSION INTERFACE
    #---------------------------------------------------
    def getAllBundleItemsByFileExtension(self, path):
        """
        Return a list of file extension bundle items
        """
        raise NotImplementedError
        
    #---------------------------------------------------------------
    # FILE EXTENSION, for drag commands
    #---------------------------------------------------------------
    #@printtime
    def getFileExtensionItem(self, path, scope):
        with_scope = []
        without_scope = []
        for item in self.getAllBundleItemsByFileExtension(path):
            if not item.scope:
                without_scope.append(item)
            else:
                score = self.scores.score(item.scope, scope)
                if score != 0:
                    with_scope.append((score, item))
        with_scope.sort(key = lambda t: t[0], reverse = True)
        with_scope = map(lambda (score, item): item, with_scope)
        return with_scope and with_scope or without_scope
    
    #---------------------------------------------------
    # ACTION ITEMS INTERFACE
    #---------------------------------------------------
    def getAllActionItems(self):
        """
        Return action items
        """
        raise NotImplementedError
    
    #---------------------------------------------------------------
    # ACTION ITEMS FOR SCOPE
    #---------------------------------------------------------------
    #@printtime
    def getActionItems(self, scope):
        """
        Return a list of actions items for scope and without scope
        """
        with_scope = []
        without_scope = []
        for item in self.getAllActionItems():
            if not item.scope:
                without_scope.append(item)
            else:
                score = self.scores.score(item.scope, scope)
                if score != 0:
                    with_scope.append((score, item))
        with_scope.sort(key = lambda t: t[0], reverse = True)
        with_scope = map(lambda (score, item): item, with_scope)
        return with_scope + without_scope
    
    #---------------------------------------------------
    # SYNTAXES INTERFACE
    #---------------------------------------------------
    def getAllSyntaxes(self):
        raise NotImplementedError
    
    #---------------------------------------------------------------
    # SYNTAXES
    #---------------------------------------------------------------
    def getSyntaxesAsDictionary(self):
        return dict(map(lambda syntax: (syntax.scopeName, syntax), self.getAllSyntaxes()))
    
    def getSyntaxes(self, sort = False):
        stxs = []
        for syntax in self.getAllSyntaxes():
            stxs.append(syntax)
        if sort:
            return sorted(stxs, key = lambda s: s.name)
        return stxs
    
    def getSyntaxByScopeName(self, scopeName):
        syntaxes = self.getSyntaxesAsDictionary()
        if scopeName in syntaxes:
            return syntaxes[scopeName]
        return None
        
    def findSyntaxByFirstLine(self, line):
        for syntax in self.getAllSyntaxes():
            if syntax.firstLineMatch != None and syntax.firstLineMatch.search(line):
                return syntax
    
    def findSyntaxByFileType(self, fileType):
        for syntax in self.getAllSyntaxes():
            if syntax.fileTypes is not None and any(map(lambda ft: fileType == "%s" % ft, syntax.fileTypes)):
                return syntax

#===================================================
# PYTHON MANAGER
#===================================================
class PMXSupportPythonManager(PMXSupportBaseManager):
    BUNDLES = {}
    BUNDLE_ITEMS = {}
    THEMES = {}
    SYNTAXES = {}
    TAB_TRIGGERS = {}
    KEY_EQUIVALENTS = {}
    DRAGS = []
    PREFERENCES = []
    TEMPLATES = []
    
    def __init__(self):
        super(PMXSupportPythonManager, self).__init__()
    
    #---------------------------------------------------
    # BUNDLE INTERFACE
    #---------------------------------------------------
    def addBundle(self, bundle):
        '''
        @param bundle: PMXBundle instance
        '''
        self.BUNDLES[bundle.uuid] = bundle
        return bundle

    def modifyBundle(self, bundle):
        pass

    def removeBundle(self, bundle):
        '''
        @param bundle: PMXBundle instance
        '''
        self.BUNDLES.pop(bundle.uuid)

    def getAllBundles(self):
        '''
        @return: list of PMXBundle instances
        '''
        return self.BUNDLES.values()
    
    #---------------------------------------------------
    # BUNDLEITEM INTERFACE
    #---------------------------------------------------
    def addBundleItem(self, item):
        self.BUNDLE_ITEMS[item.uuid] = item
        if item.bundle.mainMenu != None:
            item.bundle.mainMenu[item.uuid] = item
        if item.tabTrigger != None:
            self.TAB_TRIGGERS.setdefault(item.tabTrigger, []).append(item)
        if item.keyEquivalent != None:
            self.KEY_EQUIVALENTS.setdefault(item.keyEquivalent, []).append(item)
        if item.TYPE == 'preference':
            self.PREFERENCES.append(item)
        elif item.TYPE == 'template':
            self.TEMPLATES.append(item)
        elif item.TYPE == 'syntax':
            self.SYNTAXES[item.scopeName] = item
        return item

    def modifyBundleItem(self, item):
        pass

    def removeBundleItem(self, item):
        self.BUNDLE_ITEMS.pop(item.uuid)
    
    def getAllBundleItems(self):
        return self.BUNDLE_ITEMS.values()
        
    #---------------------------------------------------
    # THEME INTERFACE
    #---------------------------------------------------
    def addTheme(self, theme):
        self.THEMES[theme.uuid] = theme
        return theme
        
    def modifyTheme(self, theme):
        pass
        
    def removeTheme(self, theme):
        self.THEMES.pop(theme.uuid)

    def getAllThemes(self):
        return self.THEMES.values()
    
    #---------------------------------------------------
    # PREFERENCES INTERFACE
    #---------------------------------------------------
    def getAllPreferences(self):
        '''
            Return all preferences
        '''
        return self.PREFERENCES
    
    #---------------------------------------------------
    # TABTRIGGERS INTERFACE
    #---------------------------------------------------
    def getAllTabTriggersMnemonics(self):
        """
        Return a list of tab triggers
        ['class', 'def', ...]
        """
        return self.TAB_TRIGGERS.keys()
    
    def getAllBundleItemsByTabTrigger(self, tabTrigger):
        """
        Return a list of tab triggers bundle items
        """
        if tabTrigger not in self.TAB_TRIGGERS:
            return []
        return self.TAB_TRIGGERS[tabTrigger]
    
    #---------------------------------------------------
    # KEYEQUIVALENT INTERFACE
    #---------------------------------------------------
    def getAllBundleItemsByKeyEquivalent(self, keyEquivalent):
        """
        Return a list of key equivalent bundle items
        """
        if keyEquivalent not in self.KEY_EQUIVALENTS:
            return [] 
        return self.KEY_EQUIVALENTS[keyEquivalent]
    
    #---------------------------------------------------------------
    # SYNTAXES
    #---------------------------------------------------------------
    def getSyntaxes(self, sort = False):
        stxs = []
        for syntax in self.SYNTAXES.values():
            stxs.append(syntax)
        if sort:
            return sorted(stxs, key = lambda s: s.name)
        return stxs
    
    def getSyntaxByScopeName(self, scope):
        if scope in self.SYNTAXES:
            return self.SYNTAXES[scope]
        return None
        
    def findSyntaxByFirstLine(self, line):
        for syntax in self.SYNTAXES.values():
            if syntax.firstLineMatch != None and syntax.firstLineMatch.search(line):
                return syntax
