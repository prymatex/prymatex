#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import string
import shutil
import uuid as uuidmodule
import subprocess
from functools import reduce

from prymatex.core import config
from prymatex.core import source
from prymatex.utils import configparser
from prymatex.utils import plist, osextra, six
from prymatex.utils import encoding
from prymatex.utils.decorators import printtime, printparams

from .bundle import Bundle
from .properties import Properties
from . import bundleitem
from . import scope
from .staticfile import StaticFile
from .process import RunningContext

# ------- Tool function for compare bundle items by attributes
def compare(obj, keys, tests):
    if not len(keys):
        return True
    key = keys[0]
    value = getattr(obj, key, None)
    if value is None or key not in tests:
        return False
    elif isinstance(value, six.string_types):
        return value.find(tests[key]) != -1 and compare(obj, keys[1:], tests)
    elif isinstance(value, six.integer_types):
        return value == tests[key] and compare(obj, keys[1:], tests)
    else:
        return value == tests[key] and compare(obj, keys[1:], tests)

# ======================================================
# Manager of Bundles, Bundle Items
# This objects contains the basic functions for items handling
# Every set of items lives inside a namespace
# ======================================================
class SupportBaseManager(object):
    BUNDLEITEM_CLASSES = dict([ (cls.type(), cls) for cls in (
        bundleitem.Syntax,
        bundleitem.Snippet,
        bundleitem.Macro,
        bundleitem.Command,
        bundleitem.DragCommand,
        bundleitem.Proxy,
        bundleitem.Preference,
        bundleitem.Template,
        bundleitem.Project,
        bundleitem.Theme
    )])

    SETTINGS_CACHE = {}

    def __init__(self, **kwargs):
        super(SupportBaseManager, self).__init__(**kwargs)
        self.ready = False
        self.environment = {}
        self._managed_objects = {}

        # Cache
        self._configparsers = {}
        self._properties = {}
        self._auxiliaries = {}
        
        # Stored Cache!!
        self.bundleItemCache = self.buildBundleItemStorage()
        self.plistFileCache = self.buildPlistFileStorage()
        
    # ------------ Namespaces ----------------------
    def addNamespace(self, namespace):
        bundles = os.path.join(namespace.path, config.PMX_BUNDLES_NAME)
        # Update environment
        if namespace.name == config.PMX_NS_NAME:
            self.addToEnvironment("PMX_BUNDLES_PATH", bundles)
            self.addToEnvironment("TM_BUNDLES_PATH", bundles)
        else:
            self.addToEnvironment(
                "PMX_%s_BUNDLES_PATH" % namespace.name.upper(),
                bundles
            )
        if self.ready:
            for bundle in self.loadBundles(namespace):
                if bundle.enabled():
                    self.populateBundle(bundle)

    def namespace(self, name):
        pass

    def namespaces(self):
        return []

    #-------------- Environment ---------------------
    def environmentVariables(self):
        return self.environment.copy()

    def addToEnvironment(self, name, value):
        self.environment[name] = value

    def updateEnvironment(self, env):
        self.environment.update(env)

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

    def uuidtotext(self, uuid):
        return six.text_type(uuid).upper()
    
    #--------------- Run system commands --------------------
    def runSystemCommand(self, **attrs):
        """Synchronous run system command"""
        context = RunningContext(**attrs)
        
        origWD = os.getcwd()  # remember our original working directory
        if context.workingDirectory is not None:
            os.chdir(context.workingDirectory)

        context.process = subprocess.Popen(context.scriptFilePath, 
            stdin = subprocess.PIPE, stdout = subprocess.PIPE, 
            stderr = subprocess.PIPE, env = context.scriptFileEnvironment)

        outputValue, errorValue =  context.process.communicate(
            context.inputValue and encoding.to_fs(context.inputValue))
        
        context.outputValue = encoding.from_fs(outputValue)
        context.errorValue = encoding.from_fs(errorValue)
        context.outputType = context.process.returncode

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

        command = bundleitem.Command(self.uuidgen(), self, bundle)
        command.load(commandHash)
        return command

    def buildAdHocSnippet(self, snippetContent, bundle, name=None, tabTrigger=None):
        snippetHash = {'content': snippetContent,
                       'tabTrigger': tabTrigger}
        snippetHash['name'] = name if name is not None else "Ad-Hoc snippet"
        snippet = bundleitem.Snippet(self.uuidgen(), self, bundle)
        snippet.load(snippetHash)
        return snippet

    def buildAdHocSyntax(self, syntax, bundle, name=None):
        syntaxHash = syntax.copy()
        syntaxHash['name'] = name if name is not None else "Ad-Hoc syntax"
        syntax = bundleitem.Syntax(self.uuidgen(), self, bundle)
        syntax.load(syntaxHash)
        return syntax

    #--------------- Scopes selectors and context --------------
    def scopeFactory(self, source):
        return scope.Scope(source)
        
    def selectorFactory(self, selector):
        return scope.Selector(selector)
        
    def contextFactory(self, leftScope, rightScope = None):
        return scope.Context(leftScope, rightScope)

    # ------------------ AUXILIARY SCOPE
    def auxiliaryScope(self, path=""):
        if path in self._auxiliaries:
            return self._auxiliaries[path]
        return self._auxiliaries.setdefault(path, scope.auxiliary(path))
    
    def __filter_items(self, items, leftScope, rightScope=None, sort=True):
        context = self.contextFactory(leftScope, rightScope)
        if not sort:
            return [ item for item in items if item.selector.does_match(context) ]
        sortFilterItems = []
        for item in items:
            rank = []
            if item.selector.does_match(context, rank):
                sortFilterItems.append((rank.pop(), item))
        sortFilterItems.sort(key=lambda t: t[0], reverse=True)
        return [score_item[1] for score_item in sortFilterItems]

    #---------------- Message Handler ----------------
    def showMessage(self, message):
        if self.message_handler is not None:
            self.message_handler(message)

    #------------ LOAD ALL SUPPORT ----------------------------
    def loadSupport(self, message_handler=None):
        # Install message handler
        self.message_handler = message_handler
        for namespace in self.namespaces():
            self.loadBundles(namespace)
        for bundle in self.getAllBundles():
            if bundle.enabled():
                self.populateBundle(bundle)
        # Uninstall message handler
        self.message_handler = None
        self.ready = True

    #------------- LOAD BUNDLES ------------------
    def loadBundles(self, namespace):
        loadedBundles = set()
        for sourceBundlePath in Bundle.sourcePaths(os.path.join(namespace.path, config.PMX_BUNDLES_NAME)):
            try:
                bundle = self.loadBundle(sourceBundlePath, namespace)
                loadedBundles.add(bundle)
            except Exception as ex:
                self.logger().error("Error in laod bundle %s (%s)" % (sourceBundlePath, ex))
        return loadedBundles

    def loadBundle(self, sourceBundlePath, namespace):
        data = self.readPlist(Bundle.dataFilePath(sourceBundlePath))
        uuid = self.uuidgen(data.get('uuid'))
        bundle = self.getManagedObject(uuid)
        if bundle is None:
            bundle = Bundle(uuid, self)
            bundle.load(data)
            bundle = self.addBundle(bundle)
            self.addManagedObject(bundle)
        else:
            bundle.load(data)
        bundle.addSource(namespace.name, sourceBundlePath)
        return bundle

    # ----------- POPULATE BUNDLE AND LOAD BUNDLE ITEMS
    def populateBundle(self, bundle):
        for namespace in self.namespaces():
            if not bundle.hasSource(namespace.name):
                continue
            bundleDirectory = os.path.dirname(bundle.sourcePath(namespace.name))

            self.showMessage("Populating\n%s" % bundle.name)
            for klass in self.BUNDLEITEM_CLASSES.values():
                for sourceBundleItemPath in klass.sourcePaths(bundle.sourcePath(namespace.name)):
                    try:
                        bundleItem = self.loadBundleItem(klass, sourceBundleItemPath, namespace, bundle)
                    except Exception as exc:
                        self.logger().error("Error in bundle item %s (%s)" % (sourceBundleItemPath, exc))
        bundle.setPopulated(True)
        self.populatedBundle(bundle)

    def loadBundleItem(self, klass, sourceBundleItemPath, namespace, bundle):
        data = self.readPlist(klass.dataFilePath(sourceBundleItemPath))
        uuid = self.uuidgen(data.get('uuid'))
        bundleItem = self.getManagedObject(uuid)
        if bundleItem is None:
            bundleItem = klass(uuid, self, bundle)
            bundleItem.load(data)
            bundleItem = self.addBundleItem(bundleItem)
            for staticPath in klass.staticFilePaths(sourceBundleItemPath):
                # TODO: Ver que hacer con directorios
                staticFile = StaticFile(staticPath, bundleItem)
                staticFile = self.addStaticFile(staticFile)
                bundleItem.addStaticFile(staticFile)
            self.addManagedObject(bundleItem)
        else:
            bundleItem.load(data)
        bundleItem.addSource(namespace.name, sourceBundleItemPath)
        return bundleItem

    # -------------------- RELOAD SUPPORT
    def reloadSupport(self, message_handler = None):
        # Reload Implica ver en todos los espacios de nombre instalados por cambios en los items
        # Install message handler
        self.message_handler = message_handler
        self.logger().debug("Begin reload support.")
        for namespace in self.namespaces():
            self.logger().debug("Search in %s, %s." % (namespace.name, os.path.join(namespace.path, config.PMX_BUNDLES_NAME)))
            self.reloadBundles(namespace)
        for bundle in self.getAllBundles():
            if bundle.enabled():
                self.repopulateBundle(bundle)
        # Uninstall message handler
        self.message_handler = None
        self.logger().debug("End reload support.")

    # ---------------- RELOAD BUNDLES
    def reloadBundles(self, namespace):
        installedBundles = [bundle for bundle in self.getAllBundles() if bundle.hasSource(namespace.name)]
        bundlePaths = list(Bundle.sourcePaths(os.path.join(namespace.path, config.PMX_BUNDLES_NAME)))
        for bundle in installedBundles:
            bundlePath = bundle.sourcePath(namespace.name)
            if bundlePath in bundlePaths:
                if namespace.name == bundle.currentSourceName() and bundle.sourceHasChanged(namespace.name):
                    self.loadBundle(bundlePath, namespace)
                    self.modifyBundle(bundle)
                bundlePaths.remove(bundlePath)
            else:
                bundleItems = self.findBundleItems(bundle=bundle)
                for item in bundleItems:
                    item.removeSource(namespace.name)
                bundle.removeSource(namespace)
                if not bundle.hasSources():
                    self.logger().debug("Bundle %s removed." % bundle.name)
                    for item in bundleItems:
                        self.removeManagedObject(item)
                        self.removeBundleItem(item)
                    self.removeManagedObject(bundle)
                    self.removeBundle(bundle)
                else:
                    for item in bundleItems:
                        item.setDirty()
                    bundle.setSupportPath(None)
                    bundle.setDirty()
        for bundlePath in bundlePaths:
            self.logger().debug("New bundle %s." % bundlePath)
            try:
                bundle = self.loadBundle(bundlePath, namespace)
            except Exception as exc:
                self.logger().error("Error in laod bundle %s (%s)" % (bundlePath, exc))

    # ----- REPOPULATED BUNDLE AND RELOAD BUNDLE ITEMS
    def repopulateBundle(self, bundle):
        for namespace in self.namespaces():
            if not bundle.hasSource(namespace.name):
                continue
            bundlePath = bundle.sourcePath(namespace.name)
            bundleItemPaths = { klass.type(): list(klass.sourcePaths(bundlePath)) 
                for klass in self.BUNDLEITEM_CLASSES.values() }
            for bundleItem in self.findBundleItems(bundle=bundle):
                if not bundleItem.hasSource(namespace.name):
                    continue
                bundleItemPath = bundleItem.sourcePath(namespace.name)
                if bundleItemPath in bundleItemPaths[bundleItem.type()]:
                    if namespace.name == bundleItem.currentSourceName() and bundleItem.sourceHasChanged(namespace.name):
                        self.logger().debug("Bundle Item %s changed, reload from %s." % (bundleItem.name, bundleItemPath))
                        self.loadBundleItem(self.BUNDLEITEM_CLASSES[bundleItem.type()], bundleItemPath, namespace, bundle)
                        self.modifyBundleItem(bundleItem)
                    bundleItemPaths[bundleItem.type()].remove(bundleItemPath)
                else:
                    bundleItem.removeSource(namespace.name)
                    if not bundleItem.hasSources():
                        self.logger().debug("Bundle Item %s removed." % bundleItem.name)
                        self.removeManagedObject(bundleItem)
                        self.removeBundleItem(bundleItem)
                    else:
                        bundleItem.setDirty()
            for itemType, itemPaths in bundleItemPaths.items():
                klass = self.BUNDLEITEM_CLASSES[itemType]
                for itemPath in itemPaths:
                    try:
                        self.logger().debug("New bundle item %s." % itemPath)
                        item = self.loadBundleItem(klass, itemPath, namespace, bundle)
                    except Exception as exc:
                        self.logger().error("Error in bundle item %s (%s)" % (itemPath, exc))
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
        testPreference = bool(bundleItem.type() == 'preference')

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
        namespace = self.namespaces()[0]
        print(namespace)
        return obj.hasSource(namespace.name)
        
    def isSafe(self, obj):
        namespace = self.namespaces()[0]
        return obj.currentSourceName() != namespace.name

    def addManagedObject(self, obj):
        self._managed_objects[obj.uuid] = obj

    def removeManagedObject(self, obj):
        self._managed_objects.pop(obj.uuid)

    def getManagedObject(self, uuid):
        if not isinstance(uuid, uuidmodule.UUID):
            uuid = uuidmodule.UUID(uuid)
        if not self.isDeleted(uuid):
            return self._managed_objects.get(uuid, None)

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

    def createBundle(self, ns_name=config.USR_NS_NAME, **attrs):
        """Crea un bundle nuevo lo agrega en los bundles y lo retorna.
        Precondiciones:
            Tenes por lo menos dos espacios de nombre el base o proteguido y
            uno donde generar los nuevos bundles
        """
        namespace = self.namespace(ns_name)
        assert namespace is not None, "No namespace for %s" % ns_name

        bundleAttributes = Bundle.DEFAULTS.copy()
        bundleAttributes.update(attrs)
        
        # Create Bundle
        bundle = Bundle(self.uuidgen(), self)
        bundle.load(bundleAttributes)
        bundle.addSource(namespace.name, bundle.createSourcePath(os.path.join(namespace.path, config.PMX_BUNDLES_NAME)))
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
            bundle.addSource(namespace.name, bundle.createSourcePath(
                os.path.join(namespace.path, config.PMX_BUNDLES_NAME)))
            bundle.setCurrentSource(namespace.name)
            self.saveManagedObject(bundle, namespace)
            self.logger().debug("Add namespace '%s' in source %s for bundle." % (namespace.name, bundle.sourcePath(namespace.name)))
        return bundle

    def updateBundle(self, bundle, ns_name=config.USR_NS_NAME, **attrs):
        """Actualiza un bundle"""
        namespace = self.namespace(ns_name)
        assert namespace is not None, "No namespace for %s" % ns_name

        bundle = self.ensureBundleIsSafe(bundle, namespace)
        
        moveSource = not self.isProtected(bundle) and "name" in attrs
        
        # Do update and save
        bundle.update(attrs)
        self.saveManagedObject(bundle, namespace)
        self.modifyBundle(bundle)
        if moveSource:
            # Para mover hay que renombrar el directorio y mover todos los items del bundle
            bundleSourcePath = bundle.currentSourcePath()
            bundleDestinyPath = bundle.createSourcePath(os.path.join(namespace.path, config.PMX_BUNDLES_NAME))
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

        for namespace in self.namespaces():
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
            if not bundle.isPopulated():
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
    
    def createBundleItem(self, typeName, bundle, ns_name=config.USR_NS_NAME, **attrs):
        """
        Crea un bundle item nuevo lo agrega en los bundle items y lo retorna,
        Precondiciones:
            Tenes por lo menos dos nombres en el espacio de nombres
            El typeName tiene que ser uno de los conocidos
        Toma el ultimo espacio de nombres creado como espacio de nombre por defecto para el bundle item nuevo.
        """
        namespace = self.namespace(ns_name)
        assert namespace is not None, "No namespace for %s" % ns_name
        
        bundle = self.ensureBundleIsSafe(bundle, namespace)

        klass = self.BUNDLEITEM_CLASSES[typeName]
        
        bundleAttributes = klass.DEFAULTS.copy()
        bundleAttributes.update(attrs)
        
        bundleItem = klass(self.uuidgen(), self, bundle)
        bundleItem.load(bundleAttributes)
        
        print(namespace, bundle.sources, bundle.currentSourceName())
        bundleItem.addSource(namespace.name, bundleItem.createSourcePath(
            bundle.sourcePath(namespace.name)))
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
            self.logger().debug("Add namespace '%s' in source %s for bundle item." % (namespace.name, bundle.sourcePath(namespace.name)))
        return bundleItem
    
    def updateBundleItem(self, bundleItem, ns_name=config.USR_NS_NAME, **attrs):
        """Actualiza un bundle item"""
        self.updateBundleItemCacheCoherence(bundleItem, attrs)

        namespace = self.namespace(ns_name)
        assert namespace is not None, "No namespace for %s" % ns_name

        bundleItem = self.ensureBundleItemIsSafe(bundleItem, namespace)
        
        moveSource = not self.isProtected(bundleItem) and "name" in attrs

        # Do update and save
        bundleItem.update(attrs)
        self.saveManagedObject(bundleItem, namespace)
        self.modifyBundleItem(bundleItem)
        if moveSource:
            # Para mover hay que renombrar el item
            bundleItemSourcePath = bundleItem.currentSourcePath()
            bundleItemDestinyPath = bundleItem.createSourcePath(
                bundleItem.bundle.sourcePath(namespace.name))
            print(bundleItemSourcePath, bundleItemDestinyPath)
            shutil.move(bundleItemSourcePath, bundleItemDestinyPath)
            bundleItem.setSourcePath(namespace.name, bundleItemDestinyPath)
        return bundleItem

    def deleteBundleItem(self, bundleItem):
        """Elimina un bundle por su uuid,
        si el bundle es del namespace proteguido no lo elimina sino que lo marca como eliminado
        """
        for namespace in self.namespaces():
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
    def createStaticFile(self, parentItem, ns_name=config.USR_NS_NAME):
        namespace = self.namespace(ns_name)
        assert namespace is not None, "No namespace for %s" % ns_name
        
        if self.isProtected(parentItem) and not self.isSafe(parentItem):
            self.updateBundleItem(parentItem, namespace)

        path = osextra.path.ensure_not_exists(os.path.join(parentItem.path(namespace), "%s"), osextra.to_valid_name(name))
        staticFile = StaticFile(path, parentItem)
        #No es la mejor forma pero es la forma de guardar el archivo
        staticFile = self.addStaticFile(staticFile)
        parentItem.addStaticFile(staticFile)
        staticFile.save()
        return staticFile

    def updateStaticFile(self, staticFile, ns_name=config.USR_NS_NAME, **attrs):
        namespace = self.namespace(ns_name)
        assert namespace is not None, "No namespace for %s" % ns_name

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

    # ----------------- THEMESTYLE INTERFACE
    def addThemeStyle(self, style):
        return style

    def removeThemeStyle(self, style):
        pass

    # ------------ THEMESTYLE CRUD
    def createThemeStyle(self, theme, ns_name=config.USR_NS_NAME, **attrs):
        namespace = self.namespace(ns_name)
        assert namespace is not None, "No namespace for %s" % ns_name
        
        theme = self.ensureBundleItemIsSafe(theme, namespace)
        
        style = theme.createThemeStyle(attrs)

        # Do update and save
        self.saveManagedObject(theme, namespace)
        return style

    def updateThemeStyle(self, style, ns_name=config.USR_NS_NAME, **attrs):
        namespace = self.namespace(ns_name)
        assert namespace is not None, "No namespace for %s" % ns_name
        
        theme = self.ensureBundleItemIsSafe(style.theme, namespace)
        
        # Do update and save
        style.update(attrs)
        self.saveManagedObject(theme, namespace)
        self.modifyBundleItem(theme)
        return style

    def deleteThemeStyle(self, style, ns_name=config.USR_NS_NAME):
        namespace = self.namespace(ns_name)
        assert namespace is not None, "No namespace for %s" % ns_name
        
        theme = self.ensureBundleItemIsSafe(style.theme, namespace)
        theme.removeThemeStyle(style)
        self.saveManagedObject(theme, namespace)
        self.removeThemeStyle(style)

    # ----------- PREFERENCES INTERFACE
    def getAllPreferences(self):
        """Return a list of all preferences bundle items"""
        raise NotImplementedError

    #----------------- PREFERENCES ---------------------
    def getPreferences(self, leftScope=None, rightScope=None):
        memoizedKey = ("getPreferences", None, leftScope, rightScope)
        if memoizedKey in self.bundleItemCache:
            return self.bundleItemCache.get(memoizedKey)
        return self.bundleItemCache.setdefault(memoizedKey,
            self.__filter_items(self.getAllPreferences(), leftScope, rightScope))

    def getPreferenceSettings(self, leftScope = None, rightScope = None):
        # If leftScope == rightScope == None then return base settings
        memoizedKey = ("getPreferenceSettings", None, leftScope, rightScope)
        if memoizedKey in self.bundleItemCache:
            return self.bundleItemCache.get(memoizedKey)
        return self.bundleItemCache.setdefault(memoizedKey,
            bundleitem.Preference.buildSettings(
                [p.settings for p in self.getPreferences(leftScope, rightScope)]
            )
        )

    #----------------- PROPERTIES ---------------------
    def _load_parser(self, directory):
        parser = configparser.ConfigParser()
        parser.optionxform = str
        parser.source = source.Source(directory, 
            os.path.join(directory, config.PMX_PROPERTIES_NAME)
        )
        if parser.source.exists:
            parser.read(parser.source.path) 
        return parser

    def _load_parsers(self, directory):
        if directory not in self._configparsers:
            parsers = []
            parsers.append(self._load_parser(directory))
            if directory not in (os.sep, config.USER_HOME_PATH):
                parsers += self._load_parsers(
                    os.path.dirname(directory)
                )
            elif directory == os.sep:
                parsers += self._load_parsers(config.USER_HOME_PATH)
            self._configparsers[directory] = parsers
        return self._configparsers[directory]

    def propertiesHasChanged(self, directory):
        assert directory in self._configparsers
        return any(
            ( p.source.hasChanged() for p in self._configparsers[directory] )
        )

    def updateProperties(self, directory):
        # Buscar los parsers que este relacionado con el directorio
        parsers = self._configparsers[directory]
        # Filtrar el que cambio
        parser = [ parser for parser in parsers if parser.source.hasChanged() ].pop()
        # Reload parser
        parser.source = source.Source(directory, 
            os.path.join(directory, config.PMX_PROPERTIES_NAME)
        )
        parser.clear()
        if parser.source.exists:
            parser.read(parser.source.path)

        # Remove properties
        print(list(self._properties.keys()), directory)
        self._properties = {
            key: value for (key, value) in self._properties.items() \
            if not (directory == config.USER_HOME_PATH or key.startswith(directory))             
        }
        return parser.source.exists and directory or \
            os.path.join(directory, config.PMX_PROPERTIES_NAME)

    def loadProperties(self, directory):
        parsers = self._load_parsers(directory)
        properties = Properties(self)
        properties.load(parsers)
        properties = self.addProperties(properties)
        return properties

    def getProperties(self, path):
        directory = path if os.path.isdir(path) else os.path.dirname(path)
        if directory not in self._properties:
            self._properties[directory] = self.loadProperties(directory)
        return self._properties[directory]

    def getPropertiesSettings(self, path=None, leftScope=None, rightScope=None):
        self.logger().debug("Loading properties for %s" % path)
        properties = self.getProperties(path or config.USER_HOME_PATH)
        return properties.buildSettings(
            path or config.USER_HOME_PATH,
            self.contextFactory(leftScope, rightScope)
        )

    # --------------- PROPERTIES INTERFACE
    def addProperties(self, properties):
        return properties

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

    def getAllTabTriggerItemsByScope(self, leftScope, rightScope = None):
        memoizedKey = ("getAllTabTriggerItemsByScope", None, leftScope, rightScope)
        if memoizedKey in self.bundleItemCache:
            return self.bundleItemCache.get(memoizedKey)
        return self.bundleItemCache.setdefault(memoizedKey,
            self.__filter_items(self.getAllTabTriggerItems(), leftScope, rightScope))

    def getTabTriggerItem(self, tabTrigger, leftScope, rightScope):
        memoizedKey = ("getTabTriggerItem", tabTrigger, leftScope, rightScope)
        if memoizedKey in self.bundleItemCache:
            return self.bundleItemCache.get(memoizedKey)
        return self.bundleItemCache.setdefault(memoizedKey,
            self.__filter_items(self.getAllBundleItemsByTabTrigger(tabTrigger), leftScope, rightScope))

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
        memoizedKey = ("getAllKeyEquivalentCodes", None, None, None)
        if memoizedKey in self.bundleItemCache:
            return self.bundleItemCache.get(memoizedKey)
        return self.bundleItemCache.setdefault(memoizedKey,
            [item.keyCode() for item in self.getAllKeyEquivalentItems()])

    def getKeyEquivalentItem(self, keyCode, leftScope, rightScope):
        memoizedKey = ("getKeyEquivalentItem", "%s" % keyCode, leftScope, rightScope)
        if memoizedKey in self.bundleItemCache:
            return self.bundleItemCache.get(memoizedKey)
        return self.bundleItemCache.setdefault(memoizedKey,
            self.__filter_items(self.getAllBundleItemsByKeyEquivalent(keyCode), leftScope, rightScope))

    # --------------- FILE EXTENSION INTERFACE
    def getAllBundleItemsByFileExtension(self, path):
        """
        Return a list of file extension bundle items
        """
        raise NotImplementedError

    #------------- FILE EXTENSION, for drag commands -------------------------
    def getFileExtensionItem(self, path, scope):
        return self.__filter_items(self.getAllBundleItemsByFileExtension(path), scope)

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
            self.__filter_items(self.getAllActionItems(), leftScope, rightScope))

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

    def getSyntaxesByScope(self, scope):
        memoizedKey = ("getSyntaxesByScopeName", scope, None, None)
        if memoizedKey in self.bundleItemCache:
            return self.bundleItemCache.get(memoizedKey)
        context = self.contextFactory(scope)
        syntaxes = []
        for syntax in self.getAllSyntaxes():
            rank = []
            if syntax.scopeNameSelector.does_match(context, rank):
                syntaxes.append((rank.pop(), syntax))
        syntaxes.sort(key=lambda t: t[0], reverse = True)
        return self.bundleItemCache.setdefault(memoizedKey, 
            [score_syntax[1] for score_syntax in syntaxes])

    def findSyntaxByFirstLine(self, line):
        for syntax in self.getAllSyntaxes():
            if syntax.firstLineMatch != None and syntax.firstLineMatch.search(line):
                return syntax

    def findSyntaxByFileType(self, fileType):
        for syntax in self.getAllSyntaxes():
            if syntax.fileTypes is not None and any([fileType == "%s" % ft for ft in syntax.fileTypes]):
                return syntax
