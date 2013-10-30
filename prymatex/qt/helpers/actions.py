#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from prymatex.qt.helpers.base import text2objectname

from prymatex.utils import programs
import collections

def toggle_actions(actions, enable):
    """Enable/disable actions"""
    if actions is not None:
        for action in actions:
            if action is not None:
                action.setEnabled(enable)

def create_action(parent, settings, connect = True):
    """Create a QAction"""
    text = settings.get("text")
    action = QtGui.QAction(text, parent)
    name = settings.get("name", text)
    action.setObjectName(text2objectname(name, prefix = "action"))
    
    # attrs
    if "icon" in settings:
        action.setIcon(settings["icon"])
    if "shortcut" in settings:
        action.setShortcut(settings["shortcut"])
    if "tip" in settings:
        action.setToolTip(settings["tip"])
        action.setStatusTip(settings["tip"])
    if "data" in settings:
        action.setData(settings["data"])
    if "menurole" in settings:
        action.setMenuRole(settings["menurole"])
    # TODO Deprecated checkable by default if has testChecked key the action is checkable
    if "checkable" in settings or "testChecked" in settings:
        action.setCheckable("testChecked" in settings or settings["checkable"])
    
    # Action functions
    action.functionTriggered = action.functionToggled = None
    if "triggered" in settings and isinstance(settings["triggered"], collections.Callable):
        action.functionTriggered = settings["triggered"]
    if "toggled" in settings and isinstance(settings["toggled"], collections.Callable):
        action.functionToggled = settings["toggled"]
        action.setCheckable(True)

    if connect and action.functionTriggered:
        parent.connect(action, 
            QtCore.SIGNAL("triggered()"),
            isinstance(connect, collections.Callable) and connect or action.functionTriggered)

    if connect and action.functionToggled:
        parent.connect(action, 
            QtCore.SIGNAL("toggled(bool)"),
            isinstance(connect, collections.Callable) and connect or action.functionToggled)

    # Test functions
    if "testChecked" in settings and isinstance(settings["testChecked"], collections.Callable):
        action.testChecked = settings["testChecked"]
    if "testEnabled" in settings and isinstance(settings["testEnabled"], collections.Callable):
        action.testEnabled = settings["testEnabled"]
    if "testVisible" in settings and isinstance(settings["testVisible"], collections.Callable):
        action.testVisible = settings["testVisible"]
    
    #TODO: Hard-code all shortcuts and choose context=QtCore.Qt.WidgetShortcut
    # (this will avoid calling shortcuts from another dockwidget
    #  since the context thing doesn't work quite well with these widgets)
    action.setShortcutContext(settings.get("context", QtCore.Qt.WindowShortcut))
    
    return action


def create_bookmark_action(parent, url, text, icon=None, shortcut=None):
    """Create bookmark action"""
    return create_action( parent, {"text": text, "shortcut":shortcut, "icon":icon,
                          "triggered":lambda u=url: programs.start_file(u)})


def create_module_bookmark_actions(parent, bookmarks):
    """
    Create bookmark actions depending on module installation:
    bookmarks = ((module_name, url, title, icon), ...)
    """
    actions = []
    for key, url, title, icon in bookmarks:
        if programs.is_module_installed(key):
            act = create_bookmark_action(parent, url, title, icon)
            actions.append(act)
    return actions


def create_program_action(parent, text, icon, name, nt_name=None):
    """Create action to run a program"""
    if os.name == 'nt' and nt_name is not None:
        name = nt_name
    path = programs.find_program(name)
    if path is not None:
        return create_action(parent, {"text": text, "icon": icon,
                             "triggered": lambda: programs.run_program(name)})

        
def create_python_script_action(parent, text, icon, package, module, args=[]):
    """Create action to run a GUI based Python script"""
    if programs.python_script_exists(package, module):
        return create_action(parent, {"text": text, "icon":icon,
                             "triggered":lambda:
                             programs.run_python_script(package, module, args)})
