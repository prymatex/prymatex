#!/usr/bin/env python
# -*- coding: utf-8 -*-

#http://pyqt.sourceforge.net/Docs/PyQt5/multiinheritance.html#ref-cooperative-multiinheritance

class PrymatexComponent(object):
    def __init__(self, **kwargs):
        super(PrymatexComponent, self).__init__(**kwargs)
        
    def initialize(self, **kwargs):
        pass
    
    def finalize(self, **kwargs):
        pass

    def components(self):
        return filter(lambda ch: isinstance(ch, PrymatexComponent), self.children())
 
    def addComponent(self, component):
        pass

    @classmethod
    def contributeToSettings(cls):
        """Class contributions to the settings dialog"""
        return []

    @classmethod
    def contributeToMainMenu(cls):
        if hasattr(super(PrymatexComponent, cls), 'contributeToMainMenu'):
            return super(PrymatexComponent, cls).contributeToMainMenu()

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
        for component in self.components():
            componentName = component.objectName()
            if componentName in componentState["components"]:
                component.setComponentState(componentState["components"][componentName])


Key_Any = 0
class PrymatexKeyHelper(PrymatexComponent):
    KEY = Key_Any
    def accept(self, **kwargs):
        return True
    
    def execute(self, **kwargs):
        pass

class PrymatexAddon(PrymatexComponent):
    pass

class PrymatexComponentWidget(PrymatexComponent):
    def __init__(self, **kwargs):
        super(PrymatexComponentWidget, self).__init__(**kwargs)

    def addComponent(self, component):
        super(PrymatexComponentWidget, self).addComponent(component)
        if isinstance(component, PrymatexKeyHelper):
            self.addKeyHelper(component)
    
    @property
    def keyHelpers(self):
        try:
            return self._keyHelpers
        except AttributeError:
            self._keyHelpers = {}
            return self._keyHelpers
            
    def addKeyHelper(self, helper):
        try:
            self.keyHelpers.setdefault(helper.KEY, []).append(helper)
        except:
            self.keyHelpers = { helper.KEY: [ helper ]}

    def keyHelpersByClass(self, klass):
        return [keyHelper for keyHelper in self.keyHelpers[klass.KEY] if isinstance(keyHelper, klass)]
        
    def findHelpers(self, key):
        helpers = []
        if Key_Any in self.keyHelpers:
            helpers += self.keyHelpers[Key_Any]
        helpers += self.keyHelpers.get(key, [])
        return helpers

    def runKeyHelper(self, key = Key_Any, **kwargs):
        runHelper = False
        for helper in self.findHelpers(key):
            runHelper = helper.accept(**kwargs)
            if runHelper:
                helper.execute(**kwargs)
                break
        return runHelper
