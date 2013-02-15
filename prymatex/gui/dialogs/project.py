#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from prymatex.qt import QtCore, QtGui
from prymatex.core.components import PMXBaseDialog

from prymatex.utils.i18n import ugettext as _

from prymatex.ui.dialogs.project import Ui_ProjectDialog

class ProjectDialog(QtGui.QDialog, PMXBaseDialog, Ui_ProjectDialog):
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        PMXBaseDialog.__init__(self)
        self.setupUi(self)
        
        model = QtGui.QFileSystemModel(self)
        model.setRootPath(QtCore.QDir.rootPath())
        model.setFilter(QtCore.QDir.Dirs)
        self.completerFileSystem = QtGui.QCompleter(model, self)
        self.lineLocation.setCompleter(self.completerFileSystem)

        self.setupComboKeywords()        
        self.setupComboTemplates()
        self.buttonCreate.setDefault(True)
        self.projectCreated = None
        self.userEnvironment = {}


    def initialize(self, mainWindow):
        PMXBaseDialog.initialize(self, mainWindow)
        self.environmentDialog = self.mainWindow.findChild(QtGui.QDialog, "EnvironmentDialog")

        
    def setupComboKeywords(self):
        # Build project keywords
        self.application.projectManager.keywordsListModel.clear()
        self.comboBoxKeywords.setModel(
            self.application.projectManager.keywordsListModel
        )
        self.comboBoxKeywords.lineEdit().setText("")
        self.comboBoxKeywords.lineEdit().setReadOnly(True)
        self.application.projectManager.keywordsListModel.dataChanged.connect(
            self.on_keywordsListModel_dataChanged
        )


    def on_keywordsListModel_dataChanged(self, topLeft, bottomRight):
        current = self.application.projectManager.keywordsListModel.selectedKeywords()
        self.comboBoxKeywords.lineEdit().setText(", ".join(current))
        

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
        directory = self.lineLocation.text()
        path = QtGui.QFileDialog.getExistingDirectory(self, _("Choose Location for Project"), directory)
        if path:
            self.lineLocation.setText(path)
            self.lineProjectName.setText(os.path.basename(path))


    def on_buttonCreate_pressed(self):
        name = self.lineProjectName.text()
        location = self.lineLocation.text()
        
        if self.checkBoxUseTemplate.isChecked():
            self.runTemplateForProject(name, location)
        else:
            self.runCreateProject(name, location)


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
        self.buttonEnvironment.setEnabled(checked)


    def on_buttonClose_pressed(self):
        self.reject()


    def on_buttonEnvironment_pressed(self):
        name = self.lineProjectName.text()
        location = self.lineLocation.text()
        index = self.projectProxyModel.createIndex(self.comboBoxTemplate.currentIndex(), 0)
        if index.isValid():
            template = self.projectProxyModel.node(index)
            tEnv = template.buildEnvironment(projectName = name, projectLocation = location, localVars = True)
        self.userEnvironment = self.environmentDialog.editEnvironment(self.userEnvironment, template = tEnv)


    def runCreateProject(self, name, location):
        description = self.textDescription.toPlainText()
        self.projectCreated = self.application.projectManager.createProject(name, location, description)

        #Set template's bundle for project
        if self.checkBoxUseTemplate.isChecked():
            index = self.projectProxyModel.createIndex(self.comboBoxTemplate.currentIndex(), 0)
            template = self.projectProxyModel.node(index)
            self.projectCreated.addBundleMenu(template.bundle)

        self.accept()


    def afterRunTemplate(self, name, location):
        self.runCreateProject(name, location)


    def runTemplateForProject(self, name, location):
        index = self.projectProxyModel.createIndex(self.comboBoxTemplate.currentIndex(), 0)
        if index.isValid():
            template = self.projectProxyModel.node(index)

            #Build environment for template
            environment = template.buildEnvironment(projectName = name, projectLocation = location)
            environment.update(self.userEnvironment)
            template.execute(environment, self.afterRunTemplate)

    
    def createProject(self, title = "Create new project", directory = None, name = None):
        self.lineProjectName.setText(name or '')
        self.buttonCreate.setEnabled(not directory is None and not name is None)
        self.lineLocation.setText(directory or self.application.projectManager.workspaceDirectory)
        self.checkBoxUseTemplate.setChecked(False)
        if self.exec_() == self.Accepted:
            return self.projectCreated
