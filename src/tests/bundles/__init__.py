#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, glob
import plistlib
import syntax, snippet, macro, command, template
from xml.parsers.expat import ExpatError

BUNDLES = {}

class MenuItem(object):
    def __init__(self, uuid, name, comment = ''):
        pass

class MenuNode(object):
    def __init__(self, uuid, name, items, submenus = {}):
        self.uuid = uuid
        self.name = name
        self.main = dict(map(lambda i: (i, None), filter(lambda x: x != '-' * 36, items)))
        for uuid, submenu in submenus.iteritems():
            self[uuid] = MenuNode(**submenu)

    def __contains__(self, key):
        return key in self.main or any(map(lambda submenu: key in submenu, filter(lambda x: isinstance(x, MenuNode), self.main.values())))

    def __getitem__(self, key):
        try:
            return self.main[key]
        except KeyError:
            for submenu in filter(lambda x: isinstance(x, MenuNode), self.main.values()):
                if key in submenu:
                    return submenu[key]
        raise Exception();
    
    def __setitem__(self, key, menu):
        if key in self.main:
            self.main[key] = menu
        else:
            for submenu in filter(lambda x: isinstance(x, MenuNode), self.main.values()):
                if key in submenu:
                    submenu[key] = menu
        
class Bundle(object):
    def __init__(self, uuid, name, description = '', contactName = '', contactEmailRot13 = '', deleted = [], ordering = [], mainMenu = [], excludedItems = []):
        self.uuid = uuid
        self.name = name
        self.description = description
        self.contact = {'Name': contactName, 'Email': contactEmailRot13 }
        if mainMenu:
            self.menu = MenuNode(uuid, 'main', mainMenu)
        BUNDLES[self.name] = self
    
    @classmethod
    def load(cls, bundle_path):
        #Info
        info_file = os.path.join(bundle_path, 'info.plist')
        data = plistlib.readPlist(info_file)
        bundle = Bundle(**data)
        
        #TODO: Agregar las entradas al menu
        #Syntaxes
        syntax_files = glob.glob(os.path.join(bundle_path, 'Syntaxes', '*'))
        for sf in syntax_files:
            #Quito plis con caracteres raros.
            try:
                data = plistlib.readPlist(sf)
                syntax.SyntaxNode(data, None, bundle.name)
            except ExpatError:
                pass
        
        #Snippets
        syntax_files = glob.glob(os.path.join(bundle_path, 'Snippets', '*'))
        for sf in syntax_files:
            #Quito plis con caracteres raros.
            try:
                data = plistlib.readPlist(sf)
                snippet.Snippet(data, bundle.name)
            except ExpatError:
                pass
        
        #Macros
        syntax_files = glob.glob(os.path.join(bundle_path, 'Macros', '*'))
        for sf in syntax_files:
            #Quito plis con caracteres raros.
            try:
                data = plistlib.readPlist(sf)
                macro.Macro(data, bundle.name)
            except ExpatError:
                pass
        
        #Commands
        syntax_files = glob.glob(os.path.join(bundle_path, 'Commands', '*'))
        for sf in syntax_files:
            #Quito plis con caracteres raros.
            try:
                data = plistlib.readPlist(sf)
                command.Command(data, bundle.name)
            except ExpatError:
                pass
        
        #Templates
        #syntax_files = glob.glob(os.path.join(bundle_path, 'Templates', '*'))
        #for sf in syntax_files:
            #Quito plis con caracteres raros.
            #try:
                #data = plistlib.readPlist(sf)
                #template.Template(data, bundle.name)
            #except ExpatError:
                #pass

def load_bundles():
    paths = glob.glob('./bundles/Bundles/*.tmbundle')
    for path in paths:
        Bundle.load(os.path.abspath(path))

load_bundles()

def main():
    # TEST, TEST
    from pprint import pprint
    pprint(syntax.SYNTAXES)
    pprint(snippet.SNIPPETS)

if __name__ == '__main__':
    main()

