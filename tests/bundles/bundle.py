#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, glob
import plistlib
import syntax, snippet, macro, command, template, theme
from xml.parsers.expat import ExpatError

TM_BUNDLES = {}

class MenuItem(object):
    def __init__(self, uuid, name, comment = ''):
        pass

class MenuNode(object):
    def __init__(self, name, items, excludedItems = [], submenus = {}):
        self.name = name
        self.items = items
        self.excludedItems = excludedItems
        self.main = dict(map(lambda i: (i, None), filter(lambda x: x != '-' * 36, self.items)))
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
    def __init__(self, hash):
        self.uuid = hash.get('uuid')
        self.name = hash.get('name')
        self.description = hash.get('description')
        self.contact = {'Name': hash.get('contactName'), 'Email': hash.get('contactEmailRot13') }
        if 'mainMenu' in hash:
            self.menu = MenuNode('main', **hash.get('mainMenu'))
        self.deleted = hash.get('deleted', [])
        self.ordering = hash.get('ordering', [])
    
        TM_BUNDLES[self.name] = self

def main():
    # TEST, TEST
    from pprint import pprint
    pprint(syntax.TM_SYNTAXES)
    pprint(snippet.TM_SNIPPETS)

if __name__ == '__main__':
    main()

