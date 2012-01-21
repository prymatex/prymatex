#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from prymatex.core.plugin import PMXBaseWidgetPlugin

class PMXBaseStatusBar(PMXBaseWidgetPlugin):
    def acceptEditor(self, editor):
        return False
    
    def setCurrentEditor(self, editor):
        pass
    
    def setMainWindow(self, mainWindow):
        self.mainWindow = mainWindow