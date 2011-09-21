#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from prymatex.gui.central import PMXBaseTab

class PMXImageViewer(QtGui.QLabel, PMXBaseTab):
    def __init__(self, parent = None):
        QtGui.QLabel.__init__(self, parent)
        PMXBaseTab.__init__(self)

    def open(self, fileInfo):
        pixmap = QtGui.QPixmap(fileInfo.absoluteFilePath())
        self.setPixmap(pixmap)