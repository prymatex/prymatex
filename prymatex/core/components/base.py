#!/usr/bin/env python
# -*- coding: utf-8 -*-

#http://pyqt.sourceforge.net/Docs/PyQt5/multiinheritance.html#ref-cooperative-multiinheritance

class PrymatexComponent(object):
    def __init__(self, **kwargs):
        super(PrymatexComponent, self).__init__(**kwargs)
        self._components = []

    def initialize(self, **kwargs):
        pass
    
    def finalize(self, **kwargs):
        pass

    def components(self):
        return self._components
 
    def addComponent(self, component):
        self._components.append(component)

    @classmethod
    def contributeToSettings(cls):
        """Class contributions to the settings dialog"""
        return []

    @classmethod
    def contributeToMainMenu(cls):
        if hasattr(super(PrymatexComponent, cls), 'contributeToMainMenu'):
            return super(PrymatexComponent, cls).contributeToMainMenu()
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

class PrymatexAddon(PrymatexComponent):
    def contributeToContextMenu(self, **kwargs):
        if hasattr(super(PrymatexAddon, self), 'contributeToContextMenu'):
            return super(PrymatexAddon, self).contributeToContextMenu(**kwargs)
        return []

class PrymatexComponentWidget(PrymatexComponent):
    def addons(self):
        return filter(lambda ch: isinstance(ch, PrymatexAddon), self.components())