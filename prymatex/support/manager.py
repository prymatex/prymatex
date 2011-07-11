#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, string, unicodedata
import uuid as uuidmodule
from os.path import join, basename, dirname, exists

from glob import glob
from prymatex.support.bundle import PMXBundle, PMXBundleItem
from prymatex.support.macro import PMXMacro
from prymatex.support.syntax import PMXSyntax
from prymatex.support.snippet import PMXSnippet
from prymatex.support.preference import PMXPreference
from prymatex.support.command import PMXCommand, PMXDragCommand
from prymatex.support.template import PMXTemplate, PMXTemplateFile
from prymatex.support.theme import PMXTheme, PMXThemeStyle
from prymatex.support.score import PMXScoreManager
from prymatex.support.utils import ensurePath

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

class PMXSupportBaseManager(object):
    ELEMENTS = ['Bundles', 'Support', 'Themes']
    VAR_PREFIX = 'PMX'
    PROTECTEDNS = 0
    DEFAULTNS = -1
    TABTRIGGERSPLITS = (re.compile(r"\s+", re.UNICODE), re.compile(r"\w+", re.UNICODE), re.compile(r"\W+", re.UNICODE), re.compile(r"\W", re.UNICODE))
    VALID_PATH_CARACTERS = "-_.() %s%s" % (string.ascii_letters, string.digits)
    #FIXME: Dudo de la cache en este lugar
    SETTINGS_CACHE = {}
    
    def __init__(self):
        self.namespaces = {}
        # Te first is the name space base, and the last is de default for new bundles and items */
        self.nsorder = []
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
            epath = join(path, element)
            if not exists(epath):
                continue
            #Si es el primero es el protegido
            if len(self.nsorder) == 1:
                var = "_".join([ self.VAR_PREFIX, element.upper(), 'PATH' ])
            else:
                var = "_".join([ self.VAR_PREFIX, name.upper(), element.upper(), 'PATH' ])
            self.namespaces[name][element] = self.environment[var] = epath

    @property
    def protectedNamespace(self):
        return self.nsorder[self.PROTECTEDNS]
        
    @property
    def defaultNamespace(self):
        return self.nsorder[self.DEFAULTNS]

    def updateEnvironment(self, env):
        self.environment.update(env)

    def buildEnvironment(self):
        return self.environment
        
    #---------------------------------------------------
    # Tools
    #---------------------------------------------------
    def uuidgen(self):
        return uuidmodule.uuid1()

    def convertToValidPath(self, name):
        # TODO: ver que el uuid generado no este entre los elementos existentes
        validPath = []
        for char in unicodedata.normalize('NFKD', unicode(name)).encode('ASCII', 'ignore'):
            char = char if char in self.VALID_PATH_CARACTERS else '-'
            validPath.append(char)
        return ''.join(validPath)

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
                PMXTheme.loadTheme(path, namespace, self)

    #---------------------------------------------------
    # LOAD BUNDLES
    #---------------------------------------------------
    def loadBundles(self, namespace):
        if 'Bundles' in self.namespaces[namespace]:
            paths = glob(join(self.namespaces[namespace]['Bundles'], '*.tmbundle'))
            for path in paths:
                PMXBundle.loadBundle(path, namespace, self)

    #---------------------------------------------------
    # POPULATE BUNDLE AND LOAD BUNDLE ITEMS
    #---------------------------------------------------
    def populateBundle(self, bundle):
        nss = bundle.namespaces[::-1]
        for namespace in nss:
            bpath = join(self.namespaces[namespace]['Bundles'], basename(bundle.path))
            # Search for support
            if bundle.support == None and exists(join(bpath, 'Support')):
                bundle.setSupport(join(bpath, 'Support'))
            for klass in BUNDLEITEM_CLASSES:
                files = reduce(lambda x, y: x + glob(y), [ join(bpath, klass.FOLDER, file) for file in klass.PATTERNS ], [])
                for path in files:
                    klass.loadBundleItem(path, namespace, bundle, self)

    #---------------------------------------------------
    # MANAGED OBJECTS INTERFACE
    #---------------------------------------------------
    def setDeleted(self, uuid):
        '''
            Marcar un managed object como eliminado
        '''
        #self.deletedBundles.append(uuid)
        pass
        
    def isDeleted(self, uuid):
        '''
            Marcar un managed object como eliminado
        '''
        #return uuid in self.deletedBundles
        return False

    def isDisabled(self, uuid):
        #return uuid in self.disabledBundles
        return False
        
    def addManagedObject(self, obj):
        obj.setManager(self)
        self.managedObjects[obj.uuid] = obj
        
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
        '''
            Llamado luego de modificar un bundle
        '''
        pass

    def removeBundle(self, bundle):
        '''
            Llamado luego de eliminar un bundle
        '''
        pass

    def getAllBundles(self):
        pass
    
    #---------------------------------------------------
    # BUNDLE CRUD
    #---------------------------------------------------
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
    
    def createBundle(self, name, namespace = None):
        '''
            Crea un bundle nuevo lo agrega en los bundles y lo retorna,
            Precondiciones:
                Tenes por lo menos dos espacios de nombre el base o proteguido y uno donde generar los nuevos bundles
                El nombre tipo Title.
                El nombre no este entre los nombres ya cargados.
            Toma el ultimo espacio de nombres creado como espacio de nombre por defecto para el bundle nuevo.
        '''
        if len(self.nsorder) < 2:
            return None
        if namespace is None: namespace = self.defaultNamespace
        path = join(self.namespaces[namespace]['Bundles'], "%s.tmbundle" % self.convertToValidPath(name))
        bundle = PMXBundle(self.uuidgen(), namespace, { 'name': name }, path)
        bundle = self.addBundle(bundle)
        self.addManagedObject(bundle)
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
        if len(self.nsorder) < 2:
            return None
        if len(attrs) == 1 and "name" in attrs and attrs["name"] == bundle.name:
            #Updates que no son updates
            return bundle
        if bundle.isProtected:
            if not bundle.isSafe:
                namespace = self.defaultNamespace
                attrs["path"] = join(self.namespaces[namespace]['Bundles'], basename(bundle.path))
                bundle.addNamespace(namespace)
        else:
            if "name" in attrs:
                attrs["path"] = ensurePath(join(dirname(bundle.path), "%s.tmbundle"), self.convertToValidPath(attrs["name"]))
                bundle.relocate(attrs["path"])
        bundle.update(attrs)
        bundle.save()
        self.modifyBundle(bundle)
        return bundle
        
    def deleteBundle(self, bundle):
        '''
            Elimina un bundle,
            si el bundle es del namespace proteguido no lo elimina sino que lo marca como eliminado
        '''
        items = self.findBundleItems(bundle = bundle)
        print items
        #Primero los items
        for item in items:
            self.deleteBundleItem(item)
        if bundle.isProtected:
            if bundle.isSafe:
                pass #Eliminar la parte safe
            self.setDeleted(bundle.uuid)
        else:
            bundle.delete()
        self.removeBundle(bundle)
        
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
        pass
        
    #---------------------------------------------------
    # BUNDLEITEM CRUD
    #---------------------------------------------------
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

    def createBundleItem(self, name, tipo, bundle, namespace = None):
        '''
            Crea un bundle item nuevo lo agrega en los bundle items y lo retorna,
            Precondiciones:
                Tenes por lo menos dos nombres en el espacio de nombres
                El tipo tiene que ser uno de los conocidos
            Toma el ultimo espacio de nombres creado como espacio de nombre por defecto para el bundle item nuevo.
        '''
        if len(self.nsorder) < 2:
            return None
        if namespace is None: namespace = self.defaultNamespace
        klass = filter(lambda c: c.TYPE == tipo, BUNDLEITEM_CLASSES)
        if len(klass) != 1:
            raise Exception("No class type for %s" % tipo)
        klass = klass.pop()
        path = join(bundle.path, klass.FOLDER, "%s.%s" % (self.convertToValidPath(name), klass.EXTENSION))

        item = klass(self.uuidgen(), namespace, { 'name': name }, path)
        item.setBundle(bundle)
        item = self.addBundleItem(item)
        self.addManagedObject(item)
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
        if len(self.nsorder) < 2:
            return None
        if len(attrs) == 1 and "name" in attrs and attrs["name"] == item.name:
            #Updates que no son updates
            return item
        if item.bundle.isProtected and not item.bundle.isSafe:
            self.updateBundle(item.bundle)
        if item.isProtected:
            if not item.isSafe:
                namespace = self.defaultNamespace
                attrs["path"] = join(item.bundle.path, item.FOLDER, basename(item.path))
                item.addNamespace(namespace)
        else:
            if "name" in attrs:
                namePattern = "%%s.%s" % item.EXTENSION if item.EXTENSION else "%s"
                attrs["path"] = ensurePath(join(item.bundle.path, item.FOLDER, namePattern), self.convertToValidPath(attrs["name"]))
                item.relocate(attrs["path"])
        item.update(attrs)
        item.save()
        self.modifyBundleItem(item)
        return item
    
    def deleteBundleItem(self, item):
        '''
            Elimina un bundle por su uuid,
            si el bundle es del namespace proteguido no lo elimina sino que lo marca como eliminado
        '''
        #Si el espacio de nombres es distinto al protegido lo elimino
        if item.isProtected:
            if item.isSafe:
                pass #Borrar la parte safe del bundle item
            self.setDeleted(item.uuid)
        else:
            item.delete()
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
    def createTemplateFile(self, name, template):
        if template.isProtected and not template.isSafe:
            self.updateBundleItem(template)
        path = join(template.path, "%s.%s" % (self.convertToValidPath(name), template.extension))
        file = PMXTemplateFile(path, template)
        #No es la mejor forma pero es la forma de guardar el archivo
        file = self.addTemplateFile(file)
        template.files.append(file)
        #template.save()
        return file

    def updateTemplateFile(self, templateFile, **attrs):
        template = templateFile.template
        if template.isProtected and not template.isSafe:
            self.updateBundleItem(template)
        templateFile.update(attrs)
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
        pass
    
    #---------------------------------------------------
    # THEME CRUD
    #---------------------------------------------------
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

    def createTheme(self, name, namespace = None):
        if len(self.nsorder) < 2:
            return None
        if namespace is None: namespace = self.defaultNamespace
        path = join(self.namespaces[namespace]['Themes'], "%s.tmTheme" % self.convertToValidPath(name))
        theme = PMXTheme(self.uuidgen(), namespace, { 'name': name }, path)
        theme = self.addTheme(theme)
        self.addManagedObject(theme)
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
        if theme.isProtected:
            if not theme.isSafe:
                namespace = self.defaultNamespace
                attrs["path"] = join(self.namespaces[namespace]['Themes'], basename(theme.path))
                theme.addNamespace(namespace)
        else:
            if "name" in attrs:
                attrs["path"] = ensurePath(join(dirname(theme.path), "%s.tmTheme"), self.convertToValidPath(attrs["name"]))
                theme.relocate(attrs["path"])
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
        if theme.isProtected:
            if theme.isSafe:
                pass #TODO: Borrar archivos en safe zones
            self.setDeleted(theme.uuid)
        else:
            theme.delete()
    
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
    def createThemeStyle(self, name, scope, theme):
        if theme.isProtected and not theme.isSafe:
            self.updateTheme(theme)
        style = PMXThemeStyle({'name': name, 'scope': scope, 'settings': {}}, theme)
        style = self.addThemeStyle(style)
        theme.styles.append(style)
        theme.save()
        return style

    def updateThemeStyle(self, style, **attrs):
        theme = style.theme
        if theme.isProtected and not theme.isSafe:
            self.updateTheme(theme)
        style.update(attrs)
        theme.save()
        self.modifyTheme(theme)
        return style

    def deleteThemeStyle(self, style):
        theme = style.theme
        if theme.isProtected and not theme.isSafe:
            self.updateTheme(theme)
        theme.styles.remove(style)
        theme.save()
        self.removeThemeStyle(style)
        
    #---------------------------------------------------
    # PREFERENCES INTERFACE
    #---------------------------------------------------
    def getAllPreferences(self):
        '''
            Return a list of preferences bundle items
        '''
        pass
        
    #---------------------------------------------------------------
    # PREFERENCES
    #---------------------------------------------------------------
    def getPreferences(self, scope):
        with_scope = []
        without_scope = []
        for preference in self.getAllPreferences():
            if preference.scope == None:
                without_scope.append(preference)
            else:
                score = self.scores.score(preference.scope, scope)
                if score != 0:
                    with_scope.append((score, preference))
        with_scope.sort(key = lambda t: t[0], reverse = True)
        preferences = map(lambda (score, item): item, with_scope)
        with_scope = []
        for p in preferences:
            with_scope.append(p)
        return with_scope + without_scope

    def getPreferenceSettings(self, scope):
        if scope not in self.SETTINGS_CACHE:
            preferences = self.getPreferences(scope)
            self.SETTINGS_CACHE[scope] = PMXPreference.buildSettings(preferences)
        return self.SETTINGS_CACHE[scope]
    
    #---------------------------------------------------
    # TABTRIGGERS INTERFACE
    #---------------------------------------------------
    def getAllTabTriggersMnemonics(self):
        '''
            Return a list of tab triggers
            ['class', 'def', ...]
        '''
        pass
    
    def getAllBundleItemsByTabTrigger(self, tabTrigger):
        '''
            Return a list of tab triggers bundle items
        '''
        pass
    
    #---------------------------------------------------------------
    # TABTRIGGERS
    #---------------------------------------------------------------
    def getTabTriggerSymbol(self, line, index):
        line = line[:index]
        tiggers = self.getAllTabTriggersMnemonics()
        for tabSplit in self.TABTRIGGERSPLITS:
            matchs = filter(lambda m: m.start() <= index <= m.end(), tabSplit.finditer(line))
            if matchs:
                match = matchs.pop()
                word = line[match.start():match.end()]
                if word in tiggers:
                    return word
    
    def getTabTriggerItem(self, keyword, scope):
        with_scope = []
        without_scope = []
        for item in self.getAllBundleItemsByTabTrigger(keyword):
            if item.scope == None:
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
        '''
            Return a list of key equivalent bundle items
        '''
        pass
        
    #---------------------------------------------------------------
    # KEYEQUIVALENT
    #---------------------------------------------------------------
    def getKeyEquivalentItem(self, code, scope):
        with_scope = []
        without_scope = []
        for item in self.getAllBundleItemsByKeyEquivalent(code):
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

        
class PMXSupportManager(PMXSupportBaseManager):
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
        super(PMXSupportManager, self).__init__()
    
    #---------------------------------------------------
    # BUNDLE INTERFACE
    #---------------------------------------------------
    def addBundle(self, bundle):
        '''
        @param bundle: PMXBundle instance
        '''
        self.BUNDLES[bundle.uuid] = bundle
        return bundle

    def getBundle(self, uuid):
        return self.getManagedObject(uuid)

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

    def getBundleItem(self, uuid):
        return self.getManagedObject(uuid)

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
        
    def getTheme(self, uuid):
        return self.getManagedObject(uuid)

    def modifyTheme(self, theme):
        pass
        
    def removeTheme(self, theme):
        self.THEMES.pop(theme.uuid)

    def hasTheme(self, uuid):
        return uuid in self.THEMES

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
        '''
            Return a list of tab triggers
            ['class', 'def', ...]
        '''
        return self.TAB_TRIGGERS.keys()
    
    def getAllBundleItemsByTabTrigger(self, tabTrigger):
        '''
            Return a list of tab triggers bundle items
        '''
        if tabTrigger not in self.TAB_TRIGGERS:
            return []
        return self.TAB_TRIGGERS[tabTrigger]
    
    #---------------------------------------------------
    # KEYEQUIVALENT INTERFACE
    #---------------------------------------------------
    def getAllBundleItemsByKeyEquivalent(self, keyEquivalent):
        '''
            Return a list of key equivalent bundle items
        '''
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
    
    def findSyntaxByFileType(self, path):
        for syntax in self.SYNTAXES.values():
            if type(syntax.fileTypes) == list:
                for t in syntax.fileTypes:
                    if path.endswith(t):
                        return syntax
