#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from PyQt4 import QtCore, QtGui
from prymatex.core.base import PMXObject
from prymatex.ui.dialogs.newproject import Ui_NewProjectDialog

class PMXNewProjectDialog(QtGui.QDialog, Ui_NewProjectDialog, PMXObject):
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        model = QtGui.QFileSystemModel(self)
        model.setRootPath(QtCore.QDir.rootPath())
        model.setFilter(QtCore.QDir.Dirs)
        self.completerFileSystem = QtGui.QCompleter(model, self)
        self.lineLocation.setCompleter(self.completerFileSystem)
        
        self.buttonCreate.setDefault(True)
        self.projectCreated = None
    
    def on_buttonChoose_pressed(self):
        path = QtGui.QFileDialog.getExistingDirectory(self, self.trUtf8("Choose Location for Template"))
        if path:
            self.lineLocation.setText(path)

    def on_buttonCreate_pressed(self):
        template = index.internalPointer()
        environment = template.buildEnvironment(directory = self.lineLocation.text(), name = self.lineFileName.text())
        template.resolve(environment)
        self.projectCreated = environment['TM_NEW_FILE']
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

    def getNewProject(self):
        self.lineProjectName.clear()
        self.buttonCreate.setEnabled(False)
        self.lineLocation.setText(self.application.projectManager.workspaceDirectory)
        if self.exec_() == self.Accepted:
            return self.projectCreated