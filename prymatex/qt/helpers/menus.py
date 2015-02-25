#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Create QMenu
Handle dictionary's menu format
"""

from prymatex.qt import QtCore, QtGui, QtWidgets

from prymatex.qt.helpers.base import text_to_objectname
from prymatex.qt.helpers.icons import text_to_iconname
from prymatex.qt.helpers.actions import create_action, add_actions
from prymatex.utils import six

import collections

def create_menu(parent, settings, dispatcher = None, separatorName = False,
    sequence_handler = None, icon_handler=None):
    text = settings["text"]
    menu = QtWidgets.QMenu(text, parent)
    
    menu.setObjectName(text_to_objectname(text, prefix = "menu"))
    menu.menuAction().setObjectName(text_to_objectname(text, prefix = "actionMenu"))

    icon = settings.get("icon", text_to_iconname(text))
    if icon and icon_handler is not None:
        icon_handler(menu, icon)
    elif isinstance(icon, QtGui.QIcon) and not icon.isNull():
        menu.setIcon(icon)
    
    # Action functions
    menu.functionTriggered = menu.functionAboutToHide = menu.functionAboutToShow = None
    if "triggered" in settings and isinstance(settings["triggered"], collections.Callable):
        menu.functionTriggered = settings["triggered"]
    if "aboutToHide" in settings and isinstance(settings["aboutToHide"], collections.Callable):
        menu.functionAboutToHide = settings["aboutToHide"]
    if "aboutToShow" in settings and isinstance(settings["aboutToShow"], collections.Callable):
        menu.functionAboutToShow = settings["aboutToShow"]

    # The signal dispatcher
    def dispatch_signal(dispatcher, handler):
        def _dispatch(*largs):
            dispatcher(handler, *largs)
        return _dispatch

    if menu.functionTriggered is not None:
        menu.triggered[QtWidgets.QAction].connect(
            isinstance(dispatcher, collections.Callable) and \
            dispatch_signal(dispatcher, menu.functionTriggered) or \
            menu.functionTriggered)

    if menu.functionAboutToHide is not None:
        menu.aboutToHide.connect(
            isinstance(dispatcher, collections.Callable) and \
            dispatch_signal(dispatcher, menu.functionAboutToHide) or \
            menu.functionAboutToHide)

    if menu.functionAboutToShow is not None:
        menu.aboutToShow.connect(
            isinstance(dispatcher, collections.Callable) and \
            dispatch_signal(dispatcher, menu.functionAboutToShow) or \
            menu.functionAboutToShow)

    # The signal dispatcher
    if "testEnabled" in settings:
        menu.testEnabled = settings["testEnabled"]
    if "testVisible" in settings:
        menu.testVisible = settings["testVisible"]

    objects = extend_menu(menu,
        settings.get("items", []),
        dispatcher = dispatcher,
        separatorName = separatorName,
        sequence_handler = sequence_handler, 
        icon_handler = icon_handler)

    return menu, objects

def extend_menu(rootMenu, settings, dispatcher = None, separatorName = False, 
    sequence_handler = None, icon_handler = None):
    collectedObjects = []
    for item in settings:
        if item == "-":
            separator = rootMenu.addSeparator()
            separator.setObjectName(text_to_objectname("None", prefix = "separator"))
            collectedObjects.append(separator)
        elif isinstance(item, six.string_types) and item.startswith("--"):
            name = item[item.rfind("-") + 1:]
            separator = rootMenu.addSeparator()
            separator.setObjectName(text_to_objectname(name, prefix = "separator"))
            if separatorName:
                separator.setText(name)
            collectedObjects.append(separator)
        elif isinstance(item, dict) and 'items' in item:
            menu, objects = create_menu(rootMenu.parent(), item,
                dispatcher = dispatcher,
                separatorName = separatorName,
                sequence_handler = sequence_handler, 
                icon_handler = icon_handler)
            add_actions(rootMenu, [ menu ], item.get("before", None), prefix="actionMenu")
            collectedObjects.append(menu)
            collectedObjects.extend(objects)
        elif isinstance(item, dict):
            action = create_action(rootMenu.parent(), item,
                dispatcher = dispatcher, 
                sequence_handler = sequence_handler, 
                icon_handler = icon_handler)
            add_actions(rootMenu, [ action ], item.get("before", None), prefix="action")
            collectedObjects.append(action)
        elif isinstance(item, QtWidgets.QAction):
            rootMenu.addAction(item)
            collectedObjects.append(item)
        elif isinstance(item, QtWidgets.QMenu):
            rootMenu.addMenu(item)
            collectedObjects.append(item)
        elif isinstance(item, (tuple, list)):
            actionGroup = QtWidgets.QActionGroup(rootMenu.parent())
            actionGroup.setExclusive(isinstance(item, tuple))
            for action in item:
                if isinstance(action, dict):
                    action = create_action(rootMenu.parent(), action,
                        dispatcher = dispatcher, 
                        sequence_handler = sequence_handler,
                        icon_handler = icon_handler)
                if action == "-":
                    action = rootMenu.addSeparator()
                    action.setObjectName(text_to_objectname("None", prefix = "separator"))
                elif isinstance(action, str) and action.startswith("--"):
                    name = action[action.rfind("-") + 1:]
                    action = rootMenu.addSeparator()
                    action.setObjectName(text_to_objectname(name, prefix = "separator"))
                    if separatorName:
                        action.setText(name)
                else:
                    rootMenu.addAction(action)
                    action.setActionGroup(actionGroup)
                collectedObjects.append(action)
        else:
            raise Exception("%s" % item)
    return collectedObjects

# Sections
def _chunk_sections(items):
    sections = []
    start = 0
    for i in range(0, len(items)):
        if isinstance(items[i], str) and items[i].startswith('-') and start != i:
            sections.append(items[start:i])
            start = i
    sections.append(items[start:len(items)])
    return sections

def _section_name_range(items, name):
    begin, end = -1, -1
    for index, item in enumerate(items):
        if isinstance(item, str):
            if begin == -1 and item.startswith('-') and item.endswith(name):
                begin = index
            elif begin != -1 and item.startswith('-'):
                end = index
                break
    if begin == -1:
        raise Exception("Section %s not exists" % name)
    return begin, end

def _section_number_range(items, index):
    sections = _chunk_sections(items)
    section = sections[index]
    begin = items.index(section[0]) if section else 0
    end = items.index(section[-1]) + 1 if section else 1
    return begin, end

def extend_menu_section(menu, newItems, section=0, position=None):
    # TODO: Implementar algo para usar section = None, puedo ponerlo en cualquier lugar del menu con su posicion
    if not isinstance(newItems, list):
        newItems = [ newItems ]
    menuItems = menu.setdefault('items', [])
    #Ver si es un QMenu o una lista de items
    if isinstance(section, str):
        #Buscar en la lista la seccion correspondiente
        begin, end = _section_name_range(menuItems, section)
    elif isinstance(section, int):
        begin, end = _section_number_range(menuItems, section)
    newSection = menuItems[begin:end]
    if position is None:
        newSection += newItems
    else:
        if newSection and isinstance(newSection[0], str) and newSection[0].startswith("-"):
            position += 1
        newSection = newSection[:position] + newItems + newSection[position:]
    menu["items"] = menuItems[:begin] + newSection + menuItems[end:]

def update_menu(menuBase, menuUpdates):
    for name, update in menuUpdates.items():
        if isinstance(name, (list, tuple)):
            #Navegate
            menu = { "items": list(menuBase.values()) }
            for n in name:
                if not isinstance(menu, dict) or "items" not in menu:
                    return
                items = [item for item in menu["items"] if isinstance(item, dict) and "name" in item and item["name"] == n]
                if not items:
                    return
                menu = items.pop()
            position = update.pop('position', None)
            section = update.pop('section', 0)
            extend_menu_section(menu, update, section = section, position = position)
        else:
            if name not in menuBase:
                menuBase[name] = update
            else:
                position = update.pop('position', None)
                section = update.pop('section', 0)
                extend_menu_section(menuBase.get(name), update, section = section, position = position)
