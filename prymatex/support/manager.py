#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import string
import shutil
import hashlib
import uuid as uuidmodule
import subprocess
from glob import glob
from collections import namedtuple, OrderedDict

from .bundle import PMXBundle
from . import bundleitem 
from . import scope
from .theme import PMXTheme, PMXThemeStyle
from .staticfile import PMXStaticFile
from .process import RunningContext

from prymatex.utils import plist, osextra, six
from prymatex.utils import encoding

from functools import reduce

Namespace = namedtuple("Namespace", "name basedir protected bundles support themes")

# ------- Tool function for compare bundle items by attributes
def compare(obj, keys, tests):
    if not len(keys):
        return True
    key = keys[0]
    value = getattr(obj, key, None)
    if value == None or key not in tests:
        return False
    elif isinstance(value, str):
        return value.find(tests[key]) != -1 and compare(obj, keys[1:], tests)
    elif isinstance(value, (int)):
        return value == tests[key] and compare(obj, keys[1:], tests)
    else:
        return value == tests[key] and compare(obj, keys[1:], tests)

# ======================================================
# Manager of Bundles, Bundle Items and Themes
# This objects contains the basic functions for items handling
# Every set of items lives inside a namespace
# ======================================================
class PMXSupportBaseManager(object):
    ELEMENTS = ('bundles', 'support', 'themes')
    VAR_PREFIX = 'PMX'
    PROTECTEDNS = 0  # El primero es el protected
    DEFAULTNS = 1  # El segundo es el default
    BUNDLEITEM_CLASSES = dict([ (cls.TYPE, cls) for cls in (
        bundleitem.PMXSyntax,
        bundleitem.PMXSnippet,
        bundleitem.PMXMacro,
        bundleitem.PMXCommand,
        bundleitem.PMXDragCommand,
        bundleitem.PMXProxy,
        bundleitem.PMXPreference,
        bundleitem.PMXTemplate,
        bundleitem.PMXProject
    )])

    SETTINGS_CACHE = {}

    def __init__(self):
        self.namespaces = OrderedDict()
        
        self.ready = False
        self.environment = {}
        self.managedObjects = {}

        # Cache!!
        self.bundleItemCache = self.buildBundleItemStorage()
        self.plistFileCache = self.buildPlistFileStorage()
        
    # ------------ Namespaces ----------------------
    def addNamespace(self, name, path):
        directories = dict(
            [ (element, os.path.join(path, element.title())) for element in self.ELEMENTS ]
        )
        namespace = Namespace(
            name = name, 
            basedir = path,
            protected = len(self.namespaces) == 0,
            **directories)
        self.namespaces[name] = namespace
        return namespace

    def hasNamespace(self, name):
        return name in self.namespaces

    def protectedNamespace(self):
        return list(self.namespaces.values())[self.PROTECTEDNS]

    def defaultNamespace(self):
        return list(self.namespaces.values())[self.DEFAULTNS]

    def safeNamespaceNames(self):
        return list(self.namespaces.keys())[self.DEFAULTNS:]

    def safeNamespace(self, name = None):
        if name is None:
            return self.defaultNamespace()
        namespace = self.namespaces[name]
        if namespace.protected:
            return self.defaultNamespace()
        return namespace

    def namespace(self, name):
        return self.namespaces.get(name)

    def addProjectNamespace(self, project):
        #TODO: Asegurar que no esta ya cargado eso del md5 es medio trucho
        path = project.projectPath
        project.namespaceName = project.name
        while project.namespaceName in self.namespaces:
            #Crear valores random
            project.namespaceName = project.namespaceName + hashlib.md5(project.namespaceName + path).hexdigest()[:7]
        namespace = self.addNamespace(project.namespaceName, path)
        #Ya esta listo tengo que cargar este namespace
        if self.ready:
            self.loadThemes(namespace)
            for bundle in self.loadBundles(namespace):
                if bundle.enabled():
                    self.populateBundle(bundle)

    #-------------- Environment ---------------------
    def environmentVariables(self):
        environment = self.environment.copy()
        # TODO: Esto no puede durar mucho es costoso
        for namespace in self.namespaces.values():
            for element in self.ELEMENTS:
                elementDirectory = getattr(namespace, element)
                if os.path.exists(elementDirectory):
                    variableName = [ self.VAR_PREFIX, element.upper(), 'PATH' ]
                    if not namespace.protected:
                        variableName.insert(1, namespace.name.upper())
                    variableName = "_".join(variableName)
                    environment[variableName] = elementDirectory
        return environment

    def addToEnvironment(self, name, value):
        self.environment[name] = value

    def updateEnvironment(self, env):
        self.environment.update(env)

    #----------- Paths for namespaces --------------------
    def namespaceElementPath(self, namespace, element, create = False):
        assert namespace in self.namespaces, "The %s namespace is not registered" % namespace
        assert element in self.ELEMENTS, "The %s namespace is not registered" % namespace
        path = os.path.join(self.namespaces[namespace]["dirname"], element)
        if element not in self.namespaces[namespace] and create:
            os.makedirs(path)
            self.addNamespaceElement(namespace, element, path)
        return path, os.path.exists(path)

    #--------------- Plist --------------------
    def readPlist(self, path):
        if path in self.plistFileCache:
            return self.plistFileCache.get(path)
        return self.plistFileCache.setdefault(path, plist.readPlist(path))

    def writePlist(self, hashData, path):
        # TODO Ver que pasa con este set que falta
        self.plistFileCache.set(path, hashData)
        return plist.writePlist(hashData, path)

    #--------------- Tools --------------------
    def uuidgen(self, uuid = None):
        if uuid is None:
            return uuidmodule.uuid1()
        try:
            return uuidmodule.UUID(uuid)
        except ValueError:
            # Generate
            return uuidmodule.uuid3(uuidmodule.NAMESPACE_DNS, uuid)

    #--------------- Run system commands --------------------
    def runSystemCommand(self, **attrs):
        """Synchronous run system command"""
        context = RunningContext(**attrs)
        
        origWD = os.getcwd()  # remember our original working directory
        if context.workingDirectory is not None:
            os.chdir(context.workingDirectory)

        context.process = subprocess.Popen(context.shellCommand, 
            stdin = subprocess.PIPE, stdout = subprocess.PIPE, 
            stderr = subprocess.PIPE, env = context.environment)

        if context.inputValue is not None:
            context.process.stdin.write(encoding.to_fs(context.inputValue))
        context.process.stdin.close()
        try:
            context.outputValue = encoding.from_fs(context.process.stdout.read())
            context.errorValue = encoding.from_fs(context.process.stderr.read())
        except IOError as e:
            context.errorValue =  six.text_type(e)
        context.process.stdout.close()
        context.process.stderr.close()
        context.outputType = context.process.wait()

        if context.workingDirectory is not None:
            os.chdir(origWD)
        
        if context.callback is not None:
            context.callback(context)
        return context

    #--------------- Ad-Hoc Bundle Items --------------
    def buildAdHocCommand(self, commandScript, bundle, name=None, commandInput="none", commandOutput="insertText"):
        commandHash = {'command': commandScript,
                       'input': commandInput,
                       'output': commandOutput}
        commandHash['name'] = name if name is not None else "Ad-Hoc command %s" % commandScript

        command = bundleitem.PMXCommand(self.uuidgen(), self, bundle)
        command.load(commandHash)
        return command

    def buildAdHocSnippet(self, snippetContent, bundle, name=None, tabTrigger=None):
        snippetHash = {'content': snippetContent,
                       'tabTrigger': tabTrigger}
        snippetHash['name'] = name if name is not None else "Ad-Hoc snippet"
        snippet = bundleitem.PMXSnippet(self.uuidgen(), self, bundle)
        snippet.load(snippetHash)
        return snippet

    def buildAdHocSyntax(self, syntax, bundle, name=None):
        syntaxHash = syntax.copy()
        syntaxHash['name'] = name if name is not None else "Ad-Hoc syntax"
        syntax = bundleitem.PMXSyntax(self.uuidgen(), self, bundle)
        syntax.load(syntaxHash)
        return syntax

    #--------------- Scopes selectors and context --------------
    def scopeFactory(self, data):
        return scope.Scope.factory(isinstance(data, six.string_types) and data.split() or data)
        
    def selectorFactory(self, selector):
        return scope.Selector(selector)
        
    def contextFactory(self, leftScope, rightScope = None):
        return scope.Context(leftScope, rightScope or leftScope)
    
    # ------------------ SCOPE ATTRIBUTES
    def attributeScopes(self, filePath, projectDirectory = None):
        return self.scopeFactory(scope.attributes(filePath, projectDirectory))
    
    def __sort_filter_items(self, items, leftScope, rightScope = None):
        context = self.contextFactory(leftScope, rightScope)
        sortFilterItems = []
        for item in items:
            rank = []
            if item.selector.does_match(context, rank):
                sortFilterItems.append((rank.pop(), item))
        sortFilterItems.sort(key=lambda t: t[0], reverse = True)
        return [score_item[1] for score_item in sortFilterItems]

    #---------------- Message Handler ----------------
    def showMessage(self, message):
        if self.messageHandler is not None:
            self.messageHandler(message)

    #------------ LOAD ALL SUPPORT ----------------------------
    def loadSupport(self, callback=None):
        # Install message handler
        self.messageHandler = callback
        for namespace in self.namespaces.values():
            self.loadThemes(namespace)
            self.loadBundles(namespace)
        for bundle in self.getAllBundles():
            if bundle.enabled():
                self.populateBundle(bundle)
        # Uninstall message handler
        self.messageHandler = None
        self.ready = True

    #-------------- LOAD THEMES ---------------------------
    def loadThemes(self, namespace):
        loadedThemes = set()
        for sourceThemePath in PMXTheme.sourcePaths(namespace.themes):
            try:
                theme = self.loadTheme(sourceThemePath, namespace)
                self.showMessage("Loading theme\n%s" % theme.name)
                loadedThemes.add(theme)
            except Exception as ex:
                import traceback
                print("Error in laod theme %s (%s)" % (sourceThemePath, ex))
                traceback.print_exc()
        return loadedThemes

    def loadTheme(self, sourceThemePath, namespace):
        data = self.readPlist(PMXTheme.dataFilePath(sourceThemePath))
        uuid = self.uuidgen(data.pop('uuid', None))
        theme = self.getManagedObject(uuid)
        if theme is None:
            theme = PMXTheme(uuid, self)
            theme.load(data)
            theme = self.addTheme(theme)
            self.addManagedObject(theme)
        else:
            theme.load(data)
        theme.addSource(namespace.name, sourceThemePath)
        return theme

    #------------- LOAD BUNDLES ------------------
    def loadBundles(self, namespace):
        loadedBundles = set()
        for sourceBundlePath in PMXBundle.sourcePaths(namespace.bundles):
            try:
                bundle = self.loadBundle(sourceBundlePath, namespace)
                loadedBundles.add(bundle)
            except Exception as ex:
                import traceback
                print("Error in laod bundle %s (%s)" % (sourceBundlePath, ex))
                traceback.print_exc()
        return loadedBundles

    def loadBundle(self, sourceBundlePath, namespace):
        data = self.readPlist(PMXBundle.dataFilePath(sourceBundlePath))
        uuid = self.uuidgen(data.pop('uuid', None))
        bundle = self.getManagedObject(uuid)
        if bundle is None:
            bundle = PMXBundle(uuid, self)
            bundle.load(data)
            bundle = self.addBundle(bundle)
            self.addManagedObject(bundle)
        else:
            bundle.load(data)
        bundle.addSource(namespace.name, sourceBundlePath)
        return bundle

    # ----------- POPULATE BUNDLE AND LOAD BUNDLE ITEMS
    def populateBundle(self, bundle):
        for namespace in self.namespaces.values():
            if not bundle.hasSource(namespace.name):
                continue
            bundleDirectory = os.path.dirname(bundle.sourcePath(namespace.name))

            self.showMessage("Populating\n%s" % bundle.name)
            for klass in self.BUNDLEITEM_CLASSES.values():
                for sourceBundleItemPath in klass.sourcePaths(bundle.sourcePath(namespace.name)):
                    try:
                        bundleItem = self.loadBundleItem(klass, sourceBundleItemPath, namespace, bundle)
                    except Exception as e:
                        import traceback
                        print("Error in bundle item %s (%s)" % (sourceBundleItemPath, e))
                        traceback.print_exc()
        bundle.populate()
        self.populatedBundle(bundle)

    def loadBundleItem(self, klass, sourceBundleItemPath, namespace, bundle):
        data = self.readPlist(klass.dataFilePath(sourceBundleItemPath))
        uuid = self.uuidgen(data.pop('uuid', None))
        bundleItem = self.getManagedObject(uuid)
        if bundleItem is None:
            bundleItem = klass(uuid, self, bundle)
            bundleItem.load(data)
            bundleItem = self.addBundleItem(bundleItem)
            for staticPath in klass.staticFilePaths(sourceBundleItemPath):
                # TODO: Ver que hacer con directorios
                staticFile = PMXStaticFile(staticPath, bundleItem)
                staticFile = self.addStaticFile(staticFile)
                bundleItem.addStaticFile(staticFile)
            self.addManagedObject(bundleItem)
        else:
            bundleItem.load(data)
        bundleItem.addSource(namespace.name, sourceBundleItemPath)
        return bundleItem

    # -------------------- RELOAD SUPPORT
    def reloadSupport(self, callback = None):
        # Reload Implica ver en todos los espacios de nombre instalados por cambios en los items
        # Install message handler
        self.messageHandler = callback
        self.logger.debug("Begin reload support.")
        for namespace in self.namespaces.values():
            print(namespace.name)
            self.logger.debug("Search in %s, %s." % (namespace.name, namespace.basedir))
            self.reloadThemes(namespace)
            self.reloadBundles(namespace)
        for bundle in self.getAllBundles():
            if bundle.enabled():
                self.repopulateBundle(bundle)
        # Uninstall message handler
        self.messageHandler = None
        self.logger.debug("End reload support.")

    # ------------------ RELOAD THEMES
    def reloadThemes(self, namespace):
        installedThemes = [ theme for theme in self.getAllThemes() if theme.hasSource(namespace.name) ]
        themePaths = PMXTheme.sourcePaths(namespace.themes)
        print(themePaths)
        for theme in installedThemes:
            themePath = theme.sourcePath(namespace.name)
            if themePath in themePaths:
                if namespace.name == theme.currentSourceName() and theme.sourceChanged(namespace.name):
                    self.loadTheme(themePath, namespace)
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
            self.loadTheme(path, namespace)

    # ---------------- RELOAD BUNDLES
    def reloadBundles(self, namespace):
        installedBundles = [bundle for bundle in self.getAllBundles() if bundle.hasSource(namespace.name)]
        bundlePaths =  PMXBundle.sourcePaths(namespace.bundles)
        for bundle in installedBundles:
            bundlePath = bundle.sourcePath(namespace.name)
            if bundlePath in bundlePaths:
                if namespace.name == bundle.currentSourceName() and bundle.sourceChanged(namespace.name):
                    self.loadBundle(bundlePath, namespace)
                    self.modifyBundle(bundle)
                bundlePaths.remove(bundlePath)
            else:
                bundleItems = self.findBundleItems(bundle = bundle)
                list(map(lambda item: item.removeSource(namespace.name), bundleItems))
                bundle.removeSource(namespace)
                if not bundle.hasSources():
                    self.logger.debug("Bundle %s removed." % bundle.name)
                    list(map(lambda item: self.removeManagedObject(item), bundleItems))
                    list(map(lambda item: self.removeBundleItem(item), bundleItems))
                    self.removeManagedObject(bundle)
                    self.removeBundle(bundle)
                else:
                    list(map(lambda item: item.setDirty(), bundleItems))
                    bundle.setSupportPath(None)
                    bundle.setDirty()
        for bundlePath in bundlePaths:
            self.logger.debug("New bundle %s." % bundlePath)
            try:
                bundle = self.loadBundle(bundlePath, namespace)
            except Exception as ex:
                import traceback
                print("Error in laod bundle %s (%s)" % (bundlePath, ex))
                traceback.print_exc()

    # ----- REPOPULATED BUNDLE AND RELOAD BUNDLE ITEMS
    def repopulateBundle(self, bundle):
        for namespace in self.namespaces.values():
            if not bundle.hasSource(namespace.name):
                continue
            bundlePath = bundle.sourcePath(namespace.name)
            bundleItemPaths = dict([ (klass.TYPE, klass.sourcePaths(bundlePath)) 
                for klass in self.BUNDLEITEM_CLASSES.values() ])
            print(bundleItemPaths)
            for bundleItem in self.findBundleItems(bundle=bundle):
                if not bundleItem.hasSource(namespace.name):
                    continue
                bundleItemPath = bundleItem.sourcePath(namespace.name)
                if bundleItemPath in bundleItemPaths[bundleItem.TYPE]:
                    if namespace.name == bundleItem.currentSourceName() and bundleItem.sourceChanged(namespace.name):
                        self.logger.debug("Bundle Item %s changed, reload from %s." % (bundleItem.name, bundleItemPath))
                        self.loadBundleItem(self.BUNDLEITEM_CLASSES[bundleItem.TYPE], bundleItemPath, namespace, bundle)
                        self.modifyBundleItem(bundleItem)
                    bundleItemPaths[bundleItem.TYPE].remove(bundleItemPath)
                else:
                    bundleItem.removeSource(namespace.name)
                    if not bundleItem.hasSources():
                        self.logger.debug("Bundle Item %s removed." % bundleItem.name)
                        self.removeManagedObject(bundleItem)
                        self.removeBundleItem(bundleItem)
                    else:
                        bundleItem.setDirty()
            for itemType, itemPaths in bundleItemPaths.items():
                klass = self.BUNDLEITEM_CLASSES[itemType]
                for itemPath in itemPaths:
                    try:
                        self.logger.debug("New bundle item %s." % itemPath)
                        item = self.loadBundleItem(klass, itemPath, namespace, bundle)
                    except Exception as e:
                        import traceback
                        print("Error in bundle item %s (%s)" % (itemPath, e))
                        traceback.print_exc()
        self.populatedBundle(bundle)

    # ------------ Build Storages --------------------
    def buildPlistFileStorage(self):
        return {}

    def buildBundleItemStorage(self):
        return {}

    # ------------ Cache coherence -----------------
    def updateBundleItemCacheCoherence(self, bundleItem, attrs):
        # TODO NamedTuples para las keys
        keys = []
        testKeyEquivalent = bool('keyEquivalent' in attrs and bundleItem.keyEquivalent != attrs['keyEquivalent'])
        testTabTrigger = bool('tabTrigger' in attrs and bundleItem.tabTrigger != attrs['tabTrigger'])
        testScope = bool('scope' in attrs and bundleItem.scope != attrs['scope'])
        testPreference = bool(bundleItem.TYPE == 'preference')

        scopeSelectorItem = testScope and self.selectorFactory(bundleItem.scope) or None
        scopeSelectorAttr = testScope and self.selectorFactory(attrs['scope']) or None
        
        # Add keys for remove
        for key in self.bundleItemCache.keys():
            if testKeyEquivalent:
                if (key[0] == "getKeyEquivalentItem" and key[1] in [ bundleItem.keyEquivalent, attrs['keyEquivalent']]) or\
                key[0] == "getAllKeyEquivalentItems":
                    keys.append(key)
                    continue
            if testTabTrigger:
                if (key[0] == "getTabTriggerItem" and key[1] in [ bundleItem.tabTrigger, attrs['tabTrigger']]) or\
                key[0] == "getAllTabTriggerItems":
                    keys.append(key)
                    continue
            if testPreference and key[0] == "getPreferenceSettings":
                keys.append(key)
                continue
            if testScope and ( (key[2] and scopeSelectorItem.does_match(key[2])) or\
            (key[3] and scopeSelectorItem.does_match(key[3])) or\
            (key[2] and scopeSelectorAttr.does_match(key[2])) or\
            (key[3] and scopeSelectorAttr.does_match(key[3]))):
                keys.append(key)    
            
        # Quitar claves
        for key in keys:
            self.bundleItemCache.pop(key)

    # ----------- MANAGED OBJECTS INTERFACE
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

    def isProtected(self, obj):
        return obj.hasSource(self.protectedNamespace().name)
        
    def isSafe(self, obj):
        return obj.currentSourceName() != self.protectedNamespace().name

    def addManagedObject(self, obj):
        self.managedObjects[obj.uuid] = obj

    def removeManagedObject(self, obj):
        self.managedObjects.pop(obj.uuid)

    def getManagedObject(self, uuid):
        if not isinstance(uuid, uuidmodule.UUID):
            uuid = uuidmodule.UUID(uuid)
        if not self.isDeleted(uuid):
            return self.managedObjects.get(uuid, None)

    def saveManagedObject(self, obj, namespace):
        
        # Save obj
        filePath = obj.dataFilePath(obj.sourcePath(namespace.name))
        dirname = os.path.dirname(filePath)
                
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        self.writePlist(obj.dump(), filePath)
        
        # Save static files
        for static in obj.statics:
            static.save(dirname)
        
        obj.updateMtime(namespace.name)
        
    def moveManagedObject(self, obj, namespace, dst):
        src = obj.path(namespace)
        shutil.move(src, dst)
        obj.addSource(namespace.name, path)
        
    def deleteManagedObject(self, obj, namespace):
        filePath = obj.dataFilePath(obj.sourcePath(namespace.name))
        dirname = os.path.dirname(filePath)
        
        # Delete static files
        for static in obj.statics:
            os.unlink(static.path)

        os.unlink(filePath)
        if not os.listdir(dirname):
            os.rmdir(dirname)

    # ------------- BUNDLE INTERFACE
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
    
    # ------------- BUNDLE CRUD
    def findBundles(self, **attrs):
        """Retorna todos los bundles que cumplan con attrs"""
        bundles = []
        for bundle in self.getAllBundles():
            if compare(bundle, list(attrs.keys()), attrs):
                bundles.append(bundle)
        return bundles

    def createBundle(self, namespaceName, **attrs):
        """Crea un bundle nuevo lo agrega en los bundles y lo retorna.
        Precondiciones:
            Tenes por lo menos dos espacios de nombre el base o proteguido y
            uno donde generar los nuevos bundles
        """
        namespace = self.safeNamespace(namespaceName)
        
        bundleAttributes = PMXBundle.DEFAULTS.copy()
        bundleAttributes.update(attrs)
        
        # Create Bundle
        bundle = PMXBundle(self.uuidgen(), self)
        bundle.load(bundleAttributes)
        bundle.addSource(namespace.name, bundle.createSourcePath(namespace.bundles))
        
        self.saveManagedObject(bundle, namespace)
        
        bundle = self.addBundle(bundle)
        self.addManagedObject(bundle)
        return bundle

    def readBundle(self, **attrs):
        """Retorna un bundle por sus atributos"""
        bundles = self.findBundles(**attrs)
        if len(bundles) > 1:
            raise Exception("More than one bundle")
        return bundles[0]

    def getBundle(self, uuid):
        return self.getManagedObject(uuid)

    def ensureBundleIsSafe(self, bundle, namespace):
        """Ensure the bundle is safe"""
        if self.isProtected(bundle) and not self.isSafe(bundle):
            #Safe bundle
            bundle.addSource(namespace.name, bundle.createSourcePath(namespace.bundles))
            bundle.setCurrentSource(namespace.name)
            self.saveManagedObject(bundle, namespace)
            self.logger.debug("Add namespace '%s' in source %s for bundle." % (namespace.name, bundle.sourcePath(namespace.name)))
        return bundle

    def updateBundle(self, bundle, namespaceName, **attrs):
        """Actualiza un bundle"""
        namespace = self.safeNamespace(namespaceName)

        bundle = self.ensureBundleIsSafe(bundle, namespace)
        
        moveSource = not self.isProtected(bundle) and "name" in attrs
        
        # Do update and save
        bundle.update(attrs)
        self.saveManagedObject(bundle, namespace)
        self.modifyBundle(bundle)
        if moveSource:
            # Para mover hay que renombrar el directorio y mover todos los items del bundle
            bundleSourcePath = bundle.currentSourcePath()
            bundleDestinyPath = bundle.createSourcePath(namespace.bundles)
            shutil.move(bundleSourcePath, bundleDestinyPath)
            bundle.setSourcePath(namespace.name, bundleDestinyPath)
            for bundleItem in self.findBundleItems(bundle = bundle):
                bundleItemSourcePath = bundleItem.currentSourcePath()
                bundleItemDestinyPath = bundleDestinyPath + bundleItemSourcePath[len(bundleSourcePath):]
                bundleItem.setSourcePath(namespace.name, bundleItemDestinyPath)
        return bundle

    def deleteBundle(self, bundle):
        """Elimina un bundle, si el bundle es del namespace proteguido no lo elimina sino que lo marca como eliminado"""
        #Primero los bundleItems
        bundleItems = self.findBundleItems(bundle = bundle)

        for bundleItem in bundleItems:
            self.deleteBundleItem(bundleItem)

        for namespace in self.namespaces.values():
            if not bundle.hasSource(namespace.name):
                continue
            #Si el espacio de nombres es distinto al protegido lo elimino
            if namespace.protected:
                self.setDeleted(bundle.uuid)
            else:
                self.deleteManagedObject(bundle, namespace)
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

    # --------------- BUNDLEITEM INTERFACE
    def addBundleItem(self, bundleItem):
        return bundleItem

    def modifyBundleItem(self, bundleItem):
        pass

    def removeBundleItem(self, bundleItem):
        pass

    def getAllBundleItems(self):
        return []

    # -------------- BUNDLEITEM CRUD
    def findBundleItems(self, **attrs):
        """
        Retorna todos los items que complan las condiciones en attrs
        """
        bundleItems = []
        for bundleItem in self.getAllBundleItems():
            if compare(bundleItem, list(attrs.keys()), attrs):
                bundleItems.append(bundleItem)
        return bundleItems
    
    def createBundleItem(self, typeName, bundle, namespaceName, **attrs):
        """
        Crea un bundle item nuevo lo agrega en los bundle items y lo retorna,
        Precondiciones:
            Tenes por lo menos dos nombres en el espacio de nombres
            El typeName tiene que ser uno de los conocidos
        Toma el ultimo espacio de nombres creado como espacio de nombre por defecto para el bundle item nuevo.
        """
        namespace = self.safeNamespace(namespaceName)
        
        bundle = self.ensureBundleIsSafe(bundle, namespace)

        klass = self.BUNDLEITEM_CLASSES[typeName]
        
        bundleAttributes = klass.DEFAULTS.copy()
        bundleAttributes.update(attrs)
        
        bundleItem = klass(self.uuidgen(), self, bundle)
        bundleItem.load(bundleAttributes)
        
        bundleItem.addSource(namespace.name, bundleItem.createSourcePath(bundle.sourcePath(namespace.name)))
        self.saveManagedObject(bundleItem, namespace)
        
        bundleItem = self.addBundleItem(bundleItem)
        self.addManagedObject(bundleItem)
        return bundleItem

    def readBundleItem(self, **attrs):
        """Retorna un bundle item por sus atributos"""
        items = self.findBundleItems(**attrs)
        if len(items) > 1:
            raise Exception("More than one bundle item")
        return items[0]

    def getBundleItem(self, uuid):
        return self.getManagedObject(uuid)
    
    def ensureBundleItemIsSafe(self, bundleItem, namespace):
        """Ensure the bundle item is safe"""
        if self.isProtected(bundleItem) and not self.isSafe(bundleItem):
            #Safe Bundle Item
            bundle = self.ensureBundleIsSafe(bundleItem.bundle, namespace)
            path = bundleItem.createSourcePath(bundle.sourcePath(namespace.name))
            bundleItem.addSource(namespace.name, path)
            bundleItem.setCurrentSource(namespace.name)
            self.saveManagedObject(bundleItem, namespace)
            self.logger.debug("Add namespace '%s' in source %s for bundle item." % (namespace.name, bundle.sourcePath(namespace.name)))
        return bundleItem
    
    def updateBundleItem(self, bundleItem, namespaceName, **attrs):
        """Actualiza un bundle item"""
        self.updateBundleItemCacheCoherence(bundleItem, attrs)

        namespace = self.safeNamespace(namespaceName)

        bundleItem = self.ensureBundleItemIsSafe(bundleItem, namespace)
        
        moveSource = not self.isProtected(bundleItem) and "name" in attrs

        # Do update and save
        bundleItem.update(attrs)
        self.saveManagedObject(bundleItem, namespace)
        self.modifyBundleItem(bundleItem)
        if moveSource:
            # Para mover hay que renombrar el item
            bundleItemSourcePath = bundleItem.currentSourcePath()
            bundleItemDestinyPath = bundleItem.createSourcePath(bundleItem.bundle.sourcePath(namespace.name))
            shutil.move(bundleItemSourcePath, bundleItemDestinyPath)
            bundleItem.setSourcePath(namespace.name, bundleItemDestinyPath)
        return bundleItem

    def deleteBundleItem(self, bundleItem):
        """Elimina un bundle por su uuid,
        si el bundle es del namespace proteguido no lo elimina sino que lo marca como eliminado
        """
        for namespace in self.namespaces.values():
            if not bundleItem.hasSource(namespace.name):
                continue
            #Si el espacio de nombres es distinto al protegido lo elimino
            if namespace.protected:
                self.setDeleted(bundleItem.uuid)
            else:
                self.deleteManagedObject(bundleItem, namespace)

        self.removeManagedObject(bundleItem)
        self.removeBundleItem(bundleItem)

    # ------------- STATICFILE INTERFACE
    def addStaticFile(self, file):
        return file

    def removeStaticFile(self, file):
        pass

    # -------------- STATICFILE CRUD
    def createStaticFile(self, parentItem, namespaceName=None):
        namespace = self.safeNamespace(namespaceName)
        
        if self.isProtected(parentItem) and not self.isSafe(parentItem):
            self.updateBundleItem(parentItem, namespace)

        path = osextra.path.ensure_not_exists(os.path.join(parentItem.path(namespace), "%s"), osextra.to_valid_name(name))
        staticFile = PMXStaticFile(path, parentItem)
        #No es la mejor forma pero es la forma de guardar el archivo
        staticFile = self.addStaticFile(staticFile)
        parentItem.addStaticFile(staticFile)
        staticFile.save()
        return staticFile

    def updateStaticFile(self, staticFile, namespaceName, **attrs):
        namespace = self.safeNamespace(namespaceName)
        parentItem = staticFile.parentItem
        if self.isProtected(parentItem) and not self.isSafe(parentItem):
            self.updateBundleItem(parentItem, namespace)
        if "name" in attrs:
            path = osextra.path.ensure_not_exists(os.path.join(parentItem.path(namespace), "%s"), osextra.to_valid_name(attrs["name"]))
            staticFile.relocate(path)
        staticFile.update(attrs)
        self.modifyBundleItem(staticFile)
        return staticFile

    def deleteStaticFile(self, staticFile):
        parentItem = staticFile.parentItem
        if self.isProtected(parentItem) and not self.isSafe(parentItem):
            self.deleteBundleItem(parentItem)
        self.removeStaticFile(staticFile)

    # ------------- THEME INTERFACE
    def addTheme(self, theme):
        return theme

    def modifyTheme(self, theme):
        pass

    def removeTheme(self, theme):
        pass

    def getAllThemes(self):
        return []

    # ------------------ THEME CRUD
    def findThemes(self, **attrs):
        """
        Retorna todos los themes que complan las condiciones en attrs
        """
        items = []
        for item in self.getAllThemes():
            if compare(item, list(attrs.keys()), attrs):
                items.append(item)
        return items

    def createTheme(self, namespaceName = None, **attrs):
        namespace = self.safeNamespace(namespaceName)
        
        themeAttributes = PMXTheme.DEFAULTS.copy()
        themeAttributes.update(attrs)
        
        # Create Bundle
        theme = PMXTheme(self.uuidgen(), self)
        theme.load(themeAttributes)
        theme.addSource(namespace.name, theme.createSourcePath(namespace.themes))
        
        self.saveManagedObject(theme, namespace)
        
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

    def ensureThemeIsSafe(self, theme, namespace):
        """Ensure the theme is safe"""
        if self.isProtected(theme) and not self.isSafe(theme):
            #Safe theme
            theme.addSource(namespace.name, theme.createSourcePath(namespace.themes))
            theme.setCurrentSource(namespace.name)
            self.saveManagedObject(theme, namespace)
            self.logger.debug("Add namespace '%s' in source %s for theme." % (namespace.name, theme.sourcePath(namespace.name)))
        return theme
        
    def updateTheme(self, theme, namespaceName = None, **attrs):
        """Actualiza un themes"""
        namespace = self.safeNamespace(namespaceName)
        
        theme = self.ensureThemeIsSafe(theme, namespace)

        moveSource = not self.isProtected(theme) and "name" in attrs
        
        # Do update and save
        theme.update(attrs)
        self.saveManagedObject(theme, namespace)
        self.modifyTheme(theme)
        if moveSource:
            pass
            #path = osextra.path.ensure_not_exists(os.path.join(os.path.dirname(theme.path(namespace)), "%s.tmTheme"), osextra.to_valid_name(attrs["name"]))
            #theme.relocateSource(namespace, path)
        return theme

    def deleteTheme(self, theme):
        """Elimina un theme por su uuid"""
        
        for namespace in self.namespaces.values():
            if not theme.hasSource(namespace.name):
                continue
            #Si el espacio de nombres es distinto al protegido lo elimino
            if namespace.protected:
                self.setDeleted(theme.uuid)
            else:
                self.deleteManagedObject(theme, namespace)
        self.removeManagedObject(theme)
        self.removeTheme(bundle)

    # ----------------- THEMESTYLE INTERFACE
    def addThemeStyle(self, style):
        return style

    def removeThemeStyle(self, style):
        pass

    # ------------ THEMESTYLE CRUD
    def createThemeStyle(self, theme, namespaceName = None, **attrs):
        namespace = self.safeNamespace(namespaceName)
        
        theme = self.ensureThemeIsSafe(theme, namespace)
        
        style = theme.createThemeStyle(attrs)

        # Do update and save
        self.saveManagedObject(theme, namespace)
        return style

    def updateThemeStyle(self, style, namespaceName = None, **attrs):
        namespace = self.safeNamespace(namespaceName)
        
        theme = self.ensureThemeIsSafe(style.theme, namespace)
        
        # Do update and save
        style.update(attrs)
        self.saveManagedObject(theme, namespace)
        self.modifyTheme(theme)
        return style

    def deleteThemeStyle(self, style, namespaceName = None):
        namespace = self.safeNamespace(namespaceName)
        
        theme = self.ensureThemeIsSafe(style.theme, namespace)
        theme.removeThemeStyle(style)
        self.saveManagedObject(theme, namespace)
        self.removeThemeStyle(style)

    # ----------- PREFERENCES INTERFACE
    def getAllPreferences(self):
        """Return a list of all preferences bundle items"""
        raise NotImplementedError

    #----------------- PREFERENCES ---------------------
    def getPreferences(self, leftScope, rightScope = None):
        memoizedKey = ("getPreferences", None, leftScope, rightScope)
        if memoizedKey in self.bundleItemCache:
            return self.bundleItemCache.get(memoizedKey)
        return self.bundleItemCache.setdefault(memoizedKey,
            self.__sort_filter_items(self.getAllPreferences(), leftScope, rightScope))

    def getPreferenceSettings(self, leftScope, rightScope = None):
        memoizedKey = ("getPreferenceSettings", None, leftScope, rightScope)
        if memoizedKey in self.bundleItemCache:
            return self.bundleItemCache.get(memoizedKey)
        return self.bundleItemCache.setdefault(memoizedKey,
            bundleitem.PMXPreference.buildSettings(self.getPreferences(leftScope, rightScope)))

    # ----------------- TABTRIGGERS INTERFACE
    def getAllTabTriggerItems(self):
        """Return a list of all tab triggers items"""
        raise NotImplementedError

    def getAllBundleItemsByTabTrigger(self, tabTrigger):
        """Return a list of tab triggers bundle items"""
        raise NotImplementedError

    # --------------- TABTRIGGERS
    def getAllTabTriggerSymbols(self):
        memoizedKey = ("getAllTabTriggerSymbols", None, None, None)
        if memoizedKey in self.bundleItemCache:
            return self.bundleItemCache.get(memoizedKey)
        return self.bundleItemCache.setdefault(memoizedKey,
            [ item.tabTrigger for item in self.getAllTabTriggerItems() ])

    def getTabTriggerSymbol(self, line, index):
        line = line[:index][::-1]
        search = [(tabTrigger, line.find(tabTrigger[::-1]), len(tabTrigger)) for tabTrigger in self.getAllTabTriggerSymbols()]
        search = [trigger_value_length for trigger_value_length in search if trigger_value_length[1] == 0]
        if search:
            best = ("", 0)
            for trigger, value, length in search:
                if length > best[1]:
                    best = (trigger, length)
            return best[0]

    def getAllTabTiggerItemsByScope(self, leftScope, rightScope = None):
        memoizedKey = ("getAllTabTiggerItemsByScope", None, leftScope, rightScope)
        if memoizedKey in self.bundleItemCache:
            return self.bundleItemCache.get(memoizedKey)
        return self.bundleItemCache.setdefault(memoizedKey,
            self.__sort_filter_items(self.getAllTabTriggerItems(), leftScope, rightScope))

    def getTabTriggerItem(self, tabTrigger, leftScope, rightScope):
        memoizedKey = ("getTabTriggerItem", tabTrigger, leftScope, rightScope)
        if memoizedKey in self.bundleItemCache:
            return self.bundleItemCache.get(memoizedKey)
        return self.bundleItemCache.setdefault(memoizedKey,
            self.__sort_filter_items(self.getAllBundleItemsByTabTrigger(tabTrigger), leftScope, rightScope))

    # -------------- KEYEQUIVALENT INTERFACE
    def getAllKeyEquivalentItems(self):
        """
        Return a list of all key equivalent items
        """
        raise NotImplementedError

    def getAllBundleItemsByKeyEquivalent(self, keyCode):
        """Return a list of key equivalent bundle items"""
        raise NotImplementedError

    #-------------- KEYEQUIVALENT ------------------------
    def getAllKeyEquivalentCodes(self):
        # TODO En este nivel no se como estan implementados los codes no puedo llamar a keySequence
        memoizedKey = ("getAllKeyEquivalentCodes", None, None, None)
        if memoizedKey in self.bundleItemCache:
            return self.bundleItemCache.get(memoizedKey)
        return self.bundleItemCache.setdefault(memoizedKey,
            [item.keySequence() for item in self.getAllKeyEquivalentItems()])

    def getKeyEquivalentItem(self, keyCode, leftScope, rightScope):
        memoizedKey = ("getKeyEquivalentItem", keyCode, leftScope, rightScope)
        if memoizedKey in self.bundleItemCache:
            return self.bundleItemCache.get(memoizedKey)
        return self.bundleItemCache.setdefault(memoizedKey,
            self.__sort_filter_items(self.getAllBundleItemsByKeyEquivalent(keyCode), leftScope, rightScope))

    # --------------- FILE EXTENSION INTERFACE
    def getAllBundleItemsByFileExtension(self, path):
        """
        Return a list of file extension bundle items
        """
        raise NotImplementedError

    #------------- FILE EXTENSION, for drag commands -------------------------
    def getFileExtensionItem(self, path, scope):
        return self.__sort_filter_items(self.getAllBundleItemsByFileExtension(path), scope)

    # ------------- ACTION ITEMS INTERFACE
    def getAllActionItems(self):
        """
        Return action items
        """
        raise NotImplementedError

    #---------------- ACTION ITEMS FOR SCOPE ---------------------------------
    def getActionItemsByScope(self, leftScope, rightScope):
        """Return a list of actions items for scope"""
        memoizedKey = ("getActionItemsByScope", None, leftScope, rightScope)
        if memoizedKey in self.bundleItemCache:
            return self.bundleItemCache.get(memoizedKey)
        return self.bundleItemCache.setdefault(memoizedKey,
            self.__sort_filter_items(self.getAllActionItems(), leftScope, rightScope))

    # ------------------ SYNTAXES INTERFACE
    def getAllSyntaxes(self):
        raise NotImplementedError

    # ------------------ SYNTAXES
    def getSyntaxesAsDictionary(self):
        memoizedKey = ("getSyntaxesAsDictionary", None, None, None)
        if memoizedKey in self.bundleItemCache:
            return self.bundleItemCache.get(memoizedKey)
        return self.bundleItemCache.setdefault(memoizedKey,
            dict([(syntax.scopeName, syntax) for syntax in self.getAllSyntaxes()]))

    def getSyntaxes(self, sort=False):
        stxs = []
        for syntax in self.getAllSyntaxes():
            stxs.append(syntax)
        if sort:
            return sorted(stxs, key=lambda s: s.name)
        return stxs

    def getSyntaxesByScope(self, leftScope, rightScope = None):
        memoizedKey = ("getSyntaxesByScope", None, leftScope, rightScope)
        if memoizedKey in self.bundleItemCache:
            return self.bundleItemCache.get(memoizedKey)
        return self.bundleItemCache.setdefault(memoizedKey,
            self.__sort_filter_items(self.getAllSyntaxes(), leftScope, rightScope))
        
    def findSyntaxByFirstLine(self, line):
        for syntax in self.getAllSyntaxes():
            if syntax.firstLineMatch != None and syntax.firstLineMatch.search(line):
                return syntax

    def findSyntaxByFileType(self, fileType):
        for syntax in self.getAllSyntaxes():
            if syntax.fileTypes is not None and any([fileType == "%s" % ft for ft in syntax.fileTypes]):
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

    # --------------- BUNDLE INTERFACE
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
        return list(self.BUNDLES.values())

    # ----------------- BUNDLEITEM INTERFACE
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
        return list(self.BUNDLE_ITEMS.values())

    # -------------- THEME INTERFACE
    def addTheme(self, theme):
        self.THEMES[theme.uuid] = theme
        return theme

    def modifyTheme(self, theme):
        pass

    def removeTheme(self, theme):
        self.THEMES.pop(theme.uuid)

    def getAllThemes(self):
        return list(self.THEMES.values())

    # ------------ PREFERENCES INTERFACE
    def getAllPreferences(self):
        '''
            Return all preferences
        '''
        return self.PREFERENCES

    # ---------------- TABTRIGGERS INTERFACE
    def getAllTabTriggerSymbols(self):
        """
        Return a list of tab triggers
        ['class', 'def', ...]
        """
        return list(self.TAB_TRIGGERS.keys())

    def getAllBundleItemsByTabTrigger(self, tabTrigger):
        """
        Return a list of tab triggers bundle items
        """
        if tabTrigger not in self.TAB_TRIGGERS:
            return []
        return self.TAB_TRIGGERS[tabTrigger]

    # --------------- KEYEQUIVALENT INTERFACE
    def getAllBundleItemsByKeyEquivalent(self, keyEquivalent):
        """
        Return a list of key equivalent bundle items
        """
        if keyEquivalent not in self.KEY_EQUIVALENTS:
            return []
        return self.KEY_EQUIVALENTS[keyEquivalent]

    # -------------- SYNTAXES
    def getSyntaxesAsDictionary(self):
        return self.SYNTAXES

    def getSyntaxes(self, sort=False):
        stxs = []
        for syntax in list(self.SYNTAXES.values()):
            stxs.append(syntax)
        if sort:
            return sorted(stxs, key=lambda s: s.name)
        return stxs

    def getSyntaxByScopeName(self, scope):
        if scope in self.SYNTAXES:
            return self.SYNTAXES[scope]
        return None

    def findSyntaxByFirstLine(self, line):
        for syntax in list(self.SYNTAXES.values()):
            if syntax.firstLineMatch != None and syntax.firstLineMatch.search(line):
                return syntax
