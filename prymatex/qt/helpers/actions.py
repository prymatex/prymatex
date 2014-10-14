#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.utils import programs

from .base import text_to_objectname
from .icons import text_to_iconname
from .keysequences import text_to_sequencesname

def toggle_actions(actions, enable):
    """Enable/disable actions"""
    if actions is not None:
        for action in actions:
            if action is not None:
                action.setEnabled(enable)

def test_actions(instance, actions):
    for action in actions:
        # Prevent signals
        action.setVisible(not hasattr(action, "testVisible") or \
            action.testVisible(instance))
        action.setEnabled(not hasattr(action, "testEnabled") or \
            action.testEnabled(instance))
        if action.isCheckable():
            action.setChecked(hasattr(action, "testChecked") and \
                action.testChecked(instance))

def create_action(parent, settings, dispatcher = None, sequence_handler=None, icon_handler=None):
    """Create a QAction"""
    text = settings.get("text")
    action = QtWidgets.QAction(text, parent)
    action.setObjectName(text_to_objectname(text, prefix="action"))
    
    icon = settings.get("icon", text_to_iconname(text))
    if icon_handler is not None:
        icon_handler(action, icon)
    elif isinstance(icon, QtGui.QIcon) and not icon.isNull():
        action.setIcon(icon)

    sequence = settings.get("sequence", text_to_sequencesname(text))
    if sequence_handler is not None:
        sequence_handler(action, sequence)
    elif isinstance(sequence, QtGui.QKeySequence) and not sequence.isEmpty():
        action.setShortcut(sequence)

    if "tip" in settings:
        action.setToolTip(settings["tip"])
        action.setStatusTip(settings["tip"])

    if "data" in settings:
        action.setData(settings["data"])

    if "menurole" in settings:
        action.setMenuRole(settings["menurole"])

    if "context" in settings:
        action.setShortcutContext(settings["context"])
    
    # The signal dispatcher
    def dispatch_signal(dispatcher, handler):
        def _dispatch(*largs):
            dispatcher(handler, *largs)
        return _dispatch

    # Action functions
    action.functionTriggered = None
    if "triggered" in settings and isinstance(settings["triggered"], collections.Callable):
        action.functionTriggered = isinstance(dispatcher, collections.Callable) and \
            dispatch_signal(dispatcher, settings["triggered"]) or \
            settings["triggered"]
    action.setCheckable(settings.get("checkable", False))

    if action.functionTriggered is not None:
        action.triggered.connect(action.functionTriggered)

    # Test functions
    if "testChecked" in settings and isinstance(settings["testChecked"], collections.Callable):
        action.testChecked = settings["testChecked"]
    if "testEnabled" in settings and isinstance(settings["testEnabled"], collections.Callable):
        action.testEnabled = settings["testEnabled"]
    if "testVisible" in settings and isinstance(settings["testVisible"], collections.Callable):
        action.testVisible = settings["testVisible"]
    
    return action


def add_actions(target, actions, before=None, prefix=""):
    """Add actions to a menu"""
    # Convert before to action
    before_action = None
    if before:
        objectName = text_to_objectname(before, prefix=prefix)
        before_action = next((ta for ta in target.actions() if ta.objectName() == objectName), None)
    for action in actions:
        if isinstance(action, QtWidgets.QMenu):
            if before_action is None:
                target.addMenu(action)
            else:
                target.insertMenu(before_action, action)
        elif isinstance(action, QtWidgets.QAction):
            if before_action is None:
                target.addAction(action)
            else:
                target.insertAction(before_action, action)


def create_bookmark_action(parent, url, text, icon=None, sequence=None):
    """Create bookmark action"""
    return create_action( parent, {"text": text, "sequence":sequence, "icon":icon,
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
