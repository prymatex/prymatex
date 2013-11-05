#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections

# TODO: No son Mixin?

class PMXBaseComponent(object):
    def initialize(self, parent):
        pass
    
    def finalize(self):
        pass

    def components(self):
        return []
 
    def addComponent(self, component):
        pass

    @classmethod
    def contributeToSettings(cls):
        """Class contributions to the settings dialog"""
        return []

    @classmethod
    def contributeToMainMenu(cls):
        """Contributions to the main menu
        return OrderedDict, the keys are strings and the values are lists
            keys define the name of te menu to be extended
            values define the extensions to the found menu"""
        return collections.OrderedDict()

    def environmentVariables(self):
        """Return a dictionary with the defined variables of this component."""
        return {}

    def componentState(self):
        """Returns a Python dictionary containing the state of the component."""
        return {}

    def setComponentState(self, state):
        """Restore the state from the given state (returned by a previous call to saveState())."""
        pass
