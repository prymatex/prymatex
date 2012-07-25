#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from prymatex.core.plugin import PMXBaseWidgetComponent

class PMXBaseStatusBar(PMXBaseWidgetComponent):    
    def acceptEditor(self, editor):
        return False
