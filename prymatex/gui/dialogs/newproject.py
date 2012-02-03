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
        
        self.templateProxyModel = self.application.supportManager.templateProxyModel
        self.comboBoxProjectTemplate.setModel(self.templateProxyModel)
        self.comboBoxProjectTemplate.setModelColumn(0)
        self.buttonCreate.setDefault(True)
        self.projectCreated = None
    
    def on_buttonChoose_pressed(self):
        directory = self.application.fileManager.getDirectory()
        path = QtGui.QFileDialog.getExistingDirectory(self, _("Choose Location for Project"), directory)
        if path:
            self.lineLocation.setText(path)

    def on_buttonCreate_pressed(self):
        name = self.lineProjectName.text()
        location = self.lineLocation.text()
        self.runTemplateForProject(location, name)
        
        self.projectCreated = self.application.projectManager.createProject(name, location)
        
        if self.checkBoxAddToWorkingSet.isChecked():
            workingSet = self.comboBoxWorkingSet.lineEdit().text()
            self.application.projectManager.setWorkingSet(self.projectCreated, workingSet)
        self.accept()
    
    def on_lineProjectName_textChanged(self, text):
        if self.checkBoxUseDefaultLocation.isChecked():
            self.application.projectManager.workspaceDirectory
            projectPath = os.path.join(self.application.projectManager.workspaceDirectory, text)
            self.lineLocation.setText(projectPath)
        self.buttonCreate.setEnabled(bool(text))
    
    def on_lineLocation_textChanged(self, text):
        if not text:
            self.lineLocation.setText(self.application.projectManager.workspaceDirectory)

    def on_checkBoxUseDefaultLocation_toggled(self, checked):
        self.lineLocation.setEnabled(not checked)
        self.buttonChoose.setEnabled(not checked)
    
    def on_checkBoxAddToWorkingSet_toggled(self, checked):
        self.comboBoxWorkingSet.setEnabled(checked)
        
    def on_buttonClose_pressed(self):
        self.reject()

    def runTemplateForProject(self, location, name):
        index = self.templateProxyModel.mapToSource(self.templateProxyModel.createIndex(self.comboBoxProjectTemplate.currentIndex(), 0))
        if index.isValid():
            template = index.internalPointer()
            environment = template.buildEnvironment(projectLocation = location, projectName = name)
            return template.execute(environment)
    
    @classmethod
    def getNewProject(cls, parent = None, directory = None, name = None):
        dlg = cls(parent)
        dlg.lineProjectName.setText(name or '')
        dlg.buttonCreate.setEnabled(not directory is None and not name is None)
        dlg.lineLocation.setText(directory or dlg.application.projectManager.workspaceDirectory)
        if dlg.exec_() == dlg.Accepted:
            return dlg.projectCreated