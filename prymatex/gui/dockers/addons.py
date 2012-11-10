#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from prymatex.core import PMXBaseDockAddon

#========================================
# BASE PROJECT ADDON
#========================================
class ProjectDockAddon(QtCore.QObject, PMXBaseDockAddon):
    def __init__(self, parent):
        QtCore.QObject.__init__(self, parent)
        
    def contributeToContextMenu(self, node):
        return []