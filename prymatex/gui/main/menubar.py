# encoding: utf-8

"""This module contains the main window menu bar definition and widgets."""
from functools import reduce, partial

from prymatex.qt import QtGui, QtWidgets
from prymatex.qt.helpers import (text_to_objectname, extend_menu, add_actions, 
    test_actions, create_menu)

from prymatex.core import PrymatexComponent

class PrymatexMainMenuBar(QtWidgets.QMenuBar):
    def __init__(self, **kwargs):
        super(PrymatexMainMenuBar, self).__init__(**kwargs)
        self.componentActions = {}
        self.window().currentEditorChanged.connect(self.on_currentEditorChanged)

    def _instances(self, componentClass):
        componentInstances = [ self.window() ]
        for componentClass in self.window().application().componentHierarchyForClass(componentClass):
            componentInstances = reduce(
                lambda ai, ci: ai + ci.findChildren(componentClass),
                componentInstances, [])
        return componentInstances
    
    def _instance(self, componentClass):
        # El ultimo es el que tiene el foco
        instances = self._instances(componentClass)
        return instances and instances[-1]

    def on_menu_aboutToShow(self, componentClass, objects):
        instance = self._instance(componentClass)
        if instance:
            test_actions(instance, objects)

    def on_currentEditorChanged(self, editor):
        components = [ self.window().__class__ ]
        if editor is not None:
            components.append(editor.__class__)
            components.extend(self.window().application().findComponentsForClass(
                editor.__class__)
            )
        # TODO Hacer que funcione para todos los compoenentes
        return 
        for klass, actions in self.componentActions.items():
            [ action.setEnabled(klass in components) for action in actions ]

    # Extend Main Menu
    def extend(self, klass, parent = None):
        # Build handlers
        dispatcher = partial(self.componentInstanceDispatcher, klass)
        sequence_handler = partial(self.registerShortcut, klass)
        icon_handler = partial(self.registerIcon, klass)
        
        menuExtensions = issubclass(klass, PrymatexComponent) and \
            klass.contributeToMainMenu() or {}
        for name, settings in menuExtensions.items():
            # Find parent menu
            menu = self.parent().findChild(QtWidgets.QMenu, 
                text_to_objectname(name, prefix = "menu"))

            # Extend menu or create new one 
            if menu is None:
                menu, objects = create_menu(parent, settings,
                    dispatcher = dispatcher,
                    sequence_handler = sequence_handler,
                    icon_handler = icon_handler)
                add_actions(self, [ menu ], settings.get("before", None), prefix="actionMenu")
            else:
                objects = extend_menu(menu,
                    isinstance(settings, (list, tuple)) and settings or [settings],
                    dispatcher = dispatcher,
                    sequence_handler = sequence_handler,
                    icon_handler = icon_handler)
            
            menu.aboutToShow.connect(
                lambda klass=klass, objects=objects: self.on_menu_aboutToShow(klass, objects)
            )

        # Store all actions for component
        # self.componentActions.setdefault(klass, []).extend(actions + [m.menuAction() for m in menus])
        
        for componentClass in self.parent().application().pluginManager.findComponentsForClass(klass):
            self.extend(componentClass, parent)

    def componentInstanceDispatcher(self, componentClass, handler, *args):
        instance = self._instance(componentClass)
        self.parent().logger().debug("Trigger %s over %s" % (
            self.sender(), instance))

        handler(instance, *args)

    def registerShortcut(self, *args, **kwargs):
        self.parent().application().registerShortcut(*args, **kwargs)
        
    def registerIcon(self, *args, **kwargs):
        self.parent().application().registerIcon(*args, **kwargs)
