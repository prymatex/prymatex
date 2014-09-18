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
        self.customComponentObjects = {}
    
    def update(self, klass, instance):
        objects = self.customComponentObjects.get(klass, [])
        test_actions(instance, 
            filter(lambda obj: isinstance(obj, QtWidgets.QAction), objects))
        
    # Extend Main Menu
    def extend(self, klass, parent = None):
        menuExtensions = issubclass(klass, PrymatexComponent) and klass.contributeToMainMenu() or None
        if menuExtensions is not None:
            objects = []
            for name, settings in menuExtensions.items():
                if not settings:
                    continue

                # Find parent menu
                parentMenu = self.parent().findChild(QtWidgets.QMenu, 
                    text_to_objectname(name, prefix = "menu"))
                # Extend
                if parentMenu is not None:
                    # Fix menu extensions
                    if not isinstance(settings, list):
                        settings = [ settings ]
                    objects += extend_menu(parentMenu, settings,
                        dispatcher = self.componentInstanceDispatcher,
                        sequence_handler = partial(self.registerShortcut, klass),
                        icon_handler = partial(self.registerIcon, klass))
                else:
                    objs = create_menu(parent, settings,
                        dispatcher = self.componentInstanceDispatcher,
                        allObjects = True,
                        sequence_handler = partial(self.registerShortcut, klass),
                        icon_handler = partial(self.registerIcon, klass))
                    add_actions(self, [ objs[0] ], settings.get("before", None))
                    objects += objs

            # Store all new objects from creation or extension
            self.customComponentObjects.setdefault(klass, []).extend(objects)

            for componentClass in self.parent().application().pluginManager.findComponentsForClass(klass):
                self.extend(componentClass, parent)

    def componentInstanceDispatcher(self, handler, *args):
        obj = self.sender()
        componentClass = None
        for cmpClass, objects in self.customComponentObjects.items():
            if obj in objects:
                componentClass = cmpClass
                break

        componentInstances = [ self.parent() ]
        for componentClass in self.parent().application().componentHierarchyForClass(componentClass):
            componentInstances = reduce(
                lambda ai, ci: ai + ci.findChildren(componentClass),
                componentInstances, [])

        widget = self.parent().application().focusWidget()
        self.parent().logger().debug("Trigger %s over %s" % (obj, componentInstances))

        # TODO Tengo todas pero solo se lo aplico a la ultima que es la que generalmente esta en uso
        handler(componentInstances[-1], *args)

    def registerShortcut(self, *args, **kwargs):
        self.parent().application().registerShortcut(*args, **kwargs)
        
    def registerIcon(self, *args, **kwargs):
        self.parent().application().registerIcon(*args, **kwargs)
