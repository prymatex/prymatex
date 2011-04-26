#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re, plistlib
from glob import glob
from copy import copy, deepcopy
from xml.parsers.expat import ExpatError

# for run as main
if __name__ == "__main__":
    import sys
    sys.path.append(os.path.abspath('../..'))
from prymatex.bundles.score import PMXScoreManager
from prymatex.bundles.qtadapter import buildKeyEquivalentCode, buildKeyEquivalentString

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
    DRAGS = []
    PREFERENCES = {}
    TEMPLATES = []
    SETTINGS_CACHE = {}
    scores = PMXScoreManager()
    TABTRIGGERSPLITS = (re.compile(r"\s+", re.UNICODE), re.compile(r"\w+", re.UNICODE), re.compile(r"\W+", re.UNICODE), re.compile(r"\W", re.UNICODE)) 
    
    def __init__(self, hash, name_space, path = None):
        for key in [    'uuid', 'name', 'deleted', 'ordering', 'mainMenu', 'contactEmailRot13', 'description', 'contactName' ]:
            value = hash.pop(key, None)
            if key == 'mainMenu' and value != None:
                value = PMXMenuNode(self.name, **value)
            setattr(self, key, value)
        self.name_space = name_space
        self.path = path
        self.syntaxes = []
        self.snippets = []
        self.macros = []
        self.commands = []
        self.preferences = []
        self.templates = []

    def addBundleItem(self, item):
        if self.mainMenu != None:
            self.mainMenu[item.uuid] = item
        if item.tabTrigger != None:
            PMXBundle.TAB_TRIGGERS.setdefault(item.tabTrigger, []).append(item)
        if item.keyEquivalent != None:
            keyseq = buildKeyEquivalentCode(item.keyEquivalent)
            PMXBundle.KEY_EQUIVALENTS.setdefault(keyseq, []).append(item)
        # I'm four father
        item.setBundle(self)

    def buildEnvironment(self):
        env = copy(self.BASE_ENVIRONMENT)
        env.update({
            'TM_BUNDLE_PATH': self.path,
            'TM_BUNDLE_SUPPORT': self.getBundleSupportPath()
        });
        return env
        
    def getSyntaxByName(self, name):
        for syntax in self.syntaxes:
            if syntax.name == name:
                return syntax

    def getBundleSupportPath(self):
        return os.path.join(self.path, 'Support')

    @classmethod
    def loadBundle(cls, path, classes, name_space = 'prymatex'):
        info_file = os.path.join(path, 'info.plist')
        try:
            data = plistlib.readPlist(info_file)
            bundle = cls(data, name_space, path)
        except Exception, e:
            print "Error in bundle %s (%s)" % (info_file, e)
            return

        #Disabled?
        #if bundle.uuid in settings.disabled_bundles:
        #    return
            
        for klass in classes:
            for pattern in klass.path_patterns:
                files = glob(os.path.join(path, pattern))
                for sf in files:
                    try:
                        item = klass.loadBundleItem(sf, name_space)
                        if item != None:
                            bundle.addBundleItem(item)
                    except Exception, e:
                        print "Error in %s for %s (%s)" % (klass.__name__, sf, e)
        cls.BUNDLES[bundle.uuid] = bundle
        return bundle

    @classmethod
    def getBundleByName(cls, name):
        for _, bundle in cls.BUNDLES.iteritems():
            if bundle.name == name:
                return bundle

    @classmethod
    def getPreferences(cls, scope):
        with_scope = []
        without_scope = []
        for key in cls.PREFERENCES.keys():
            if key == None:
                without_scope.extend(cls.PREFERENCES[key])
            else:
                score = cls.scores.score(key, scope)
                if score != 0:
                    with_scope.append((score, cls.PREFERENCES[key]))
        with_scope.sort(key = lambda t: t[0], reverse = True)
        preferences = map(lambda (score, item): item, with_scope)
        with_scope = []
        for p in preferences:
            with_scope.extend(p)
        print with_scope, without_scope
        return with_scope and with_scope or without_scope

    @classmethod
    def getPreferenceSettings(cls, scope):
        #TODO: retrive the __class__ is ugly
        klass = cls.PREFERENCES.values()[0][0].__class__
        if scope not in cls.SETTINGS_CACHE:
            preferences = cls.getPreferences(scope)
            cls.SETTINGS_CACHE[scope] = klass.buildSettings(preferences)
        return cls.SETTINGS_CACHE[scope]

    @classmethod
    def getTabTriggerSymbol(cls, line, index):
        line = line[:index]
        for tabSplit in cls.TABTRIGGERSPLITS:
            matchs = filter(lambda m: m.start() <= index <= m.end(), tabSplit.finditer(line))
            if matchs:
                match = matchs.pop()
                word = line[match.start():match.end()]
                if cls.TAB_TRIGGERS.has_key(word):
                    return word
        
    
    @classmethod
    def getTabTriggerItem(cls, keyword, scope):
        with_scope = []
        without_scope = []
        if cls.TAB_TRIGGERS.has_key(keyword):
            for item in cls.TAB_TRIGGERS[keyword]:
                if item.scope == None:
                    without_scope.append(item)
                else:
                    score = cls.scores.score(item.scope, scope)
                    if score != 0:
                        with_scope.append((score, item))
            with_scope.sort(key = lambda t: t[0], reverse = True)
            with_scope = map(lambda (score, item): item, with_scope)
        print with_scope, without_scope
        return with_scope and with_scope or without_scope
            
    @classmethod
    def getKeyEquivalentItem(cls, code, scope):
        with_scope = []
        without_scope = []
        if code in cls.KEY_EQUIVALENTS:
            for item in cls.KEY_EQUIVALENTS[code]:
                if item.scope == None:
                    without_scope.append(item)
                else:
                    score = cls.scores.score(item.scope, scope)
                    if score != 0:
                        with_scope.append((score, item))
            with_scope.sort(key = lambda t: t[0], reverse = True)
            with_scope = map(lambda (score, item): item, with_scope)
        print with_scope, without_scope
        return with_scope and with_scope or without_scope

class PMXBundleItem(object):
    path_patterns = []
    bundle_collection = ""
    def __init__(self, hash, name_space, path = None):
        self.hash = deepcopy(hash)
        self.name_space = name_space
        self.path = path
        self.bundle = None
        for key in [    'uuid', 'bundleUUID', 'name', 'tabTrigger', 'keyEquivalent', 'scope' ]:
            setattr(self, key, hash.get(key, None))
    
    def setBundle(self, bundle):
        self.bundle = bundle
        if self.bundle_collection:
            collection = getattr(bundle, self.bundle_collection, None)
            if collection != None:
                collection.append(self)
    
    def buildEnvironment(self, **kwargs):
        env = self.bundle.buildEnvironment()
        return env
    
    @classmethod
    def loadBundleItem(cls, path, name_space = 'prymatex'):
        try:
            data = plistlib.readPlist(path)
            return cls(data, name_space, path)
        except Exception, e:
            data = open(path).read()
            for match in RE_XML_ILLEGAL.finditer(data):
                data = data[:match.start()] + "?" + data[match.end():]
            try:
                data = plistlib.readPlistFromString(data)
                return cls(data, name_space, path)
            except ExpatError, e:
                print "Error in %s for %s (%s)" % (cls.__name__, path, e)

    def buildMenuTextEntry(self, nemonic = ''):
        text = unicode(self.name)
        if nemonic:
            return text.replace('&', '&&') + u"\t" + nemonic
        if self.tabTrigger != None:
            text += u"\t%s⇥" % (self.tabTrigger)
        if self.keyEquivalent != None:
            text += u"\t%s" % (buildKeyEquivalentString(self.keyEquivalent))
        return text.replace('&', '&&')
    
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

def test_commands():
    bundle = PMXBundle.getBundleByName('Python')
    #bundle = PMXBundle.getBundleByName('SQL')
    errors = 0
    #for bundle in PMXBundle.BUNDLES.values():
    for command in bundle.commands:
        try:
            #if command.name.startswith("Validate Syntax"):
                env = command.buildEnvironment()
                env["TM_CURRENT_WORD"] = "echo"
                env["PHP_MANUAL_LOCATION"] = "http://www.php.net/download-docs.php"
            #if snippet.name.startswith("Convert Tabs To Table"):
                print command.name, command.path
                command.resolve(u"print 'ú'", u"d", env)
                command.execute({})
        except Exception, e:
            print command.path, e
            errors += 1
    print errors
    
def print_snippet_syntax():
    bundle = PMXBundle.getBundleByName('Bundle Development')
    syntax = bundle.getSyntaxByName("Snippet")
    pprint(syntax.hash)
    
def test_syntaxes():
    from prymatex.bundles.syntax import PMXSyntax
    from prymatex.bundles.processor import PMXDebugSyntaxProcessor
    syntax = PMXSyntax.getSyntaxesByName("Python")
    syntax[0].parse("class Persona(object):", PMXDebugSyntaxProcessor())
    print PMXSyntax.getSyntaxesNames()

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
    DIRECTORY = '/home/dvanhaaster/workspace/'
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

if __name__ == '__main__':
    from prymatex.bundles import BUNDLEITEM_CLASSES
    from pprint import pprint
    for file in glob(os.path.join('../../bundles/prymatex/Bundles', '*')):
        PMXBundle.loadBundle(file, BUNDLEITEM_CLASSES)
    print_commands()