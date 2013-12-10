#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Create QMenu
Handle dictionary's menu format
"""

from prymatex.qt import QtCore, QtGui

from prymatex.qt.helpers.base import text2objectname
from prymatex.qt.helpers.actions import create_action

import collections

def create_menu(parent, settings, dispatcher = None, separatorName = False, allObjects = False, sequence_handler = None):
    menu = QtGui.QMenu(settings["text"], parent)
    
    menu.setObjectName(text2objectname(
        settings.get("name", settings["text"]), prefix = "menu"))
    menu.menuAction().setObjectName(text2objectname(
        settings.get("name", settings["text"]), prefix = "actionMenu"))

    # attrs
    if "icon" in settings:
        menu.setIcon(settings["icon"])

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
        parent.connect(menu, QtCore.SIGNAL("triggered(QAction)"),
            isinstance(dispatcher, collections.Callable) and \
            dispatch_signal(dispatcher, menu.functionTriggered) or \
            menu.functionTriggered)

    if menu.functionAboutToHide is not None:
        parent.connect(menu, QtCore.SIGNAL("aboutToHide()"),
            isinstance(dispatcher, collections.Callable) and \
            dispatch_signal(dispatcher, menu.functionAboutToHide) or \
            menu.functionAboutToHide)

    if menu.functionAboutToShow is not None:
        parent.connect(menu, QtCore.SIGNAL("aboutToShow()"),
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
        sequence_handler = sequence_handler)

    return allObjects and objects or menu

def extend_menu(rootMenu, settings, dispatcher = None, separatorName = False, sequence_handler = None):
    collectedObjects = [ rootMenu ]
    for item in settings:
        objects = None
        if item == "-":
            objects = rootMenu.addSeparator()
            objects.setObjectName(text2objectname("None", prefix = "separator"))
        elif isinstance(item, str) and item.startswith("--"):
            name = item[item.rfind("-") + 1:]
            objects = rootMenu.addSeparator()
            objects.setObjectName(text2objectname(name, prefix = "separator"))
            if separatorName:
                objects.setText(name)
        elif isinstance(item, dict) and 'items' in item:
            objects = create_menu(rootMenu.parent(), item,
                dispatcher = dispatcher,
                separatorName = separatorName,
                allObjects = True,
                sequence_handler = sequence_handler)
            add_actions(rootMenu, [ objects[0] ], item.get("before", None))
        elif isinstance(item, dict):
            objects = create_action(rootMenu.parent(), item,
                dispatcher = dispatcher, 
                sequence_handler = sequence_handler)
            add_actions(rootMenu, [ objects ], item.get("before", None))
        elif isinstance(item, QtGui.QAction):
            rootMenu.addAction(item)
            objects = item
        elif isinstance(item, QtGui.QMenu):
            objects = rootMenu.addMenu(item)
        elif isinstance(item, (tuple, list)):
            actionGroup = QtGui.QActionGroup(rootMenu.parent())
            actionGroup.setExclusive(isinstance(item, tuple))
            objects = []
            for action in item:
                if isinstance(action, dict):
                    action = create_action(rootMenu.parent(), action,
                        dispatcher = dispatcher, 
                        sequence_handler = sequence_handler)
                if action == "-":
                    action = rootMenu.addSeparator()
                    action.setObjectName(text2objectname("None", prefix = "separator"))
                elif isinstance(action, str) and action.startswith("--"):
                    name = action[action.rfind("-") + 1:]
                    action = rootMenu.addSeparator()
                    action.setObjectName(text2objectname(name, prefix = "separator"))
                    if separatorName:
                        action.setText(name)
                else:
                    rootMenu.addAction(action)
                    action.setActionGroup(actionGroup)
                objects.append(action)
        else:
            raise Exception("%s" % item)
        if objects is not None:
            getattr(collectedObjects, isinstance(objects, (tuple, list)) and "extend" or "append")(objects)
    return collectedObjects

def add_actions(target, actions, before=None):
    """Add actions to a menu"""
    # Convert before to action
    before_action = None
    if before:
        objectName = text2objectname(before, prefix = "actionMenu")
        before_action = next((ta for ta in target.actions() if ta.objectName() == objectName), None)
    for action in actions:
        if isinstance(action, QtGui.QMenu):
            if before_action is None:
                target.addMenu(action)
            else:
                target.insertMenu(before_action, action)
        elif isinstance(action, QtGui.QAction):
            if before_action is None:
                target.addAction(action)
            else:
                target.insertAction(before_action, action)

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

def extend_menu_section(menu, newItems, section = 0, position = None):
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
