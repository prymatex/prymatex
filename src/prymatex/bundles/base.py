import os
from glob import glob
import plistlib
if __name__ != "__main__":
    from prymatex.bundles import command, macro, snippet, syntax 
from xml.parsers.expat import ExpatError

PMX_BUNDLES = {}

MENU_SPACE = '-' * 36
class PMXMenuNode(object):
    def __init__(self, name = '', items = [], excludedItems = [], submenus = {}):
        self.name = name
        self.items = items
        self.excludedItems = excludedItems
        self.main = dict(map(lambda i: (i, None), filter(lambda x: x != MENU_SPACE, self.items)))
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
        #TODO: Ver si esta en exclude o en deleted
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
        if hasattr(self, 'deleted') and self.deleted:
            items = filter(lambda x: not x in self.deleted, items)
        for item in items:
            if item != MENU_SPACE:
                yield (item, self[item])
            else:
                yield (MENU_SPACE, MENU_SPACE)
        
class PMXBundle(object):
    def __init__(self, hash):
        global PMX_BUNDLES
        self.uuid = hash.get('uuid')
        self.name = hash.get('name')
        self.description = hash.get('description')
        self.contact = {'Name': hash.get('contactName'), 'Email': hash.get('contactEmailRot13') }
        if 'mainMenu' in hash:
            self.menu = PMXMenuNode('main', **hash.get('mainMenu'))
            self.menu.deleted = hash.get('deleted', [])
            self.menu.ordering = hash.get('ordering', [])
        else:
            self.menu = {}
        PMX_BUNDLES[self.name] = self

def load_prymatex_bundle(bundle_path):
    '''
    Carga un bundle
    @return: bundle cargado
    '''
    BUNDLE_ELEMENTS = {'Syntaxes': syntax.PMXSyntax,
                       'Snippets': snippet.PMXSnippet,
                       'Macros': macro.PMXMacro,
                       'Commands': command.PMXCommand}
    info_file = os.path.join(bundle_path, 'info.plist')
    try:
        data = plistlib.readPlist(info_file)
        bundle = PMXBundle(data)
    except ExpatError:
        raise
    
    for path, klass in BUNDLE_ELEMENTS.iteritems():
        files = glob(os.path.join(bundle_path, path, '*'))
        for sf in files:
            #Quito plis con caracteres raros.
            try:
                data = plistlib.readPlist(sf)
                uuid = data.pop('uuid')
                bundleUUID = data.pop('bundleUUID', None)
                e = klass(data, 'prymatex')
                bundle.menu[uuid] = e
            except ExpatError:
                pass
    
    return bundle

from os.path import basename

def load_prymatex_bundles(path, after_load_callback = None):
    '''
    Forma simple de cargar los bundles de manera no diferida
    @return: Canidad de bundles cargados
    '''
    paths = glob(os.path.join(path, '*.tmbundle'))
    counter = 0
    total = len(paths)
    for bundle_path in paths:
        if callable(after_load_callback):
            after_load_callback(counter = counter, total = total, 
                                name = basename(bundle_path).split('.')[0])
        load_prymatex_bundle(bundle_path)
        counter += 1
        
    return counter

if __name__ == '__main__':
    import command, macro, snippet, syntax
    bundle = load_prymatex_bundle('../share/Bundles/Python.tmbundle')
    from pprint import pprint
    pprint(bundle.uuid)
    pprint(bundle.menu.main)