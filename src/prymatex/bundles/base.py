#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, plistlib
from glob import glob
from copy import deepcopy
from xml.parsers.expat import ExpatError

# for run as main
if __name__ == "__main__":
    import sys
    sys.path.append(os.path.abspath('../..'))
from prymatex.bundles.score import PMXScoreManager

'''
    Este es el unico camino -> http://manual.macromates.com/en/
    http://manual.macromates.com/en/bundles
    http://blog.macromates.com/2005/introduction-to-scopes/
    http://manual.macromates.com/en/scope_selectors.html
'''

class PMXMenuNode(object):
    MENU_SPACE = '-' * 36
    def __init__(self, name = '', items = [], excludedItems = [], submenus = {}):
        self.name = name
        self.items = items
        self.excludedItems = excludedItems
        self.main = dict(map(lambda i: (i, None), filter(lambda x: x != self.MENU_SPACE, self.items)))
        for uuid, submenu in submenus.iteritems():
            self[uuid] = PMXMenuNode(**submenu)

    def __contains__(self, key):
        return key in self.main or any(map(lambda submenu: key in submenu, filter(lambda x: isinstance(x, PMXMenuNode), self.main.values())))

    def __getitem__(self, key):
        try:
            return self.main[key]
        except KeyError:
            for submenu in filter(lambda x: isinstance(x, PMXMenuNode), self.main.values()):
                if key in submenu:
                    return submenu[key]
        raise KeyError(key)
    
    def __setitem__(self, key, menu):
        if key in self.main:
            self.main[key] = menu
        else:
            for submenu in filter(lambda x: isinstance(x, PMXMenuNode), self.main.values()):
                if key in submenu:
                    submenu[key] = menu

    def iteritems(self):
        items = self.items
        if self.excludedItems:
            items = filter(lambda x: not x in self.excludedItems, items)
        for item in items:
            if item != self.MENU_SPACE:
                yield (item, self[item])
            else:
                yield (self.MENU_SPACE, self.MENU_SPACE)

class PMXBundle(object):
    BUNDLES = {}
    TAB_TRIGGERS = {}
    KEY_EQUIVALENTS = {}
    PREFERENCES = {}
    scores = PMXScoreManager()
    
    def __init__(self, hash):
        for key in [    'uuid', 'name', 'deleted', 'ordering', 'mainMenu', 'contactEmailRot13', 'description', 'contactName' ]:
            value = hash.pop(key, None)
            if key == 'mainMenu' and value != None:
                value = PMXMenuNode(self.name, **value)
            setattr(self, key, value)
        self.syntaxes = []
        self.snippets = []
        self.macros = []
        self.commands = []
        self.preferences = []
        
        if hash:
            print "Bundle '%s' has more values (%s)" % (self.name, ', '.join(hash.keys()))

    def addItem(self, item):
        if self.mainMenu != None:
            self.mainMenu[item.uuid] = item
        if item.tabTrigger != None:
            PMXBundle.TAB_TRIGGERS.setdefault(item.tabTrigger, []).append(item)
        if item.keyEquivalent != None:
            PMXBundle.KEY_EQUIVALENTS.setdefault(item.keyEquivalent, []).append(item)
        # I'm four father
        item.bundle = self

    def addSyntax(self, syntax):
        self.addItem(syntax)
        self.syntaxes.append(syntax)

    def addSnippet(self, snippet):
        self.addItem(snippet)
        self.snippets.append(snippet)

    def addMacro(self, macro):
        self.addItem(macro)
        self.macros.append(macro)

    def addCommand(self, command):
        self.addItem(command)
        self.commands.append(command)

    def addPreference(self, preference):
        self.addItem(preference)
        self.preferences.append(preference)
        PMXBundle.PREFERENCES.setdefault(preference.scope, []).append(preference)
    
    def getSyntaxByName(self, name):
        for syntax in self.syntaxes:
            if syntax.name == name:
                return syntax

    @staticmethod
    def loadBundle(path, elements, name_space = 'prymatex'):
        info_file = os.path.join(path, 'info.plist')
        try:
            data = plistlib.readPlist(info_file)
            bundle = PMXBundle(data)
        except Exception, e:
            print "Error en bundle %s (%s)" % (info_file, e)
            
        for name, pattern, klass in elements:
            files = glob(os.path.join(path, pattern))
            for sf in files:
                try:
                    data = plistlib.readPlist(sf)
                    item = klass(data, name_space)
                    method = getattr(bundle, "add" + name, None)
                    if method != None:
                        method(item)
                except Exception, e:
                    print "Error in %s for %s (%s)" % (klass.__name__, sf, e)
        PMXBundle.BUNDLES[bundle.uuid] = bundle
        return bundle

    @classmethod
    def getBundleByName(cls, name):
        for uuid, bundle in cls.BUNDLES.iteritems():
            if bundle.name == name:
                return bundle

    @classmethod
    def getPreferences(cls, scope):
        preferences = []
        for key in cls.PREFERENCES.keys():
            if key == None:
                score = 1
            else:
                score = cls.scores.score(scope, key)
            if score != 0:
                preferences.append((score, cls.PREFERENCES[key]))
        preferences.sort(key = lambda t: t[0])
        result = []
        for _, ps in preferences:
            result.extend(ps)
        return result

    @classmethod
    def getTabTriggerItem(cls, keyword, scope):
        items = []
        if cls.TAB_TRIGGERS.has_key(keyword):
            for item in cls.TAB_TRIGGERS[keyword]:
                score = cls.scores.score(scope, item.scope)
                if score != 0:
                    items.append((score, item))
            items.sort(key = lambda t: t[0])
            items = map(lambda (score, item): item, items)
        return items
            
    @classmethod
    def getKeyEquivalentItem(cls, key, scope):
        items = []
        if cls.KEY_EQUIVALENTS.has_key(key):
            for item in cls.KEY_EQUIVALENTS[key]:
                score = cls.scores.score(scope, item.scope)
                if score != 0:
                    items.append((score, item))
            items.sort(key = lambda t: t[0])
            items = map(lambda (score, item): item, items)
        return items

class PMXBundleItem(object):
    def __init__(self, hash, name_space):
        self.hash = deepcopy(hash)
        self.name_space = name_space
        for key in [    'uuid', 'bundleUUID', 'name', 'tabTrigger', 'keyEquivalent', 'scope' ]:
            setattr(self, key, hash.pop(key, None))

#----------------------------------------
# Tests
#----------------------------------------
def test_preferences():
    from prymatex.bundles.preference import PMXPreference
    bundle = PMXBundle.getBundleByName('Python')
    print PMXPreference.getSettings(bundle.getPreferences('source.python'))

def test_snippets():
    bundle = PMXBundle.getBundleByName('Python')
    for snippet in bundle.snippets:
        if snippet.name == 'New Class':
            print snippet.content
        #if snippet.name == 'New Function':
            snippet.compile()
            
def print_snippet_syntax():
    bundle = PMXBundle.getBundleByName('Bundle Development')
    syntax = bundle.getSyntaxByName("Snippet")
    print syntax.hash
    
def test_syntaxes():
    from prymatex.bundles.syntax import PMXSyntax
    print PMXSyntax.getSyntaxesByScope("text")
    print PMXSyntax.getSyntaxesNames()
    
if __name__ == '__main__':
    from prymatex.bundles import BUNDLE_ELEMENTS
    from pprint import pprint
    for file in glob(os.path.join('../share/Bundles/', '*')):
        PMXBundle.loadBundle(file, BUNDLE_ELEMENTS)
    test_syntaxes()