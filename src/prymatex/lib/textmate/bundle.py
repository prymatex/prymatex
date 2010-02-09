import os
from glob import glob
import plistlib
from prymatex.lib.textmate import command, macro, snippet, syntax, template 
from xml.parsers.expat import ExpatError

TM_BUNDLES = {}

class TMMenuNode(object):
    def __init__(self, name, items, excludedItems = [], submenus = {}):
        self.name = name
        self.items = items
        self.excludedItems = excludedItems
        self.main = dict(map(lambda i: (i, None), filter(lambda x: x != '-' * 36, self.items)))
        for uuid, submenu in submenus.iteritems():
            self[uuid] = TMMenuNode(**submenu)

    def __contains__(self, key):
        return key in self.main or any(map(lambda submenu: key in submenu, filter(lambda x: isinstance(x, TMMenuNode), self.main.values())))

    def __getitem__(self, key):
        try:
            return self.main[key]
        except KeyError:
            for submenu in filter(lambda x: isinstance(x, TMMenuNode), self.main.values()):
                if key in submenu:
                    return submenu[key]
        raise Exception();
    
    def __setitem__(self, key, menu):
        #TODO: Ver si esta en exclude o en deleted
        if key in self.main:
            self.main[key] = menu
        else:
            for submenu in filter(lambda x: isinstance(x, TMMenuNode), self.main.values()):
                if key in submenu:
                    submenu[key] = menu

class TMBundle(object):
    def __init__(self, hash):
        self.uuid = hash.get('uuid')
        self.name = hash.get('name')
        self.description = hash.get('description')
        self.contact = {'Name': hash.get('contactName'), 'Email': hash.get('contactEmailRot13') }
        if 'mainMenu' in hash:
            self.menu = TMMenuNode('main', **hash.get('mainMenu'))
            self.menu.deleted = hash.get('deleted', [])
            self.menu.ordering = hash.get('ordering', [])
        else:
            self.menu = {}
        TM_BUNDLES[self.name] = self

def load_textmate_bundle(bundle_path):
    '''
    Carga un bundle
    @return: bundle cargado
    '''
    info_file = os.path.join(bundle_path, 'info.plist')
    try:
        data = plistlib.readPlist(info_file)
        bundle = TMBundle(data)
    except ExpatError:
        continue
    
    #Syntaxes
    syntax_files = glob(os.path.join(bundle_path, 'Syntaxes', '*'))
    for sf in syntax_files:
        #Quito plis con caracteres raros.
        try:
            data = plistlib.readPlist(sf)
            uuid = data.pop('uuid')
            s = syntax.TMSyntaxNode(data, None, bundle.name)
            bundle.menu[uuid] = s
        except ExpatError:
            pass
    
    #Snippets
    syntax_files = glob(os.path.join(bundle_path, 'Snippets', '*'))
    for sf in syntax_files:
        #Quito plis con caracteres raros.
        try:
            data = plistlib.readPlist(sf)
            uuid = data.pop('uuid')
            s = snippet.TMSnippet(data, bundle.name)
            bundle.menu[uuid] = s
        except ExpatError:
            pass
    
    #Macros
    syntax_files = glob(os.path.join(bundle_path, 'Macros', '*'))
    for sf in syntax_files:
        #Quito plis con caracteres raros.
        try:
            data = plistlib.readPlist(sf)
            uuid = data.pop('uuid')
            m = macro.Macro(data, bundle.name)
            bundle.menu[uuid] = m
        except ExpatError:
            pass
    
    #Commands
    syntax_files = glob(os.path.join(bundle_path, 'Commands', '*'))
    for sf in syntax_files:
        #Quito plis con caracteres raros.
        try:
            data = plistlib.readPlist(sf)
            uuid = data.pop('uuid')
            c = command.Command(data, bundle.name)
            bundle.menu[uuid] = c
        except ExpatError:
            pass
    
    #Templates
    #syntax_files = glob(os.path.join(bundle_path, 'Templates', '*'))
    #for sf in syntax_files:
        #Quito plis con caracteres raros.
        #try:
            #data = plistlib.readPlist(sf)
            #template.Template(data, bundle.name)
        #except ExpatError:
            #pass
    return bundle

def load_textmate_bundles(path):
    '''
    Forma simple de cargar los bundles de manera no diferida
    @return: Canidad de bundles cargados
    '''
    paths = glob(os.path.join(path, '*.tmbundle'))
    counter = 0
    for bundle_path in paths:
        load_textmate_bundle(bundle_path)
        counter += 1
    return counter