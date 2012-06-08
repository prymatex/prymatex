#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex.core.plugin.addons import PMXDockBaseAddon

#========================================
# BASE PROJECT ADDON
#========================================
class ProjectDockAddon(QtCore.QObject, PMXDockBaseAddon):
    def __init__(self, parent):
        QtCore.QObject.__init__(self, parent)
        
    def contributeToContextMenu(self):
        pass