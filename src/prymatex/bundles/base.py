#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re, plistlib, ipdb
from glob import glob
from copy import copy, deepcopy
from xml.parsers.expat import ExpatError

# for run as main
if __name__ == "__main__":
    import sys
    sys.path.append(os.path.abspath('../..'))
from prymatex.bundles.score import PMXScoreManager
from prymatex.core.config import settings
from prymatex.bundles.qtadapter import buildKeyEquivalentString, buildKeySequence

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
    KEY_SEQUENCE = {}
    PREFERENCES = {}
    TEMPLATES = []
    scores = PMXScoreManager()
    
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
            keyseq = buildKeySequence(item.keyEquivalent)
            if keyseq > 255:
                PMXBundle.KEY_SEQUENCE.setdefault(keyseq, []).append(item)
            else:
                PMXBundle.KEY_EQUIVALENTS.setdefault(keyseq, []).append(item)
        # I'm four father
        item.setBundle(self)

    def buildEnvironment(self):
        env = deepcopy(os.environ)
        env.update({
            'TM_APP_PATH': settings['PMX_APP_PATH'],
            'TM_BUNDLE_PATH': self.path,
            'TM_BUNDLE_SUPPORT': self.getBundleSupportPath(),
            'TM_SUPPORT_PATH': settings['PMX_SUPPORT_PATH'],
        });
        #Append TM_BUNDLE_SUPPORT TM_SUPPORT_PATH and to PATH
        env['PATH'] = env['PATH'] + ':' + env['TM_BUNDLE_SUPPORT'] + '/bin:' + env['TM_SUPPORT_PATH'] + '/bin'
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
        if bundle.uuid in settings.disabled_bundles:
            return
            
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
                if not item.ready():
                    item.compile()
                if item.scope == None:
                    items.append((1, item))
                else:
                    score = cls.scores.score(item.scope, scope)
                    if score != 0:
                        items.append((score, item))
            items.sort(key = lambda t: t[0])
            items = map(lambda (score, item): item.clone(), items)
        return items
            
    @classmethod
    def getKeyEquivalentItem(cls, character, scope):
        items = []
        if cls.KEY_EQUIVALENTS.has_key(character):
            for item in cls.KEY_EQUIVALENTS[character]:
                if not item.ready():
                    item.compile()
                if item.scope == None:
                    items.append((1, item))
                else:
                    score = cls.scores.score(item.scope, scope)
                    if score != 0:
                        items.append((score, item))
            items.sort(key = lambda t: t[0])
            items = map(lambda (score, item): item.clone(), items)
        return items

    @classmethod
    def getKeySequenceItem(cls, key, scope):
        items = []
        if cls.KEY_SEQUENCE.has_key(key):
            for item in cls.KEY_SEQUENCE[key]:
                if not item.ready():
                    item.compile()
                if item.scope == None:
                    items.append((1, item))
                else:
                    score = cls.scores.score(item.scope, scope)
                    if score != 0:
                        items.append((score, item))
            items.sort(key = lambda t: t[0])
            items = map(lambda (score, item): item.clone(), items)
        return items
    
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

    def buildMenuTextEntry(self):
        text = unicode(self.name)
        if self.tabTrigger != None:
            text += u" \t %s⇥" % (self.tabTrigger)
        if self.keyEquivalent != None:
            text += u" \t %s" % (buildKeyEquivalentString(self.keyEquivalent))
        return text
    
    def clone(self):
        return self
    
    def ready(self):
        return True

    def compile(self):
        pass

    def resolve(self, **kwargs):
        pass

#----------------------------------------
# Tests
#----------------------------------------
def test_snippets():
    bundle = PMXBundle.getBundleByName('LaTeX')
    #bundle = PMXBundle.getBundleByName('Python')
    errors = 0
    #for bundle in PMXBundle.BUNDLES.values():
    for snippet in bundle.snippets:
        try:
            #if snippet.name.startswith("Itemize Lines"):
            #if snippet.name.startswith("belongs_to"):
                snippet.compile()
                snippet.resolve(indentation = "",
                                tabreplacement = "    ",
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

def buildEnvironment(bundle = None):
    env = deepcopy(os.environ)
    env.update({'TM_CURRENT_LINE': 'TM_CURRENT_LINE',
           'TM_SUPPORT_PATH': settings['PMX_SUPPORT_PATH'],
           'TM_INPUT_START_LINE_INDEX': '',
           'TM_LINE_INDEX': '', 
           'TM_LINE_NUMBER': '', 
           'TM_SELECTED_SCOPE': 'TM_SELECTED_SCOPE', 
           'TM_CURRENT_WORD': 'TM_CURRENT_WORD',
           'TM_FILEPATH': '',
           'TM_FILENAME': '',
           'TM_PROJECT_DIRECTORY': '',
           'TM_DIRECTORY': '',
           'TM_SOFT_TABS': 'YES',
           'TM_TAB_SIZE': "TM_TAB_SIZE",
           'TM_BUNDLE_SUPPORT': bundle != None and bundle.getBundleSupportPath() or '',
           'TM_SELECTED_TEXT': "TM_SELECTED_TEXT"})
    env.update(settings['static_variables'])
    return env
    
def test_commands():
    bundle = PMXBundle.getBundleByName('LaTeX')
    #bundle = PMXBundle.getBundleByName('SQL')
    errors = 0
    #for bundle in PMXBundle.BUNDLES.values():
    for command in bundle.commands:
        try:
            #if snippet.name.startswith("Itemize Lines"):
            #if snippet.name.startswith("Convert Tabs To Table"):
                command.compile()
                command.resolve(environment = buildEnvironment(bundle = bundle))
                print command.name, command
        except Exception, e:
            print bundle.name, command.name, e
            errors += 1
    print errors
    
def print_snippet_syntax():
    bundle = PMXBundle.getBundleByName('Bundle Development')
    syntax = bundle.getSyntaxByName("Snippet")
    pprint(syntax.hash)
    
def test_syntaxes():
    from prymatex.bundles.syntax import PMXSyntax
    from prymatex.bundles.processor import PMXDebugSyntaxProcessor
    syntax = PMXSyntax.getSyntaxesByName("LaTeX")
    syntax[0].parse("item", PMXDebugSyntaxProcessor())
    print PMXSyntax.getSyntaxesNames()

def print_commands():
    from pprint import pprint
    pprint(PMXBundle.KEY_EQUIVALENTS)

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
    
if __name__ == '__main__':
    from prymatex.bundles import BUNDLEITEM_CLASSES
    from pprint import pprint
    for file in glob(os.path.join(settings['PMX_BUNDLES_PATH'], '*')):
        PMXBundle.loadBundle(file, BUNDLEITEM_CLASSES)
    test_templates()