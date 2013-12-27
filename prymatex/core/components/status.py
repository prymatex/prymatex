#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex.core.components.base import PMXBaseComponent

__all__ = ["PMXBaseStatusBar"]

class PMXBaseStatusBar(PMXBaseComponent):    
    def initialize(self, mainWindow):
        PMXBaseComponent.initialize(self, mainWindow)
        self.mainWindow = mainWindow

    def acceptEditor(self, editor):
        return False
