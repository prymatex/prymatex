#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex.core.components.base import PMXBaseWidgetComponent

__all__ = ["PMXBaseDialog"]

# TODO: separar estos dialogos de los que se pueden generar desde el servidor remoto?
class PMXBaseDialog(PMXBaseWidgetComponent):
    def __init__(self):
        PMXBaseWidgetComponent.__init__(self)
        
    def setParameters(self, parameters):
        pass

    def waitForInput(self, callback):
        pass
    
    def execModal(self):
        pass