#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex.gui.project.models import PMXPropertyTreeNode
from prymatex.ui.configure.resource import Ui_ResouceWidget

class PMXResouceWidget(QtGui.QWidget, PMXPropertyTreeNode, Ui_ResouceWidget):
    """Resouce"""
    NAMESPACE = ""
    TITLE = "Resouce"
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        PMXPropertyTreeNode.__init__(self, "resouce")
        self.setupUi(self)
        self.fileSystemItem = None

    def acceptFileSystemItem(self, fileSystemItem):
        return True
    
    def edit(self, fileSystemItem):
        self.fileSystemItem = fileSystemItem
        self.textLabelPath.setText(self.fileSystemItem.path())
        self.textLabelType.setText(self.fileSystemItem.path())
        self.textLabelLocation.setText(self.fileSystemItem.path())
        self.textLabelLastModified.setText(self.fileSystemItem.path())