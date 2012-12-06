#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from prymatex.qt.helpers.base import text2objectname

from prymatex.utils import programs

def toggle_actions(actions, enable):
    """Enable/disable actions"""
    if actions is not None:
        for action in actions:
            if action is not None:
                action.setEnabled(enable)


def create_action(parent, settings):
    """Create a QAction"""
    text = settings.get("text", "Action")
    action = QtGui.QAction(text, parent)
    action.setObjectName(text2objectname(text, prefix = "action"))
    
    # attrs
    if settings.has_key("icon"):
        action.setIcon(settings["icon"])
    if settings.has_key("shortcut"):
        action.setShortcut(settings["shortcut"])
    if settings.has_key("tip"):
        action.setToolTip(settings["tip"])
        action.setStatusTip(settings["tip"])
    if settings.has_key("data"):
        action.setData(settings["data"])
    if settings.has_key("menurole"):
        action.setMenuRole(settings["menurole"])
    if settings.has_key("checkable"):
        action.setCheckable(settings["checkable"])
    
    # callables
    if settings.has_key("callback"):
        action.callback = settings["callback"]
    if settings.has_key("testChecked"):
        action.testChecked = settings["testChecked"]
    
    if settings.has_key("triggered") and callable(settings["triggered"]):
        parent.connect(action, QtCore.SIGNAL("triggered()"), settings["triggered"])
    if settings.has_key("toggled") and callable(settings["toggled"]):
        parent.connect(action, QtCore.SIGNAL("toggled(bool)"), settings["toggled"])
        action.setCheckable(True)
        
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
