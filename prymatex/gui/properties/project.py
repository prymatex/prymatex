#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui
from prymatex import resources

from prymatex.models.properties import PropertyTreeNode
from prymatex.ui.configure.project import Ui_Project

class ProjectPropertiesWidget(PropertyTreeNode, Ui_Project, QtGui.QWidget):
    """ Project Settings """
    NAMESPACE = ""
    TITLE = "Project"

    def __init__(self, **kwargs):
        super(ProjectPropertiesWidget, self).__init__(nodeName = "project", **kwargs)
        self.setupUi(self)
        self.projectNode = None
        self.setupComboLicences()
        self.setupComboKeywords()

    def acceptFileSystemItem(self, fileSystemItem):
        return fileSystemItem.isproject
    
    def setupComboLicences(self):
        for licence in resources.LICENSES:
            self.comboBoxLicence.addItem(licence)
    
    def setupComboKeywords(self):
        # Build project keywords
        self.comboBoxKeywords.setModel(
            self.application().projectManager.keywordsListModel
        )
        self.comboBoxKeywords.lineEdit().setReadOnly(True)
        self.application().projectManager.keywordsListModel.selectionChanged.connect(
            self.on_keywordsListModel_selectionChanged
        )

    def on_keywordsListModel_selectionChanged(self):
        currents = self.comboBoxKeywords.model().selectedItems()
        self.comboBoxKeywords.lineEdit().setText(", ".join(currents))
    
    def edit(self, projectNode):
        self.projectNode = projectNode
        self.lineProjectName.setText(self.projectNode.name)
        if self.projectNode.description:
            self.textDescription.setText(self.projectNode.description)
        if self.projectNode.keywords:
            self.comboBoxKeywords.model().selectItems(self.projectNode.keywords)
            self.comboBoxKeywords.lineEdit().setText(", ".join(self.projectNode.keywords))
        if self.projectNode.licence:
            index = self.comboBoxLicence.findText(self.projectNode.licence)
            if index == -1:
                self.comboBoxLicence.addItem(self.projectNode.licence)
                index = self.comboBoxLicence.findText(self.projectNode.licence)
            self.comboBoxLicence.setCurrentIndex(index)
        self.textLabelLocation.setText(self.projectNode.path())
    
    def saveChanges(self):
        self.application().projectManager.updateProject(self.projectNode,
            name = self.lineProjectName.text(),
            description = self.textDescription.toPlainText(),
            licence = self.comboBoxLicence.currentText(),
            keywords = self.comboBoxKeywords.model().selectedItems())
        