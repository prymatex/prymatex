#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from os.path import join, basename, exists

from glob import glob
from prymatex.support.bundle import PMXBundle, PMXBundleItem
from prymatex.support.macro import PMXMacro
from prymatex.support.syntax import PMXSyntax
from prymatex.support.snippet import PMXSnippet
from prymatex.support.preference import PMXPreference
from prymatex.support.command import PMXCommand, PMXDragCommand
from prymatex.support.template import PMXTemplate
from prymatex.support.theme import PMXTheme
from prymatex.support.score import PMXScoreManager
from prymatex.support.utils import sh

BUNDLEITEM_CLASSES = [ PMXSyntax, PMXSnippet, PMXMacro, PMXCommand, PMXPreference, PMXTemplate, PMXDragCommand ]

def compare(object, attrs, tests):
    if not attrs:
        return True
    attr = getattr(object, attrs[0], None)
    if attr == None or attrs[0] not in tests:
        return True and compare(object, attrs[1:], tests)
    elif isinstance(attr, (str, unicode)):
        return attr.find(tests[attrs[0]]) != -1 and compare(object, attrs[1:], tests)
    elif isinstance(attr, (int)):
        return attr == tests[attrs[0]] and compare(object, attrs[1:], tests)
    else:
        return attr == tests[attrs[0]] and compare(object, attrs[1:], tests)
    
class PMXSupportManager(object):
    ELEMENTS = ['Bundles', 'Support', 'Themes']
    VAR_PREFIX = 'PMX'
    BUNDLES = {}
    BUNDLE_ITEMS = {}
    THEMES = {}
    SYNTAXES = {}
    TAB_TRIGGERS = {}
    KEY_EQUIVALENTS = {}
    DRAGS = []
    PREFERENCES = {}
    TEMPLATES = []
    SETTINGS_CACHE = {}
    TABTRIGGERSPLITS = (re.compile(r"\s+", re.UNICODE), re.compile(r"\w+", re.UNICODE), re.compile(r"\W+", re.UNICODE), re.compile(r"\W", re.UNICODE))
    
    def __init__(self, disabledBundles = [], deletedBundles = []):
        self.namespaces = {}
        # Te first is the name space base, and the last is de default for new bundles and items */
        self.nsorder = []
        self.environment = {}
        self.disabledBundles = disabledBundles
        self.deletedBundles = deletedBundles
        self.scores = PMXScoreManager()
    
    def addNamespace(self, name, path):
        self.namespaces[name] = {}
        self.nsorder.append(name)
        for element in self.ELEMENTS:
            epath = join(path, element)
            if not exists(epath):
                continue
            #Si es el primero es el protegido
            if len(self.nsorder) == 1:
                var = "_".join([ self.VAR_PREFIX, element.upper(), 'PATH' ])
            else:
                var = "_".join([ self.VAR_PREFIX, name.upper(), element.upper(), 'PATH' ])
            self.namespaces[name][element] = self.environment[var] = epath

    def uuidgen(self):
        # TODO: ver que el uuid generado no este entre los elementos existentes
        return sh("uuidgen").strip()

    def updateEnvironment(self, env):
        self.environment.update(env)

    def buildEnvironment(self):
        return self.environment

    #---------------------------------------------------
    # LOAD ALL SUPPORT
    #---------------------------------------------------
    def loadSupport(self, callback = None):
        for ns in self.nsorder[::-1]:
            self.loadThemes(ns)
            self.loadBundles(ns)
        for bundle in self.getAllBundles():
            self.populateBundle(bundle)

    #---------------------------------------------------
    # LOAD THEMES
    #---------------------------------------------------
    def loadThemes(self, namespace):
        if 'Themes' in self.namespaces[namespace]:
            paths = glob(join(self.namespaces[namespace]['Themes'], '*.tmTheme'))
            for path in paths:
                theme = PMXTheme.loadTheme(path, namespace)
                if theme == None:
                    continue
                if not self.hasTheme(theme.uuid):
                    self.addTheme(theme)

    #---------------------------------------------------
    # LOAD BUNDLES
    #---------------------------------------------------
    def loadBundles(self, namespace):
        if 'Bundles' in self.namespaces[namespace]:
            paths = glob(join(self.namespaces[namespace]['Bundles'], '*.tmbundle'))
            for path in paths:
                bundle = PMXBundle.loadBundle(path, namespace)
                if bundle == None:
                    continue
                bundle.disabled = bundle.uuid in self.disabledBundles
                if bundle.uuid not in self.deletedBundles and not self.hasBundle(bundle.uuid):
                    bundle.manager = self
                    self.addBundle(bundle)

    #---------------------------------------------------
    # POPULATE BUNDLE AND LOAD BUNDLE ITEMS
    #---------------------------------------------------
    def populateBundle(self, bundle):
        bns = bundle.namespace
        nss = self.nsorder[::-1]
        index = nss.index(bns)
        for ns in nss[index:]:
            bpath = join(self.namespaces[ns]['Bundles'], basename(bundle.path))
            # Search for support
            if bundle.support == None and exists(join(bpath, 'Support')):
                bundle.support = join(bpath, 'Support')
            for klass in BUNDLEITEM_CLASSES:
                files = reduce(lambda x, y: x + glob(y), [ join(bpath, klass.FOLDER, file) for file in klass.PATTERNS ], [])
                for sf in files:
                    item = klass.loadBundleItem(sf, ns)
                    if item == None:
                        continue
                    if not self.hasBundleItem(item.uuid):
                        item.bundle = bundle
                        self.addBundleItem(item)

    #---------------------------------------------------
    # BUNDLE INTERFACE
    #---------------------------------------------------
    def addBundle(self, bundle):
        '''
        @param bundle: PMXBundle instance
        '''
        self.BUNDLES[bundle.uuid] = bundle

    def getBundle(self, uuid):
        '''
        @return: PMXBundle by UUID
        '''
        return self.BUNDLES[uuid]

    def modifyBundle(self, bundle):
        pass

    def removeBundle(self, bundle):
        '''
        @param bundle: PMXBundle instance
        '''
        self.BUNDLES.pop(bundle.uuid)

    def addDeletedBundle(self, uuid):
        '''
            Perform logical delete
        '''
        self.deletedBundles.append(uuid)
        
    def hasBundle(self, uuid):
        '''
        @return: True if bundle exists
        '''
        return uuid in self.BUNDLES

    def getAllBundles(self):
        '''
        @return: list of PMXBundle instances
        '''
        return self.BUNDLES.values()
    
    def findBundles(self, **attrs):
        '''
            Retorna todos los bundles que cumplan con attrs
        '''
        bundles = []
        keys = PMXBundle.KEYS
        keys.extend([key for key in attrs.keys() if key not in keys])
        for bundle in self.getAllBundles():
            if compare(bundle, keys, attrs):
                bundles.append(bundle)
        return bundles
        
    #---------------------------------------------------
    # BUNDLE CRUD
    #---------------------------------------------------
    def createBundle(self, name, namespace = None):
        '''
            Crea un bundle nuevo lo agrega en los bundles y lo retorna,
            Precondiciones:
                Tenes por lo menos un nombre en el espacio de nombres
                El nombre tipo Title.
                El nombre no este entre los nombres ya cargados.
            Toma el ultimo espacio de nombres creado como espacio de nombre por defecto para el bundle nuevo.
        '''
        namespace = self.nsorder[-1] if namespace == None else namespace
        hash = {    'uuid': self.uuidgen(),
                    'name': name }
        path = join(self.namespaces[namespace]['Bundles'], "%s.tmbundle" % name)
        bundle = PMXBundle(namespace, hash, path)
        self.addBundle(bundle)
        return bundle
    
    def readBundle(self, **attrs):
        '''
            Retorna un bundle por sus atributos
        '''
        bundles = self.findBundles(**attrs)
        if len(bundles) > 1:
            raise Exception("More than one bundle")
        return bundles[0]
        
    def updateBundle(self, bundle, **attrs):
        '''
            Actualiza un bundle
        '''
        if bundle.namespace == self.nsorder[0]:
            #Cambiar de namespace y de path al por defecto para proteger el base
            newns = self.nsorder[-1]
            attrs["namespace"] = newns
            #TODO: escape de los caracteres del file system en el nombre pasado
            name = "%s.tmbundle" % attrs["name"] if "name" in attrs else basename(bundle.path)
            attrs["path"] = join(self.namespaces[newns]['Bundles'], name)
        bundle.update(attrs)
        bundle.save()
        self.modifyBundle(bundle)
        return bundle
        
    def deleteBundle(self, bundle):
        '''
            Elimina un bundle,
            si el bundle es del namespace proteguido no lo elimina sino que lo marca como eliminado
        '''
        self.removeBundle(bundle)
        items = self.findBundleItems(bundle = bundle)
        #Primero los items
        for item in items:
            self.deleteBundleItem(item)
        if bundle.namespace == self.nsorder[0]:
            self.addDeletedBundle(bundle.uuid)
        else:
            bundle.delete()
        
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
            self.PREFERENCES.setdefault(item.scope, []).append(item)
        elif item.TYPE == 'template':
            self.TEMPLATES.append(item)
        elif item.TYPE == 'syntax':
            self.SYNTAXES[item.scopeName] = item
            # puede ser dependiente del namespace ? self.SYNTAXES[item.namespace][item.scopeName] = self

    def getBundleItem(self, uuid):
        return self.BUNDLE_ITEMS[uuid]

    def modifyBundleItem(self, item):
        pass

    def removeBundleItem(self, item):
        self.BUNDLE_ITEMS.pop(item.uuid)
    
    def hasBundleItem(self, uuid):
        '''
        @return: True if PMXBundleItem exists
        '''
        return uuid in self.BUNDLE_ITEMS

    def getAllBundleItems(self):
        return self.BUNDLE_ITEMS.values()
        
    def findBundleItems(self, **attrs):
        '''
            Retorna todos los items que complan las condiciones en attrs
        '''
        items = []
        keys = PMXBundleItem.KEYS
        keys.extend([key for key in attrs.keys() if key not in keys])
        for item in self.getAllBundleItems():
            if compare(item, keys, attrs):
                items.append(item)
        return items

    #---------------------------------------------------
    # BUNDLEITEM CRUD
    #---------------------------------------------------
    def createBundleItem(self, name, tipo, bundle, namespace = None):
        '''
            Crea un bundle item nuevo lo agrega en los bundle items y lo retorna,
            Precondiciones:
                Tenes por lo menos un nombre en el espacio de nombres
                El tipo tiene que ser uno de los conocidos
            Toma el ultimo espacio de nombres creado como espacio de nombre por defecto para el bundle item nuevo.
        '''
        namespace = self.nsorder[-1] if namespace == None else namespace
        hash = {    'uuid': self.uuidgen(),
                    'name': name }
        klass = filter(lambda c: c.TYPE == tipo, BUNDLEITEM_CLASSES)
        if len(klass) != 1:
            raise Exception("No class type for %s" % tipo)
        klass = klass.pop()
        path = join(bundle.path, klass.FOLDER, "%s.%s" % (name, klass.EXTENSION))

        item = klass(namespace, hash, path)
        item.bundle = bundle
        self.addBundleItem(item)
        return item
    
    def readBundleItem(self, **attrs):
        '''
            Retorna un bundle item por sus atributos
        '''
        items = self.findBundleItems(**attrs)
        if len(items) > 1:
            raise Exception("More than one bundle item")
        return items[0]
    
    def updateBundleItem(self, item, **attrs):
        '''
            Actualiza un bundle item
        '''
        if item.bundle.namespace == self.nsorder[0]:
            self.updateBundle(item.bundle)
        if item.namespace == self.nsorder[0]:
            #Cambiar de namespace y de path al por defecto para proteger el base
            newns = self.nsorder[-1]
            attrs["namespace"] = newns
            #TODO: escape de los caracteres del file system en el nombre pasado
            name = ("%s.%s" % attrs["name"], item.__class__.EXTENSION) if "name" in attrs else basename(item.path)
            attrs["path"] = join(item.bundle.path, item.__class__.FOLDER, name)
        item.update(attrs)
        item.save()
        self.modifyBundleItem(item)
        return item
    
    def deleteBundleItem(self, item):
        '''
            Elimina un bundle por su uuid,
            si el bundle es del namespace proteguido no lo elimina sino que lo marca como eliminado
        '''
        self.removeBundleItem(item)
        #Si el espacio de nombres es distinto al protegido lo elimino
        if item.namespace != self.nsorder[0]:
            item.delete()
        
    #---------------------------------------------------
    # THEME INTERFACE
    #---------------------------------------------------
    def addTheme(self, theme):
        self.THEMES[theme.uuid] = theme
        
    def getTheme(self, uuid):
        return self.THEMES[uuid]

    def modifyTheme(self, theme):
        pass
        
    def removeTheme(self, theme):
        self.THEMES.pop(theme.uuid)

    def hasTheme(self, uuid):
        return uuid in self.THEMES

    def getAllThemes(self):
        return self.THEMES.values()
    
    def findThemes(self, **attrs):
        '''
            Retorna todos los themes que complan las condiciones en attrs
        '''
        items = []
        keys = PMXTheme.KEYS
        keys.extend([key for key in attrs.keys() if key not in keys])
        for item in self.getAllThemes():
            if compare(item, keys, attrs):
                items.append(item)
        return items
    #---------------------------------------------------
    # THEME CRUD
    #---------------------------------------------------
    def createTheme(self, name, namespace = None):
        '''
            
        '''
        namespace = self.nsorder[-1] if namespace == None else namespace
        hash = {    'uuid': self.uuidgen(),
                    'name': name }
        theme = PMXTheme(namespace, hash, path)
        self.addTheme(theme)
        return theme
    
    def readTheme(self, **attrs):
        '''
            Retorna un bundle item por sus atributos
        '''
        items = self.findThemes(**attrs)
        if len(items) > 1:
            raise Exception("More than one theme")
        return items[0]
        
    def updateTheme(self, theme, **attrs):
        '''
            Actualiza un themes
        '''
        if not theme.isChanged(attrs): return theme;
        if theme.namespace == self.nsorder[0]:
            #Cambiar de namespace y de path al por defecto para proteger el base
            newns = self.nsorder[-1]
            attrs["namespace"] = newns
            name = "%s.tmTheme" % attrs["name"] if "name" in attrs else basename(theme.path)
            attrs["path"] = join(self.namespaces[newns]['Themes'], name)
        theme.update(attrs)
        theme.save()
        self.modifyTheme(theme)
        return theme
        
    def deleteTheme(self, theme):
        '''
            Elimina un theme por su uuid
        '''
        self.removeTheme(theme)
        #Si el espacio de nombres es distinto al protegido lo elimino
        if theme.namespace != self.nsorder[0]:
            theme.delete()
    
    #---------------------------------------------------
    # TEMPLATES INTERFACE
    #---------------------------------------------------
    def getAllTemplates(self):
        return self.TEMPLATES
    
    #---------------------------------------------------------------
    # PREFERENCES
    #---------------------------------------------------------------
    def getPreferences(self, scope):
        with_scope = []
        without_scope = []
        for key in self.PREFERENCES.keys():
            if key == None:
                without_scope.extend(self.PREFERENCES[key])
            else:
                score = self.scores.score(key, scope)
                if score != 0:
                    with_scope.append((score, self.PREFERENCES[key]))
        with_scope.sort(key = lambda t: t[0], reverse = True)
        preferences = map(lambda (score, item): item, with_scope)
        with_scope = []
        for p in preferences:
            with_scope.extend(p)
        return with_scope and with_scope or without_scope

    def getPreferenceSettings(self, scope):
        if scope not in self.SETTINGS_CACHE:
            preferences = self.getPreferences(scope)
            self.SETTINGS_CACHE[scope] = PMXPreference.buildSettings(preferences)
        return self.SETTINGS_CACHE[scope]
    
    #---------------------------------------------------------------
    # TABTRIGGERS
    #---------------------------------------------------------------
    def getTabTriggerSymbol(self, line, index):
        line = line[:index]
        for tabSplit in self.TABTRIGGERSPLITS:
            matchs = filter(lambda m: m.start() <= index <= m.end(), tabSplit.finditer(line))
            if matchs:
                match = matchs.pop()
                word = line[match.start():match.end()]
                if self.TAB_TRIGGERS.has_key(word):
                    return word
    
    def getTabTriggerItem(self, keyword, scope):
        with_scope = []
        without_scope = []
        if self.TAB_TRIGGERS.has_key(keyword):
            for item in self.TAB_TRIGGERS[keyword]:
                if item.scope == None:
                    without_scope.append(item)
                else:
                    score = self.scores.score(item.scope, scope)
                    if score != 0:
                        with_scope.append((score, item))
            with_scope.sort(key = lambda t: t[0], reverse = True)
            with_scope = map(lambda (score, item): item, with_scope)
        return with_scope and with_scope or without_scope
        
    #---------------------------------------------------------------
    # KEYEQUIVALENT
    #---------------------------------------------------------------
    def getKeyEquivalentItem(self, code, scope):
        with_scope = []
        without_scope = []
        if code in self.KEY_EQUIVALENTS:
            for item in self.KEY_EQUIVALENTS[code]:
                if item.scope == None:
                    without_scope.append(item)
                else:
                    score = self.scores.score(item.scope, scope)
                    if score != 0:
                        with_scope.append((score, item))
            with_scope.sort(key = lambda t: t[0], reverse = True)
            with_scope = map(lambda (score, item): item, with_scope)
        return with_scope and with_scope or without_scope
        
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
    
    def findSyntaxByFileType(self, path):
        for syntax in self.SYNTAXES.values():
            if type(syntax.fileTypes) == list:
                for t in syntax.fileTypes:
                    if path.endswith(t):
                        return syntax
