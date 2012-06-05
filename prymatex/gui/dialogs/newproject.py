#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from PyQt4 import QtCore, QtGui

from prymatex.utils.i18n import ugettext as _
from prymatex.ui.dialogs.newproject import Ui_NewProjectDialog

class PMXNewProjectDialog(QtGui.QDialog, Ui_NewProjectDialog):
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.application = QtGui.QApplication.instance()
        
        model = QtGui.QFileSystemModel(self)
        model.setRootPath(QtCore.QDir.rootPath())
        model.setFilter(QtCore.QDir.Dirs)
        self.completerFileSystem = QtGui.QCompleter(model, self)
        self.lineLocation.setCompleter(self.completerFileSystem)
        
        self.setupComboTemplates()
        self.buttonCreate.setDefault(True)
        self.projectCreated = None

    def setupComboTemplates(self):
        self.projectProxyModel = self.application.supportManager.projectProxyModel
        tableView = QtGui.QTableView(self)
        tableView.setModel(self.projectProxyModel)
        tableView.resizeColumnsToContents()
        tableView.resizeRowsToContents()
        tableView.verticalHeader().setVisible(False)
        tableView.horizontalHeader().setVisible(False)
        tableView.setShowGrid(False)
        tableView.setMinimumWidth(tableView.horizontalHeader().length() + 25)
        tableView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        tableView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        tableView.setAutoScroll(False)
        self.comboBoxTemplate.setModel(self.projectProxyModel)
        self.comboBoxTemplate.setView(tableView)
        self.comboBoxTemplate.setModelColumn(0)

    def on_buttonChoose_pressed(self):
        directory = self.application.fileManager.getDirectory()
        path = QtGui.QFileDialog.getExistingDirectory(self, _("Choose Location for Project"), directory)
        if path:
            self.lineLocation.setText(path)
            self.lineProjectName.setText(os.path.basename(path))

    def on_buttonCreate_pressed(self):
        name = self.lineProjectName.text()
        location = self.lineLocation.text()
        
        if self.checkBoxUseTemplate.isChecked():
            location = self.runTemplateForProject(name, location)
        
        self.projectCreated = self.application.projectManager.createProject(name, location)
        
        if self.checkBoxAddToWorkingSet.isChecked():
            workingSet = self.comboBoxWorkingSet.lineEdit().text()
            self.application.projectManager.setWorkingSet(self.projectCreated, workingSet)
        self.accept()
    
    def on_lineProjectName_textChanged(self, text):
        if self.checkBoxUseDefaultLocation.isChecked():
            projectPath = os.path.join(self.application.projectManager.workspaceDirectory, text)
            self.lineLocation.setText(projectPath)
        self.buttonCreate.setEnabled(bool(text.strip()))
    
    def on_lineLocation_textChanged(self, text):
        if text and not self.checkBoxUseDefaultLocation.isChecked():
            self.lineProjectName.setText(os.path.basename(text))

    def on_checkBoxUseDefaultLocation_toggled(self, checked):
        self.lineLocation.setEnabled(not checked)
        self.buttonChoose.setEnabled(not checked)
        if checked:
            projectPath = os.path.join(self.application.projectManager.workspaceDirectory, self.lineProjectName.text())
            self.lineLocation.setText(projectPath)
    
    def on_checkBoxAddToWorkingSet_toggled(self, checked):
        self.comboBoxWorkingSet.setEnabled(checked)
    
    def on_checkBoxUseTemplate_toggled(self, checked):
        self.comboBoxTemplate.setEnabled(checked)
        
    def on_buttonClose_pressed(self):
        self.reject()

    def runTemplateForProject(self, name, location):
        index = self.projectProxyModel.mapToSource(self.projectProxyModel.createIndex(self.comboBoxTemplate.currentIndex(), 0))
        if index.isValid():
            template = index.internalPointer()
            environment = template.buildEnvironment(projectName = name, projectLocation = location)
            return template.execute(environment)
    
    @classmethod
    def getNewProject(cls, parent = None, directory = None, name = None):
        dlg = cls(parent)
        dlg.lineProjectName.setText(name or '')
        dlg.buttonCreate.setEnabled(not directory is None and not name is None)
        dlg.lineLocation.setText(directory or dlg.application.projectManager.workspaceDirectory)
        dlg.checkBoxUseTemplate.setChecked(False)
        if dlg.exec_() == dlg.Accepted:
            return dlg.projectCreated