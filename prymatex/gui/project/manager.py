#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import fnmatch

from PyQt4 import QtCore, QtGui
from prymatex.core.base import PMXObject
from prymatex.core.settings import USER_HOME_PATH
from prymatex.core.settings import pmxConfigPorperty
from prymatex.gui.project.models import PMXProjectTreeModel
from prymatex.gui.project.base import PMXProject

class PMXProjectManager(QtGui.QWidget, PMXObject):
    #Signals
    projectClosed = QtCore.pyqtSignal(object)
    projectOpened = QtCore.pyqtSignal(object)
    
    #Settings
    workspacePath  = pmxConfigPorperty(default = os.path.join(USER_HOME_PATH, "workspace"))  #Eclipse muejejeje
    projects = pmxConfigPorperty(default = [])
    
    SETTINGS_GROUP = 'ProjectManager'
    
    def __init__(self, parent = None):
        PMXObject.__init__(self)
        self.projectTreeModel = PMXProjectTreeModel(self)
        self.configure()

    def openProject(self):
        pass

    def createProject(self):
        # Mostrar Dialogo
        pass

    def deleteProject(self):
        pass

