#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fnmatch
import uuid as uuidmodule
from PyQt4 import QtCore, QtGui
from prymatex.core.base import PMXObject
from prymatex.core.settings import pmxConfigPorperty
from prymatex.gui.project.models import PMXProjectTreeModel

class PMXProjectManager(PMXObject):
    #Signals
    
    #Settings
        
    SETTINGS_GROUP = 'ProjectManager'
    
    def __init__(self, parent = None):
        PMXObject.__init__(self)
        self.projectTreeModel = PMXProjectTreeModel(self)
        self.projectTreeModel.addProject("workspace", "/home/diego/workspace")
        self.projectTreeModel.addProject("home", "/home/diego")
        self.configure()
