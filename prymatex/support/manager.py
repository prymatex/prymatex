#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import string
import unicodedata
import hashlib
import uuid as uuidmodule
import subprocess
from glob import glob

from prymatex.support.bundle import PMXBundle, PMXStaticFile
from prymatex.support.macro import PMXMacro
from prymatex.support.syntax import PMXSyntax
from prymatex.support.snippet import PMXSnippet
from prymatex.support.preference import PMXPreference
from prymatex.support.command import PMXCommand, PMXDragCommand
from prymatex.support.template import PMXTemplate
from prymatex.support.project import PMXProject
from prymatex.support.theme import PMXTheme, PMXThemeStyle
from prymatex.support.utils import ensurePath
from prymatex.support import scope

from prymatex.utils import plist

from functools import reduce

BUNDLEITEM_CLASSES = [PMXSyntax, PMXSnippet, PMXMacro, PMXCommand, 
                        PMXPreference, PMXTemplate, PMXDragCommand, PMXProject]

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
    BUNDLES_NAME = 'Bundles'
    SUPPORT_NAME = 'Support'
    THEMES_NAME = 'Themes'
    ELEMENTS = [ BUNDLES_NAME, SUPPORT_NAME, THEMES_NAME ]
    VAR_PREFIX = 'PMX'
    PROTECTEDNS = 0  # El primero es el protected
    DEFAULTNS = 1  # El segundo es el default
    VALID_PATH_CARACTERS = "-_.() %s%s" % (string.ascii_letters, string.digits)

    SETTINGS_CACHE = {}

    def __init__(self):
        self.namespaces = {}
        self.nsorder = []

        self.ready = False
        self.environment = {}
        self.managedObjects = {}

        # Cache!!
        self.bundleItemCache = self.buildBundleItemStorage()
        self.plistFileCache = self.buildPlistFileStorage()
    
    # ------------ Namespaces ----------------------
    def addNamespace(self, name, path):
        # TODO: Quiza migrar a algo con mas forma para encapsular los namespace
        self.namespaces[name] = {"dirname": path}
        self.nsorder.append(name)
        for element in self.ELEMENTS:
            elementPath = os.path.join(path, element)
            if not os.path.exists(elementPath):
                continue
            self.addNamespaceElement(name, element, elementPath)
        return name

    def addNamespaceElement(self, namespace, element, path):
        if namespace == self.protectedNamespace:
            # Es el protected namespace ?
            var = "_".join([self.VAR_PREFIX, element.upper(), 'PATH'])
        else:
            var = "_".join([self.VAR_PREFIX, namespace.upper(), element.upper(), 'PATH'])
        self.namespaces[namespace][element] = self.environment[var] = path

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

    @property
    def safeNamespaces(self):
        return self.nsorder[self.DEFAULTNS:][:]

    def addProjectNamespace(self, project):
        #TODO: Asegurar que no esta ya cargado eso del md5 es medio trucho
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

    #-------------- Environment ---------------------
    def environmentVariables(self):
        return self.environment.copy()

    def addToEnvironment(self, name, value):
        self.environment[name] = value

    def updateEnvironment(self, env):
        self.environment.update(env)

    def projectEnvironment(self, project):
        assert hasattr(project, 'namespace'), "El proyecto no tienen namespace"
        namespace = project.namespace
        env = {}
        for element in self.ELEMENTS:
            key = "_".join([self.VAR_PREFIX, "PROJECT", element.upper(), 'PATH'])
            path, exists = self.namespaceElementPath(namespace, element)
            if exists:
                env[key] = path
        return env

    #----------- Paths for namespaces --------------------
    def namespaceElementPath(self, namespace, element, create = False):
        assert namespace in self.namespaces, "The %s namespace is not registered" % namespace
        assert element in self.ELEMENTS, "The %s namespace is not registered" % namespace
        path = os.path.join(self.namespaces[namespace]["dirname"], element)
        if element not in self.namespaces[namespace] and create:
            # TODO Usar el del fileManager
            os.makedirs(path)
            self.addNamespaceElement(namespace, element, path)
        return path, os.path.exists(path)

    #--------------- Plist --------------------
    def readPlist(self, path):
        if path in self.plistFileCache:
            return self.plistFileCache.get(path)
        return self.plistFileCache.setdefault(path, plist.readPlist(path))
        
    def writePlist(self, hashData, path):
        self.plistFileCache.set(path, hashData)
        return plist.writePlist(hashData, path)

    #--------------- Tools --------------------
    def uuidgen(self, uuid=None):
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
        for char in unicodedata.normalize('NFKD', str(name)).encode('ASCII', 'ignore'):
            char = char if char in self.VALID_PATH_CARACTERS else '-'
            validPath.append(char)
        return ''.join(validPath)

    def runProcess(self, context, callback):
        """Synchronous run process"""
        origWD = os.getcwd()  # remember our original working directory
        if context.workingDirectory is not None:
            os.chdir(context.workingDirectory)

        context.process = subprocess.Popen(context.shellCommand, 
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, env=context.environment)

        if context.inputType is not None:
            context.process.stdin.write(str(context.inputValue).encode("utf-8"))
        context.process.stdin.close()
        try:
            context.outputValue = context.process.stdout.read()
            context.errorValue = context.process.stderr.read()
        except IOError as e:
            context.errorValue = str(e).decode("utf-8")
        context.process.stdout.close()
        context.process.stderr.close()
        context.outputType = context.process.wait()

        if context.workingDirectory is not None:
            os.chdir(origWD)

        callback(context)

    def buildAdHocCommand(self, commandScript, bundle, name=None, commandInput="none", commandOutput="insertText"):
        commandHash = {'command': commandScript,
                       'input': commandInput,
                       'output': commandOutput}
        commandHash['name'] = name if name is not None else "Ad-Hoc command %s" % commandScript

        command = PMXCommand(self.uuidgen())
        command.load(commandHash)
        command.setBundle(bundle)
        command.setManager(self)
        return command

    def buildAdHocSnippet(self, snippetContent, bundle, name=None, tabTrigger=None):
        snippetHash = {'content': snippetContent,
                       'tabTrigger': tabTrigger}
        snippetHash['name'] = name if name is not None else "Ad-Hoc snippet"
        snippet = PMXSnippet(self.uuidgen())
        snippet.load(snippetHash)
        snippet.setBundle(bundle)
        snippet.setManager(self)
        return snippet

    #--------------- Scopes and selectors --------------
    def createScopeSelector(self, scopeSelector):
        return scope.Selector(scopeSelector)
        
    def __sort_filter_items(self, items, leftScope, rightScope = None):
        context = scope.Context.get(leftScope, rightScope)
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
        for ns in self.nsorder[::-1]:
            self.loadThemes(ns)
            self.loadBundles(ns)
        for bundle in self.getAllBundles():
            if bundle.enabled:
                self.populateBundle(bundle)
        # Uninstall message handler
        self.messageHandler = None
        self.ready = True

    #-------------- LOAD THEMES ---------------------------
    def loadThemes(self, namespace):
        loadedThemes = set()
        if self.THEMES_NAME in self.namespaces[namespace]:
            themePaths = glob(os.path.join(self.namespaces[namespace][self.THEMES_NAME], '*.tmTheme'))
            for themePath in themePaths:
                try:
                    theme = self.loadTheme(themePath, namespace)
                    self.showMessage("Loading theme\n%s" % theme.name)
                    loadedThemes.add(theme)
                except Exception as ex:
                    import traceback
                    print("Error in laod theme %s (%s)" % (themePath, ex))
                    traceback.print_exc()
        return loadedThemes

    def loadTheme(self, themePath, namespace):
        data = self.readPlist(PMXTheme.dataFilePath(themePath))
        uuid = self.uuidgen(data.pop('uuid', None))
        theme = self.getManagedObject(uuid)
        if not (theme or self.isDeleted(uuid)):
            theme = PMXTheme(uuid)
            theme.load(data)
            theme.setManager(self)
            theme.addSource(namespace, themePath)
            theme = self.addTheme(theme)
            settings = data.pop('settings', [])
            if settings:
                theme.setDefaultSettings(settings.pop(0)["settings"])
            for setting in settings:
                style = PMXThemeStyle(setting, theme)
                style = self.addThemeStyle(style)
                theme.styles.append(style)
            self.addManagedObject(theme)
        elif theme:
            theme.addSource(namespace, themePath)
        return theme

    #------------- LOAD BUNDLES ------------------
    def loadBundles(self, namespace):
        loadedBundles = set()
        if self.BUNDLES_NAME in self.namespaces[namespace]:
            bundle_directories = glob(os.path.join(self.namespaces[namespace][self.BUNDLES_NAME], '*.tmbundle'))
            for bundle_dir in bundle_directories:
                try:
                    bundle = self.loadBundle(bundle_dir, namespace)
                    loadedBundles.add(bundle)
                except Exception as ex:
                    import traceback
                    print("Error in laod bundle %s (%s)" % (bundle_dir, ex))
                    traceback.print_exc()
        return loadedBundles

    def loadBundle(self, bundle_dir, namespace):
        data = self.readPlist(PMXBundle.dataFilePath(bundle_dir))
        uuid = self.uuidgen(data.pop('uuid', None))
        bundle = self.getManagedObject(uuid)
        if bundle is None and not self.isDeleted(uuid):
            bundle = PMXBundle(uuid)
            bundle.load(data)
            bundle.setManager(self)
            bundle.addSource(namespace, bundle_dir)
            bundle = self.addBundle(bundle)
            self.addManagedObject(bundle)
        elif bundle is not None:
            bundle.addSource(namespace, bundle_dir)
        return bundle

    # ----------- POPULATE BUNDLE AND LOAD BUNDLE ITEMS
    def populateBundle(self, bundle):
        nss = bundle.namespaces[::-1]
        for namespace in nss:
            bpath = bundle.path(namespace)
            # Search for support
            supportPath = os.path.join(bpath, self.SUPPORT_NAME)
            if not bundle.hasSupportPath() and os.path.exists(supportPath):
                bundle.setSupportPath(supportPath)
            self.showMessage("Populating\n%s" % bundle.name)
            for klass in BUNDLEITEM_CLASSES:
                bundle_item_files = reduce(lambda x, y: x + glob(y), [os.path.join(bpath, klass.FOLDER, file) for file in klass.PATTERNS], [])
                for bundle_item_file in bundle_item_files:
                    try:
                        bundleItem = self.loadBundleItem(klass, bundle_item_file, namespace, bundle)
                        bundleItem.populate()
                    except Exception as e:
                        import traceback
                        print("Error in bundle item %s (%s)" % (bundle_item_file, e))
                        traceback.print_exc()
        bundle.populate()
        self.populatedBundle(bundle)

    def loadBundleItem(self, klass, file_path, namespace, bundle):
        data = self.readPlist(klass.dataFilePath(file_path))
        uuid = self.uuidgen(data.pop('uuid', None))
        bundleItem = self.getManagedObject(uuid)
        if bundleItem is None and not self.isDeleted(uuid):
            bundleItem = klass(uuid)
            bundleItem.load(data)
            bundleItem.setBundle(bundle)
            bundleItem.setManager(self)
            bundleItem.addSource(namespace, file_path)
            bundleItem = self.addBundleItem(bundleItem)
            for staticPath in bundleItem.staticPaths():
                # TODO: Ver que hacer con directorios
                staticFile = PMXStaticFile(staticPath, bundleItem)
                staticFile = self.addStaticFile(staticFile)
                bundleItem.addStaticFile(staticFile)
            self.addManagedObject(bundleItem)
        elif bundleItem is not None:
            bundleItem.addSource(namespace, file_path)
        return bundleItem

    # -------------------- RELOAD SUPPORT
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

    # ------------------ RELOAD THEMES
    def reloadThemes(self, namespace):
        if self.THEMES_NAME in self.namespaces[namespace]:
            installedThemes = [theme for theme in self.getAllThemes() if theme.hasNamespace(namespace)]
            themePaths = glob(os.path.join(self.namespaces[namespace][self.THEMES_NAME], '*.tmTheme'))
            for theme in installedThemes:
                themePath = theme.path(namespace)
                if themePath in themePaths:
                    if namespace == theme.currentNamespace and theme.sourceChanged(namespace):
                        # Remove all styles
                        for style in theme.styles:
                            theme.removeThemeStyle(style)
                        self.logger.debug("Theme %s changed, reload from %s." % (theme.name, themePath))
                        data = self.readPlist(PMXBundle.dataFilePath(themePath))
                        bundle.load(data)
                        settings = data.pop('settings', [])
                        if settings:
                            theme.setDefaultSettings(settings.pop(0)["settings"])
                        for setting in settings:
                            style = PMXThemeStyle(setting, theme)
                            style = self.addThemeStyle(style)
                            theme.styles.append(style)
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
                self.loadTheme(path, namespace)

    # ---------------- RELOAD BUNDLES
    def reloadBundles(self, namespace):
        if self.BUNDLES_NAME in self.namespaces[namespace]:
            installedBundles = [theme for theme in self.getAllBundles() if theme.hasNamespace(namespace)]
            bundlePaths = glob(os.path.join(self.namespaces[namespace][self.BUNDLES_NAME], '*.tmbundle'))
            for bundle in installedBundles:
                bundlePath = bundle.path(namespace)
                if bundlePath in bundlePaths:
                    if namespace == bundle.currentNamespace and bundle.sourceChanged(namespace):
                        self.logger.debug("Bundle %s changed, reload from %s." % (bundle.name, bundlePath))
                        data = self.readPlist(PMXBundle.dataFilePath(bundlePath))
                        bundle.load(data)
                        bundle.updateMtime(namespace)
                        self.modifyBundle(bundle)
                    bundlePaths.remove(bundlePath)
                else:
                    bundleItems = self.findBundleItems(bundle=bundle)
                    list(map(lambda item: item.removeSource(namespace), bundleItems))
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
            for bundle_dir in bundlePaths:
                self.logger.debug("New bundle %s." % path)
                try:
                    # TODO: Que pasa con los nuevos
                    bundle = self.loadBundle(bundle_dir, namespace)
                except Exception as ex:
                    import traceback
                    print("Error in laod bundle %s (%s)" % (bundle_dir, ex))
                    traceback.print_exc()

    # ----- REPOPULATED BUNDLE AND RELOAD BUNDLE ITEMS
    def repopulateBundle(self, bundle):
        namespaces = bundle.namespaces[::-1]
        bundleItems = self.findBundleItems(bundle=bundle)
        bundle.setSupport(None)
        for namespace in namespaces:
            bpath = bundle.path(namespace)
            # Search for support
            supportPath = os.path.join(bpath, self.SUPPORT_NAME)
            if not bundle.hasSupportPath() and os.path.exists(supportPath):
                bundle.setSupport(supportPath)
            bundleItemPaths = {}
            for klass in BUNDLEITEM_CLASSES:
                klassPaths = reduce(lambda x, y: x + glob(y), [os.path.join(bpath, klass.FOLDER, file) for file in klass.PATTERNS], [])
                bundleItemPaths.update(dict([(path, klass) for path in klassPaths]))
            for bundleItem in bundleItems:
                if not bundleItem.hasNamespace(namespace):
                    continue
                bundleItemPath = bundleItem.path(namespace)
                if bundleItemPath in bundleItemPaths:
                    if namespace == bundleItem.currentNamespace and bundleItem.sourceChanged(namespace):
                        for staticFile in bundleItem.statics:
                            bundleItem.removeStaticFile(staticFile)
                        self.logger.debug("Bundle Item %s changed, reload from %s." % (bundleItem.name, bundleItemPath))
                        data = self.readPlist(self.dataFilePath(bundleItemPath))
                        bundleItem.load(data)
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
            for bundle_item_file, klass in bundleItemPaths.items():
                self.logger.debug("New bundle item %s." % path)
                try:
                    item = self.loadBundleItem(klass, bundle_item_file, namespace, bundle)
                    item.populate()
                except Exception as e:
                    import traceback
                    print("Error in bundle item %s (%s)" % (path, e))
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
        testPreference = bool(PMXPreference.TYPE == bundleItem.TYPE)

        scopeSelectorItem = testScope and scope.Selector(bundleItem.scope) or None
        scopeSelectorAttr = testScope and scope.Selector(attrs['scope']) or None
        
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

    def addManagedObject(self, obj):
        self.managedObjects[obj.uuid] = obj

    def removeManagedObject(self, obj):
        self.managedObjects.pop(obj.uuid)

    def getManagedObject(self, uuid):
        if not isinstance(uuid, uuidmodule.UUID):
            uuid = uuidmodule.UUID(uuid)
        return self.managedObjects.get(uuid, None)

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
        basePath, _ = self.namespaceElementPath(namespace, self.BUNDLES_NAME, create = True)
        path = ensurePath(os.path.join(basePath, "%s.tmbundle"), self.convertToValidPath(name))
        bundle = PMXBundle(self.uuidgen(), {'name': name})
        bundle.setManager(self)
        bundle.addSource(namespace, path)
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

    def updateBundle(self, bundle, namespace = None, **attrs):
        """Actualiza un bundle"""
        if len(attrs) == 1 and "name" in attrs and attrs["name"] == bundle.name:
            #Updates que no son updates
            return bundle

        namespace = namespace or self.defaultNamespace

        if bundle.isProtected and not bundle.isSafe:
            #Safe bundle
            basePath, _ = self.namespaceElementPath(namespace, self.BUNDLES_NAME, create = True)
            path = os.path.join(basePath, os.path.basename(bundle.path(self.protectedNamespace)))
            bundle.addSource(namespace, path)
            if bundle.hasSupportPath():
                bundle.relocateSupport(os.path.join(path, self.SUPPORT_NAME))
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
        items = []
        for item in self.getAllBundleItems():
            if compare(item, list(attrs.keys()), attrs):
                items.append(item)
        return items

    def createBundleItem(self, name, tipo, bundle, namespace=None):
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
        klass = [c for c in BUNDLEITEM_CLASSES if c.TYPE == tipo]
        if len(klass) != 1:
            raise Exception("No class type for %s" % tipo)
        klass = klass.pop()
        path = os.path.join(bundle.path(namespace), klass.FOLDER, "%s.%s" % (self.convertToValidPath(name), klass.EXTENSION))

        item = klass(self.uuidgen(), {'name': name})
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

    def updateBundleItem(self, item, namespace=None, **attrs):
        """
        Actualiza un bundle item
        """
        print(item, namespace, attrs)
        # TODO Sacar esta porqueria
        if len(attrs) == 1 and "name" in attrs and attrs["name"] == item.name:
            #Updates que no son updates
            return item

        self.updateBundleItemCacheCoherence(item, attrs)

        #TODO: Este paso es importante para obtener el namespace, quiza ponerlo en un metodo para trabajarlo un poco más
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

    # ------------- STATICFILE INTERFACE
    def addStaticFile(self, file):
        return file

    def removeStaticFile(self, file):
        pass

    # -------------- STATICFILE CRUD
    def createStaticFile(self, name, parentItem, namespace=None):
        namespace = namespace or self.defaultNamespace
        if parentItem.isProtected and not parentItem.isSafe:
            self.updateBundleItem(parentItem, namespace)
        path = ensurePath(os.path.join(parentItem.path(namespace), "%s"), self.convertToValidPath(name))
        staticFile = PMXStaticFile(path, parentItem)
        #No es la mejor forma pero es la forma de guardar el archivo
        staticFile = self.addStaticFile(staticFile)
        parentItem.files.append(staticFile)
        staticFile.save()
        return staticFile

    def updateStaticFile(self, staticFile, namespace=None, **attrs):
        namespace = namespace or self.defaultNamespace
        parentItem = staticFile.parentItem
        if parentItem.isProtected and not parentItem.isSafe:
            self.updateBundleItem(parentItem, namespace)
        if "name" in attrs:
            path = ensurePath(os.path.join(parentItem.path(namespace), "%s"), self.convertToValidPath(attrs["name"]))
            staticFile.relocate(path)
        staticFile.update(attrs)
        self.modifyBundleItem(staticFile)
        return staticFile

    def deleteStaticFile(self, staticFile):
        parentItem = staticFile.parentItem
        if parentItem.isProtected and not parentItem.isSafe:
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

    def createTheme(self, name, namespace=None):
        if len(self.nsorder) < 2:
            return None
        if namespace is None:
            namespace = self.defaultNamespace
        path = os.path.join(self.namespaces[namespace][self.THEMES_NAME], "%s.tmTheme" % self.convertToValidPath(name))
        theme = PMXTheme(self.uuidgen(), namespace, {'name': name}, path)
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

    def updateTheme(self, theme, namespace=None, **attrs):
        """
        Actualiza un themes
        """
        namespace = namespace or self.defaultNamespace
        if theme.isProtected and not theme.isSafe:
            path = os.path.join(self.namespaces[namespace][self.THEMES_NAME], os.path.basename(theme.path(self.protectedNamespace)))
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

    # ----------------- THEMESTYLE INTERFACE
    def addThemeStyle(self, style):
        return style

    def removeThemeStyle(self, style):
        pass

    # ------------ THEMESTYLE CRUD
    def createThemeStyle(self, name, scope, theme, namespace=None):
        namespace = namespace or self.defaultNamespace
        if theme.isProtected and not theme.isSafe:
            self.updateTheme(theme, namespace)
        style = PMXThemeStyle({'name': name, 'scope': scope, 'settings': {}}, theme)
        theme.styles.append(style)
        theme.save(namespace)
        theme.updateMtime(namespace)
        style = self.addThemeStyle(style)
        return style

    def updateThemeStyle(self, style, namespace=None, **attrs):
        namespace = namespace or self.defaultNamespace
        theme = style.theme
        if theme.isProtected and not theme.isSafe:
            self.updateTheme(theme, namespace)
        style.update(attrs)
        theme.save(namespace)
        theme.updateMtime(namespace)
        self.modifyTheme(theme)
        return style

    def deleteThemeStyle(self, style, namespace=None):
        namespace = namespace or self.defaultNamespace
        theme = style.theme
        if theme.isProtected and not theme.isSafe:
            self.updateTheme(theme, namespace)
        theme.styles.remove(style)
        theme.save(namespace)
        theme.updateMtime(namespace)
        self.removeThemeStyle(style)

    # ----------- PREFERENCES INTERFACE
    def getAllPreferences(self):
        """
        Return a list of all preferences bundle items
        """
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
            PMXPreference.buildSettings(self.getPreferences(leftScope, rightScope)))

    # ----------------- TABTRIGGERS INTERFACE
    def getAllTabTriggerItems(self):
        """
        Return a list of all tab triggers items
        """
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

    def getAllBundleItemsByKeyEquivalent(self, keyEquivalent):
        """Return a list of key equivalent bundle items"""
        raise NotImplementedError

    #-------------- KEYEQUIVALENT ------------------------
    def getAllKeyEquivalentCodes(self):
        memoizedKey = ("getAllKeyEquivalentCodes", None, None, None)
        if memoizedKey in self.bundleItemCache:
            return self.bundleItemCache.get(memoizedKey)
        return self.bundleItemCache.setdefault(memoizedKey,
            [item.keyEquivalent for item in self.getAllKeyEquivalentItems()])

    def getKeyEquivalentItem(self, code, leftScope, rightScope):
        memoizedKey = ("getKeyEquivalentItem", code, leftScope, rightScope)
        if memoizedKey in self.bundleItemCache:
            return self.bundleItemCache.get(memoizedKey)
        return self.bundleItemCache.setdefault(memoizedKey,
            self.__sort_filter_items(self.getAllBundleItemsByKeyEquivalent(code), leftScope, rightScope))

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
    def getActionItems(self, leftScope, rightScope):
        """Return a list of actions items for scope"""
        return self.__sort_filter_items(self.getAllActionItems(), leftScope, rightScope)

    # ------------------ SYNTAXES INTERFACE
    def getAllSyntaxes(self):
        raise NotImplementedError

    # ------------------ SYNTAXES
    def getSyntaxesAsDictionary(self):
        return dict([(syntax.scopeName, syntax) for syntax in self.getAllSyntaxes()])

    def getSyntaxes(self, sort=False):
        stxs = []
        for syntax in self.getAllSyntaxes():
            stxs.append(syntax)
        if sort:
            return sorted(stxs, key=lambda s: s.name)
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
