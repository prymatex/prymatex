#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from prymatex.models.properties import PropertyTreeNode
from prymatex.ui.configure.project import Ui_Project

class ProjectPropertiesWidget(QtGui.QWidget, PropertyTreeNode, Ui_Project):
    """ Project Settings """
    NAMESPACE = ""
    TITLE = "Project"

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        PropertyTreeNode.__init__(self, "project")
        self.setupUi(self)
        self.fileSystemItem = None

    def acceptFileSystemItem(self, fileSystemItem):
        return fileSystemItem.isproject
    
    def edit(self, projectNode):
        self.lineProjectName.setText(projectNode.name)
        self.textDescription.setText(projectNode.description)
        #self.comboBoxLicence.setText(projectNode.licence)
        self.textLabelLocation.setText(projectNode.path())