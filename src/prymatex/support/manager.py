#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from os.path import join, abspath, basename, exists

from glob import glob
from prymatex.support.bundle import PMXBundle, PMXMenuNode
from prymatex.support.macro import PMXMacro
from prymatex.support.syntax import PMXSyntax
from prymatex.support.snippet import PMXSnippet
from prymatex.support.preference import PMXPreference
from prymatex.support.command import PMXCommand, PMXDragCommand
from prymatex.support.template import PMXTemplate
from prymatex.support.theme import PMXTheme
from prymatex.support.qtadapter import buildQTextFormat, buildKeyEquivalentCode
from prymatex.support.score import PMXScoreManager

BUNDLEITEM_CLASSES = [ PMXSyntax, PMXSnippet, PMXMacro, PMXCommand, PMXPreference, PMXTemplate, PMXDragCommand ]
    
class PMXSupportManager(object):
    ELEMENTS = ['Bundles', 'Support', 'Themes']
    DEFAULT = 'prymatex'
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
        self.environment = {}
        self.disabledBundles = disabledBundles
        self.deletedBundles = deletedBundles
        self.scores = PMXScoreManager()
    
    def addNameSpace(self, name, path):
        self.namespaces[name] = {}
        for element in self.ELEMENTS:
            epath = join(path, element)
            if not exists(epath):
                continue
            if name == self.DEFAULT:
                var = "_".join([ self.VAR_PREFIX, element.upper(), 'PATH' ])
            else:
                var = "_".join([ self.VAR_PREFIX, name.upper(), element.upper(), 'PATH' ])
            self.namespaces[name][element] = self.environment[var] = epath
    
    def updateEnvironment(self, env):
        self.environment.update(env)

    @property
    def priority(self):
        ns = self.namespaces.keys()
        ns.remove(self.DEFAULT)
        return ns + [ self.DEFAULT ]
    
    #---------------------------------------------------
    # LOAD ALL SUPPORT
    #---------------------------------------------------
    def loadSupport(self, callback = None):
        for ns in self.priority:
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
                    self.addBundle(bundle)

    #---------------------------------------------------
    # POPULATE BUNDLE AND LOAD BUNDLE ITEMS
    #---------------------------------------------------
    def populateBundle(self, bundle):
        bns = bundle.namespace
        nss = self.priority
        index = nss.index(bns)
        bundle.manager = self
        for ns in nss[index:]:
            bpath = join(self.namespaces[ns]['Bundles'], basename(bundle.path))
            # Search for support
            if bundle.support == None and exists(join(bpath, 'Support')):
                bundle.support = join(bpath, 'Support')
            for klass in BUNDLEITEM_CLASSES:
                files = reduce(lambda x, y: x + glob(y), [ join(bpath, klass.FOLDER, file) for file in klass.FILES ], [])
                for sf in files:
                    item = klass.loadBundleItem(sf, ns)
                    if item == None:
                        continue
                    if not self.hasBundleItem(item.uuid):
                        item.bundle = bundle
                        self.addBundleItem(item)

    def hasBundle(self, uuid):
        return uuid in self.BUNDLES

    def addBundle(self, bundle):
        self.BUNDLES[bundle.uuid] = bundle

    def getBundle(self, uuid):
        return self.BUNDLES[uuid]

    def getAllBundles(self):
        return self.BUNDLES.values()

    def hasBundleItem(self, uuid):
        return uuid in self.BUNDLE_ITEMS
        
    def addBundleItem(self, item):
        self.BUNDLE_ITEMS[item.uuid] = item
        if item.bundle.mainMenu != None:
            item.bundle.mainMenu[item.uuid] = item
        if item.tabTrigger != None:
            self.TAB_TRIGGERS.setdefault(item.tabTrigger, []).append(item)
        if item.keyEquivalent != None:
            keyseq = buildKeyEquivalentCode(item.keyEquivalent)
            self.KEY_EQUIVALENTS.setdefault(keyseq, []).append(item)
        if item.TYPE == 'preference':
            self.PREFERENCES.setdefault(item.scope, []).append(item)
        elif item.TYPE == 'template':
            self.TEMPLATES.append(item)
        elif item.TYPE == 'syntax':
            self.SYNTAXES[item.scopeName] = item
            # puede ser dependiente del namespace ? self.SYNTAXES[item.namespace][item.scopeName] = self

    def getBundleItem(self, uuid):
        return self.BUNDLE_ITEMS[uuid]
    
    def hasTheme(self, uuid):
        return uuid in self.THEMES
    
    def addTheme(self, theme):
        self.THEMES[theme.uuid] = theme
        
    def getTheme(self, uuid):
        return self.THEMES[uuid]
    
    def getAllThemes(self):
        return self.THEMES.values()
    
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