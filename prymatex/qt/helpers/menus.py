#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Create QMenu
Handle dictionary's menu format

settings = {
    "text": "Menu Title",
    "icon": "resourece icon key"
    "items": [
        action1, action2,
        {"text": "SubMenu Title",
         "items": [
            (gaction1, qaction2, qaction3), # Create Action Group, Exclusive = True
            [gaction1, qaction2, qaction3], # Create ACtion Group, Exclusive = False
            { 'text': "Action Title",       # Create action whit callback
              "sortcut": 'F20',
              "icon": ....,
              'callback': ....},
            "-",                            # Add separator
            action1,
            "--Section",                            # Add named separator
            action2
        ]}
        action3, "-", action4
    ]
}

"""

from prymatex.qt import QtCore, QtGui

from prymatex.qt.helpers.base import text2objectname
from prymatex.qt.helpers.actions import create_action

def create_menu(parent, settings, useSeparatorName = False, connectActions = False):
    text = settings.get("text", "Menu")
    menu = QtGui.QMenu(text, parent)
    name = settings.get("name", text)
    menu.setObjectName(text2objectname(name, prefix = "menu"))

    # attrs
    if "icon" in settings:
        menu.setIcon(settings["icon"])

    actions = []
    if isinstance(parent, QtGui.QMenu):
        menuAction = parent.addMenu(menu)
        if "testEnabled" in settings:
            menuAction.testEnabled = settings["testEnabled"]
        if "testVisible" in settings:
            menuAction.testVisible = settings["testVisible"]

    # actions
    actions += extend_menu(menu, settings.get("items", []), useSeparatorName = useSeparatorName)
    if connectActions:
        for action in actions:
            if hasattr(action, 'callback'):
                if action.isCheckable():
                    parent.connect(action, QtCore.SIGNAL('triggered(bool)'), action.callback)
                else:
                    parent.connect(action, QtCore.SIGNAL('triggered()'), action.callback)

    return menu, actions

def extend_menu(menu, items, useSeparatorName = False):
    actions = []
    for item in items:
        if item == "-":
            action = menu.addSeparator()
            actions.append(action)
        elif isinstance(item, str) and item.startswith("--"):
            name = item[item.rfind("-") + 1:]
            action = menu.addSeparator()
            action.setObjectName(text2objectname(name, prefix = "section"))
            if useSeparatorName:
                action.setText(name)
            actions.append(action)
        elif isinstance(item, dict) and 'items' in item:
            submenu, subactions = create_menu(menu, item)
            actions.extend(subactions)
        elif isinstance(item, dict):
            action = create_action(menu, item)
            actions.append(action)
            menu.addAction(action)
        elif isinstance(item, QtGui.QAction):
            menu.addAction(item)
        elif isinstance(item, QtGui.QMenu):
            menu.addMenu(item)
        elif isinstance(item, list):
            actionGroup = QtGui.QActionGroup(menu)
            actions.append(actionGroup)
            actionGroup.setExclusive(False)
            list(map(menu.addAction, item))
            list(map(lambda action: action.setActionGroup(actionGroup), item))
        elif isinstance(item, tuple):
            actionGroup = QtGui.QActionGroup(menu)
            actions.append(actionGroup)
            actionGroup.setExclusive(True)
            list(map(menu.addAction, item))
            list(map(lambda action: action.setActionGroup(actionGroup), item))
        else:
            raise Exception("%s" % item)
    return actions

def add_actions(target, actions, insert_before=None):
    """Add actions to a menu"""
    previous_action = None
    target_actions = list(target.actions())
    if target_actions:
        previous_action = target_actions[-1]
        if previous_action.isSeparator():
            previous_action = None
    for action in actions:
        if (action is None) and (previous_action is not None):
            if insert_before is None:
                target.addSeparator()
            else:
                target.insertSeparator(insert_before)
        elif isinstance(action, QtGui.QMenu):
            if insert_before is None:
                target.addMenu(action)
            else:
                target.insertMenu(insert_before, action)
        elif isinstance(action, QtGui.QAction):
            if insert_before is None:
                target.addAction(action)
            else:
                target.insertAction(insert_before, action)
        previous_action = action

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
