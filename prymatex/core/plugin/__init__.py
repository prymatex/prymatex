#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PyQt4 import QtCore, QtGui

#TODO: en inicialize deberia pasar un proveedro de servicios o otra forma menos directa de que un plguin hable con el core
class PMXBasePlugin(object):
    
    def initialize(self):
        raise NotImplemented
        
    def finalize(self):
        pass
    
class PMXBaseWidgetPlugin(PMXBasePlugin):
    def initialize(self, mainWindow):
        self.mainWindow = mainWindow
    
Key_Any = 0
class PMXBaseKeyHelper(PMXBasePlugin):
    KEY = Key_Any
    def accept(self, editor, event, cursor = None, scope = None):
        pass
    
    def execute(self, editor, event, cursor = None, scope = None):
        pass
    
class PMXBaseAddon(PMXBasePlugin):
    pass
