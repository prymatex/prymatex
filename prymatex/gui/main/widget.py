#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore
from prymatex.core.base import PMXWidget

class PMXBaseWidget(PMXWidget):
    # Signals
    tabStatusChanged = QtCore.pyqtSignal()
    
    def getTitle(self):
        pass
    
    def getIcon(self):
        pass
