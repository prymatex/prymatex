#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, glob
import plistlib
import syntax

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
    raise ItemDoesNotExist();

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

  @classmethod
  def load(cls, bundle_path):
    #Info
    info_file = os.path.join(bundle_path, 'info.plist')
    data = plistlib.readPlist(info_file)
    bundle = Bundle(**data)

    #Syntaxes
    syntax_files = glob.glob(os.path.join(bundle_path, 'Syntaxes', '*'))
    for sf in syntax_files:
      data = plistlib.readPlist(sf)
      syntax.SyntaxNode(data, None, bundle.name)

    '''for item in FOO_BAR:
      item_abspath = os.path.join(bundle_abspath, item.path_name)
      if os.path.exists(item_abspath):
	for file in filter(lambda x: not x.startswith('.'), os.listdir(item_abspath)):
	  print os.path.join(item_abspath, file)
	  data = plistlib.readPlist(os.path.join(item_abspath, file))
	  element = item(**data)'''

def main():
  paths = glob.glob('./Bundles/*.tmbundle')
  for path in paths:
    bundle = Bundle.load(os.path.abspath(path))
  
  # TEST, TEST
  from pprint import pprint
  pprint(syntax.SYNTAXES)

if __name__ == '__main__':
  main()

