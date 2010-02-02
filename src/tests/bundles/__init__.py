#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import plistlib
from bundles.syntax import SyntaxNode
from pprint import pprint

class Menu(object):
  def __init__(self, name, items, submenus = {}, excludedItems = []):
    self.name = name
    self.main = dict(map(lambda i: (i, None), filter(lambda x: x != '-' * 36, items)))
    for uuid, submenu in submenus.iteritems():
      self[uuid] = Menu(**submenu)

  def __contains__(self, key):
    return key in self.main or any(map(lambda submenu: key in submenu, filter(lambda x: isinstance(x, Menu), self.main.values())))

  def __getitem__(self, key):
    try:
      return self.main[key]
    except KeyError:
      for submenu in filter(lambda x: isinstance(x, Menu), self.main.values()):
    if key in submenu:
      return submenu[key]
      raise ItemDoesNotExist();

  def __setitem__(self, key, menu):
    if key in self.main:
      self.main[key] = menu
    else:
      for submenu in filter(lambda x: isinstance(x, Menu), self.main.values()):
    if key in submenu:
      submenu[key] = menu

class Bundle(object):
  def __init__(self, uuid, name, description, contactName, contactEmailRot13, mainMenu, deleted, ordering):
    self.uuid = uuid
    self.name = name
    self.description = description
    self.contact = {'Name': contactName, 'Email': contactEmailRot13 }
    self.menu = Menu('main', **mainMenu)

  @classmethod
  def load(cls, name):
    bundle_abspath = os.path.join(os.path.abspath(os.curdir), name + '.tmbundle')
    info_file = os.path.join(bundle_abspath, 'info.plist')
    data = plistlib.readPlist(info_file)
    bundle = Bundle(**data)
    for item in FOO_BAR:
      item_abspath = os.path.join(bundle_abspath, item.path_name)
      if os.path.exists(item_abspath):
    for file in filter(lambda x: not x.startswith('.'), os.listdir(item_abspath)):
      print os.path.join(item_abspath, file)
      data = plistlib.readPlist(os.path.join(item_abspath, file))
      element = item(**data)

def main():
  bundle = Bundle.load('PHP')

if __name__ == '__main__':
  main()

