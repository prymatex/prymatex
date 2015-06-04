#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.utils import text as textutils
#http://pyqt.sourceforge.net/Docs/PyQt5/multiinheritance.html#ref-cooperative-multiinheritance

class PrymatexComponent(object):
    def __init__(self, *args, **kwargs):
        super(PrymatexComponent, self).__init__(*args, **kwargs)
        self._components = []
        self._commands = {}

    def initialize(self, *args, **kwargs):
        pass
    
    def finalize(self, *args, **kwargs):
        pass

    # --------- Component API    
    def components(self):
        return self._components
 
    def addComponent(self, component):
        self._components.append(component)

    # --------- Command API
    def commands(self):
        return self._commands

    def addCommand(self, string, command):
        self._commands[string] = command
        
    def addCommandsByName(self):
        for method in dir(self):
            if method.startswith("command_"):
                name = "_".join(textutils.camelcase_to_text(method[8:]).split())
                self.addCommand(name, getattr(self, method))

    def runCommand(self, string, **kwargs):
        command = self._commands[string]
        getattr(command, "run", command)(**kwargs)

    @classmethod
    def contributeToSettings(cls):
        """Class contributions to the settings dialog"""
        return []

    @classmethod
    def contributeToMainMenu(cls):
        return {}

    def contributeToShortcuts(self):
        return []
        
    def environmentVariables(self):
        """Return a dictionary with the defined variables of this component."""
        return {}

    # Save an restore component state
    def componentState(self):
        """Returns a Python dictionary containing the state of the component."""
        components = {}
        for component in self.components():
            componentState = component.componentState()
            if componentState:
                components[component.objectName()] = componentState
        
        return components and {"components": components } or {}

    def setComponentState(self, componentState):
        """Restore the state from the given state (returned by a previous call to saveState())."""
        if "components" in componentState:
            for component in self.components():
                componentName = component.objectName()
                if componentName in componentState["components"]:
                    component.setComponentState(componentState["components"][componentName])

class PrymatexCommand(object):
    def run(self, edit, *args, **kwargs):
        pass
    
    def is_enabled(self, *args, **kwargs):
        pass
        
    def is_visible(self, *args, **kwargs):
        pass

    def description(self, *args, **kwargs):
        pass
        
class PrymatexAddon(PrymatexComponent):
    def contributeToContextMenu(self, *args, **kwargs):
        return []

class PrymatexComponentWidget(PrymatexComponent):
    def addons(self):
        return filter(lambda ch: isinstance(ch, PrymatexAddon), self.components())
        
    def findAddon(self, klass):
        return next((addon for addon in self.addons() if isinstance(addon, klass)))
