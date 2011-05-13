#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re, plistlib
from glob import glob
from copy import copy, deepcopy
from xml.parsers.expat import ExpatError

# for run as main
if __name__ == "__main__":
    import sys
    sys.path.append(os.path.abspath('..'))
from prymatex.support.qtadapter import buildKeyEquivalentString

'''
    Este es el unico camino -> http://manual.macromates.com/en/
    http://manual.macromates.com/en/bundles
    http://blog.macromates.com/2005/introduction-to-scopes/
    http://manual.macromates.com/en/scope_selectors.html
'''

RE_XML_ILLEGAL = u'([\u0000-\u0008\u000b-\u000c\u000e-\u001f\ufffe-\uffff])' + \
                 u'|' + \
                 u'([%s-%s][^%s-%s])|([^%s-%s][%s-%s])|([%s-%s]$)|(^[%s-%s])' % \
                  (unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
                   unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
                   unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff))

RE_XML_ILLEGAL = re.compile(RE_XML_ILLEGAL)

class PMXMenuNode(object):
    MENU_SPACE = '-' * 36
    def __init__(self, name = None, items = [], excludedItems = [], submenus = {}):
        self.name = name
        self.items = items
        self.excludedItems = excludedItems
        self.submenus = submenus
        self.main = dict(map(lambda i: (i, None), filter(lambda x: x != self.MENU_SPACE, self.items)))
        for uuid, submenu in self.submenus.iteritems():
            self[uuid] = PMXMenuNode(**submenu)

    @property
    def hash(self):
        hash = { 'items': self.items }
        if self.name != None:
            hash['name'] = self.name
        if self.excludedItems:
            hash['excludedItems'] = self.excludedItems
        if self.submenus:
            hash['submenus'] = {}
        for uuid in self.submenus.keys():
            submenu = self[uuid]
            if submenu != None:
                hash['submenus'].update( { uuid: submenu.hash } )
        return hash
            
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
    KEYS = [    'uuid', 'name', 'deleted', 'ordering', 'mainMenu', 'contactEmailRot13', 'description', 'contactName' ]
    FILE = 'info.plist'
    def __init__(self, namespace, hash = None, path = None):
        self.namespace = namespace
        self.path = path
        self.disabled = False
        self.support = None
        self.manager = None
        if hash != None:
            self.load(hash)

    def load(self, hash):
        for key in PMXBundle.KEYS:
            value = hash.get(key, None)
            setattr(self, key, value)
        if self.mainMenu != None:
            self.mainMenu = PMXMenuNode(**self.mainMenu)

    @property
    def hash(self):
        #TODO: el menu
        hash = {}
        for key in PMXBundle.KEYS:
            value = getattr(self, key)
            if value != None:
                if key in ['mainMenu']:
                    value = self.mainMenu.hash
                hash[key] = value
        return hash

    def save(self, base = None):
        if base != None:
            path = os.path.join(base, os.path.basename(self.path))
            if not os.path.exists(path):
                os.makedirs(path)
            file = os.path.join(path, self.FILE)
        else:
            file = os.path.join(self.path , self.FILE)
        plistlib.writePlist(self.hash, file)

    def buildEnvironment(self):
        env = copy(self.manager.buildEnvironment())
        env['TM_BUNDLE_PATH'] = self.path
        if self.support != None:
            env['TM_BUNDLE_SUPPORT'] = self.support
        return env

    def getSyntaxByName(self, name):
        for syntax in self.syntaxes:
            if syntax.name == name:
                return syntax

    @classmethod
    def loadBundle(cls, path, namespace):
        info_file = os.path.join(path, cls.FILE)
        try:
            data = plistlib.readPlist(info_file)
            bundle = cls(namespace, data, path)
            return bundle
        except Exception, e:
            print "Error in bundle %s (%s)" % (info_file, e)

class PMXBundleItem(object):
    KEYS = [ 'uuid', 'name', 'tabTrigger', 'keyEquivalent', 'scope' ]
    TYPE = ''
    FOLDER = ''
    FILES = []
    def __init__(self, namespace, hash = None, path = None):
        self.namespace = namespace
        self.path = path
        self.bundle = None
        if hash != None:
            self.load(hash)

    def load(self, hash):
        for key in PMXBundleItem.KEYS:
            setattr(self, key, hash.get(key, None))
    
    @property
    def hash(self):
        hash = {}
        for key in PMXBundleItem.KEYS:
            value = getattr(self, key)
            if value != None:
                hash[key] = value
        return hash

    def save(self, base = None):
        if base != None:
            path = os.path.join(base, os.path.basename(self.bundle.path), self.FOLDER)
            if not os.path.exists(path):
                os.makedirs(path)
            file = os.path.join(path , os.path.basename(self.path))
        else:
            file = self.path
        plistlib.writePlist(self.hash, file)
        
    @property
    def trigger(self):
        trigger = []
        if self.tabTrigger != None:
            trigger.append(u"%s⇥" % (self.tabTrigger))
        if self.keyEquivalent != None:
            trigger.append(u"%s" % (buildKeyEquivalentString(self.keyEquivalent)))
        return ", ".join(trigger)

    def buildEnvironment(self, **kwargs):
        env = self.bundle.buildEnvironment()
        return env
        
    def buildMenuTextEntry(self, nemonic = ''):
        text = unicode(self.name)
        if nemonic:
            return text.replace('&', '&&') + u"\t" + nemonic
        else:
            text += u"\t%s" % (self.trigger)
        return text.replace('&', '&&')
    
    # Trying to speed things up a bit, a memoize     
    @classmethod
    def loadBundleItem(cls, path, namespace):
        try:
            data = plistlib.readPlist(path)
            item = cls(namespace, data, path)
            return item
        except Exception, e:
            data = open(path).read()
            for match in RE_XML_ILLEGAL.finditer(data):
                data = data[:match.start()] + "?" + data[match.end():]
            try:
                data = plistlib.readPlistFromString(data)
                item = cls(namespace, data, path)
                return item
            except ExpatError, e:
                print "Error in %s for %s (%s)" % (cls.__name__, path, e)
    
    def resolve(self, *args, **kwargs):
        pass

#----------------------------------------
# Tests
#----------------------------------------
def test_snippets():
    #bundle = PMXBundle.getBundleByName('LaTeX')
    bundle = PMXBundle.getBundleByName('HTML')
    errors = 0
    #for bundle in PMXBundle.BUNDLES.values():
    for snippet in bundle.snippets:
        try:
            if snippet.name.startswith("Special:"):
            #if snippet.name.startswith("belongs_to"):
                snippet.compile()
                snippet.resolve(indentation = "",
                                tabreplacement = "----",
                                environment = {"TM_CURRENT_LINE": "  ", "TM_SCOPE": "text.tex.latex string.other.math.block.environment.latex", "TM_SELECTED_TEXT": "uno\tdos\tcuatro\t"})
                print "-" * 10, " Bundle ", bundle.name, " Test ", snippet.name, " (", snippet.tabTrigger, ") ", "-" * 10
                print snippet.path
                print "Origin: ", len(snippet), snippet.next()
                print snippet, snippet.ends
                clon = snippet.clone()
                clon.write(0, "Un Capitulo Nuevo")
                print "Clone: ", len(clon), clon.next()
                print clon, clon.ends
        except Exception, e:
            print bundle.name, snippet.name, e
            errors += 1
            if "'ascii' codec can't encode" not in str(e):
                import sys, traceback
                traceback.print_exc()
                sys.exit(0)
    print errors
    
def test_syntaxes():
    from prymatex.bundles.syntax import PMXSyntax
    from time import time
    from prymatex.bundles.processor import PMXSyntaxProcessor
    syntax = PMXSyntax.getSyntaxesByName("Python")
    print syntax[0].hash
    file = open('../gui/editor/codeedit.py', 'r');
    start = time()
    syntax[0].parse(file.read(), PMXSyntaxProcessor())
    file.close()
    print "Time:", time() - start

def print_commands():
    before = []
    for bundle in PMXBundle.BUNDLES.values():
        for command in bundle.commands:
            if command.beforeRunningCommand != "nop":
                before.append(command.beforeRunningCommand)
    print before

def test_keys():
    from pprint import pprint
    pprint(PMXBundle.KEY_EQUIVALENTS)
    
def test_templates():
    DIRECTORY = os.path.join(os.path.expanduser('~'), 'workspace/')
    for template in PMXBundle.TEMPLATES:
        environment = template.buildEnvironment(directory = DIRECTORY)
        template.resolve(environment)

def test_bundle_elements():
    from pprint import pprint
    pprint(PMXBundle.BUNDLES)
    pprint(PMXBundle.TAB_TRIGGERS)
    pprint(PMXBundle.KEY_EQUIVALENTS)
    pprint(PMXBundle.KEY_SEQUENCE)
    pprint(PMXBundle.PREFERENCES)
    pprint(PMXBundle.TEMPLATES)

def test_preferences():
    settings = PMXBundle.getPreferenceSettings('source.c++')
    for key in settings.KEYS:
        print key, getattr(settings, key)

def test_macros():
    bundles = PMXBundle.BUNDLES.values()
    commands = []
    for bundle in bundles:
        for macro in bundle.macros:
            for command in macro.commands:
                c = command['command']
                if c not in commands:
                    commands.append(c)
    print commands
    
def test_queryItems():
    from prymatex.bundles.qtadapter import Qt
    print PMXBundle.getTabTriggerItem('class', 'source.python')
    print PMXBundle.getKeyEquivalentItem(Qt.CTRL + ord('H'), 'text.html')

def test_saveBundleItems():
    from prymatex.bundles import PMXBundle
    for bundle in PMXBundle.BUNDLES.values():
        bundle.save(base = os.path.join(os.path.expanduser('~'), 'Bundles'))
    
if __name__ == '__main__':
    from prymatex.bundles import PMXBundleManager
    manager = PMXBundleManager(disabled = [], deleted = [])
    manager.addNameSpace(manager.DEFAULT, os.path.abspath('../bundles/prymatex'))
    manager.addNameSpace('user', os.path.abspath(os.path.join(os.path.expanduser('~'), '.prymatex')))
    manager.loadShit()
    for bundle in manager.BUNDLES.values():
        print bundle.buildEnvironment()
