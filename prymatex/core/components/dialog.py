#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex.core.components.base import PMXBaseComponent

__all__ = ["PMXBaseDialog"]

# TODO: separar estos dialogos de los que se pueden generar desde el servidor remoto?
class PMXBaseDialog(PMXBaseComponent):
    def initialize(self, mainWindow):
        PMXBaseComponent.initialize(self, mainWindow)
        self.mainWindow = mainWindow
        
    def setParameters(self, parameters):
        pass

    def waitForInput(self, callback):
        pass
    
    def execModal(self):
        pass