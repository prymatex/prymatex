#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from prymatex import resources
from prymatex.core.plugin import PMXBaseWidgetComponent

class PMXBaseDialog(PMXBaseWidgetComponent):
    def __init__(self):
        PMXBaseWidgetComponent.__init__(self)
        
    def setParameters(self, parameters):
        pass