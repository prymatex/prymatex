#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from prymatex.qt import QtCore, QtGui
from prymatex import resources

from prymatex.core.components import PMXBaseDialog
from prymatex.core import exceptions

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

        self.setupComboLicences()
        self.setupComboKeywords()        
        self.setupComboTemplates()
        self.buttonCreate.setDefault(True)
        self.projectCreated = None
        self.userEnvironment = {}

    def initialize(self, mainWindow):
        PMXBaseDialog.initialize(self, mainWindow)
        self.environmentDialog = self.mainWindow.findChild(QtGui.QDialog, "EnvironmentDialog")

    def setupComboLicences(self):
        for licence in resources.LICENSES:
            self.comboBoxLicence.addItem(licence)

    def setupComboKeywords(self):
        # Build project keywords
        self.comboBoxKeywords.setModel(
            self.application.projectManager.keywordsListModel
        )
        self.comboBoxKeywords.lineEdit().setReadOnly(True)
        self.application.projectManager.keywordsListModel.selectionChanged.connect(
            self.on_keywordsListModel_selectionChanged
        )

    def on_keywordsListModel_selectionChanged(self):
        currents = self.comboBoxKeywords.model().selectedItems()
        self.comboBoxKeywords.lineEdit().setText(", ".join(currents))

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
        try:
            self.projectCreated = self.application.projectManager.createProject(name, location)
        except exceptions.ProjectExistsException:
            rslt = QtGui.QMessageBox.information(None, 
                _("Project already created on %s") % name,
                _("Directory %s already contains .pmxproject directory structure. "
                "Unless you know what you are doing, Cancel and import project,"
                " if it still fails, choose overwirte. Overwrite?") % location,
                QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok, QtGui.QMessageBox.Cancel) 
            if rslt == QtGui.QMessageBox.Cancel:
                self.cancel()
            self.projectCreated = self.application.projectManager.createProject(name, location, overwrite = True)

        self.application.projectManager.updateProject(self.projectCreated,
            description = self.textDescription.toPlainText(),
            licence = self.comboBoxLicence.currentText(),
            keywords = self.comboBoxKeywords.model().selectedItems())

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
        self.comboBoxKeywords.lineEdit().setText("")
        self.application.projectManager.keywordsListModel.unselectAllItems()
        self.buttonCreate.setEnabled(not directory is None and not name is None)
        self.lineLocation.setText(directory or self.application.projectManager.workspaceDirectory)
        self.checkBoxUseTemplate.setChecked(False)
        if self.exec_() == self.Accepted:
            return self.projectCreated
