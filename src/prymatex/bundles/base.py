import os, plistlib
from glob import glob
from xml.parsers.expat import ExpatError

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
    tabTriggers = {}
    keyEquivalents = {}
    
    def __init__(self, hash):
        for key in [    'uuid', 'name', 'deleted', 'ordering', 'mainMenu', 'contactEmailRot13', 'description', 'contactName' ]:
            value = hash.pop(key, None)
            if key == 'mainMenu' and value != None:
                value = PMXMenuNode(self.name, **value)
            setattr(self, key, value)
        
        if hash:
            print "Bundle '%s' has more values (%s)" % (self.name, ', '.join(hash.keys()))
    
    def addItem(self, item):
        self.mainMenu[item.uuid] = item
        if (hasattr(item, "tabTrigger") and item.tabTrigger != None):
            self.__class__.tabTriggers.setdefault(item.tabTrigger, []).append(item)
        if (hasattr(item, "keyEquivalent")  and item.keyEquivalent != None):
            self.__class__.keyEquivalents.setdefault(item.keyEquivalent, []).append(item)
    
    @staticmethod
    def loadBundle(path, elements, name_space = 'prymatex'):
        info_file = os.path.join(path, 'info.plist')
        try:
            data = plistlib.readPlist(info_file)
            bundle = PMXBundle(data)
        except Exception:
            print "Error en bundle %s" % info_file
        
        for name, pattern, klass in elements:
            files = glob(os.path.join(path, pattern))
            for sf in files:
                #Quito plis con caracteres raros.
                try:
                    data = plistlib.readPlist(sf)
                    item = klass(data, name_space)
                    bundle.addItem(item)
                except Exception, e:
                    pass
                    #print "Error in %s for %s (%s)" % (klass.__name__, sf, e)
        PMXBundle.BUNDLES[bundle.uuid] = bundle    
        return bundle
    
class PMXBundleItem(object):
    def __init__(self, hash, name_space):
        self.name_space = name_space
        for key in [    'uuid', 'bundleUUID', 'name', 'tabTrigger', 'keyEquivalent', 'scope' ]:
            setattr(self, key, hash.pop(key, None))
    
if __name__ == '__main__':
    from prymatex.bundles import command, macro, snippet, syntax, preference
    elements = (('Syntax', 'Syntaxes/*', syntax.PMXSyntax)
                   ('Snippet', 'Snippets/*', snippet.PMXSnippet)
                   ('Macro', 'Macros/*', macro.PMXMacro)
                   ('Command', 'Commands/*', command.PMXCommand)
                   ('Preference', 'Preferences/*', preference.PMXPreference)
                   )
    
    for file in glob(os.path.join('../share/Bundles/', '*')):
        PMXBundle.loadBundle(file, elements)
    
    #items = PMXBundle.tabTriggers["class"]
    #sp = PMXScoreManager()
    #reference_scope = 'source.python'
    #print filter(lambda item: sp.score( item.scope, reference_scope ) != 0, items)[0].content
    
    biggest = (None, [])
    for key, value in PMXBundle.tabTriggers.iteritems():
        if len(value) > len(biggest[1]):
            biggest = (key, value)
        items = filter(lambda item: isinstance(item, command.PMXCommand), value)
        if items:
            print "%s" % ", ".join(map(lambda item: item.name, items))
            
    print "%s: %s" % biggest
    biggest = (None, [])
    for key, value in PMXBundle.keyEquivalents.iteritems():
        if len(value) > len(biggest[1]):
            biggest = (key, value)
        items = filter(lambda item: isinstance(item, snippet.PMXSnippet), value)
        if items:
            print "%s" % ", ".join(map(lambda item: item.name, items))
    print "%s: %s" % biggest
            
    print "%s: %s" % biggest
    biggest = (None, [])
    for key, value in PMXBundle.keyEquivalents.iteritems():
        if len(value) > len(biggest[1]):
            biggest = (key, value)
        items = filter(lambda item: isinstance(item, snippet.PMXSnippet), value)
        if items:
            print "%s" % ", ".join(map(lambda item: item.name, items))