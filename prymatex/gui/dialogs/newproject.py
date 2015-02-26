#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from prymatex.qt import QtCore, QtGui, QtWidgets

from prymatex.core.components import PrymatexDialog
from prymatex.core import exceptions
from prymatex.core import config

from prymatex.utils.i18n import ugettext as _

from prymatex.ui.dialogs.newproject import Ui_NewProjectDialog

class NewProjectDialog(PrymatexDialog, Ui_NewProjectDialog, QtWidgets.QDialog):
    def __init__(self, **kwargs):
        super(NewProjectDialog, self).__init__(**kwargs)
        self.setupUi(self)

        self.setupComboLicences()
        self.setupComboKeywords()        
        self.setupComboTemplates()
        self.pushButtonCreate.setDefault(True)
        self.projectCreated = None
        self.userEnvironment = {}

    def initialize(self, **kwargs):
        super(NewProjectDialog, self).initialize(**kwargs)
        self.environmentDialog = self.window().findChild(QtWidgets.QDialog, "EnvironmentDialog")

    def setupComboLicences(self):
        for licence in self.resources().get_software_licenses():
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

    def setupComboTemplates(self):
        self.projectProxyModel = self.application().supportManager.projectProxyModel
        tableView = QtWidgets.QTableView(self)
        tableView.setModel(self.projectProxyModel)
        tableView.resizeColumnsToContents()
        tableView.resizeRowsToContents()
        tableView.verticalHeader().setVisible(False)
        tableView.horizontalHeader().setVisible(False)
        tableView.setShowGrid(False)
        tableView.setMinimumWidth(tableView.horizontalHeader().length() + 25)
        tableView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        tableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        tableView.setAutoScroll(False)
        self.comboBoxTemplate.setModel(self.projectProxyModel)
        self.comboBoxTemplate.setView(tableView)
        self.comboBoxTemplate.setModelColumn(0)

    def on_pushButtonChooseFolder_pressed(self):
        folder_path = self.lineEditFolder.text()
        path = QtWidgets.QFileDialog.getExistingDirectory(self, _("Choose source folder for project"), folder_path)
        if path:
            self.lineEditFolder.setText(path)

    def on_pushButtonChooseFile_pressed(self):
        file_path = self.lineEditFile.text()
        path, filers = QtWidgets.QFileDialog.getSaveFileName(self, _("Choose file name for project"), file_path)
        if path:
            self.lineEditFile.setText(path)

    def on_pushButtonCreate_pressed(self):
        name = self.lineEditName.text()
        folder_path = self.lineEditFolder.text()
        file_path = self.lineEditFile.text()
        
        if self.checkBoxUseTemplate.isChecked():
            self.runTemplateForProject(name, file_path, folder_path)
        else:
            self.runCreateProject(name, file_path, folder_path)

    def on_lineEditName_textChanged(self, text):
        if self.checkBoxUseSourceFolder.isChecked():
            folder_path = os.path.join(self.application().projectManager.default_directory, text)
            self.lineEditFolder.setText(folder_path)
        self.pushButtonCreate.setEnabled(bool(text))

    def on_lineEditFolder_textChanged(self, text):
        file_path = os.path.join(
            text or self.application().projectManager.default_directory,
            "%s.%s" % (self.lineEditName.text(), config.PMX_PROJECT_EXTENSION)
        )
        self.lineEditFile.setText(file_path)

    def on_checkBoxUseSourceFolder_toggled(self, checked):
        self.pushButtonChooseFolder.setEnabled(checked)
        folder_path = os.path.join(self.application().projectManager.default_directory, self.lineEditName.text()) \
            if checked \
            else ""
        self.lineEditFolder.setText(folder_path)

    def on_checkBoxAddToWorkingSet_toggled(self, checked):
        self.comboBoxWorkingSet.setEnabled(checked)
    
    def on_checkBoxUseTemplate_toggled(self, checked):
        self.comboBoxTemplate.setEnabled(checked)
        self.pushButtonEnvironment.setEnabled(checked)

    def on_pushButtonClose_pressed(self):
        self.reject()

    def on_pushButtonEnvironment_pressed(self):
        name = self.lineEditName.text()
        folder_path = self.lineEditFolder.text()
        index = self.projectProxyModel.createIndex(self.comboBoxTemplate.currentIndex(), 0)
        if index.isValid():
            template = self.projectProxyModel.node(index)
            t_env = template.buildEnvironment(projectName=name, projectLocation=folder_path, localVars=True)
        self.userEnvironment = self.environmentDialog.editEnvironment(self.userEnvironment, template=t_env)

    def runCreateProject(self, name, file_path, folder_path):
        folders = [ folder_path ] if folder_path else []
        try:
            self.projectCreated = self.application().projectManager.createProject(name, file_path, folders=folders)
        except exceptions.ProjectExistsException:
            rslt = QtWidgets.QMessageBox.information(None, 
                _("Project file already exists"),
                _("The %s path already exists. "
                "Unless you know what you are doing, Cancel and open project,"
                " if it still fails, choose overwirte. Overwrite?") % file_path,
                QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Cancel) 
            if rslt == QtWidgets.QMessageBox.Cancel:
                self.cancel()
            self.projectCreated = self.application().projectManager.createProject(name, file_path, folders=folders, overwrite=True)

        self.application().projectManager.updateProject(self.projectCreated,
            description = self.textEditDescription.toPlainText(),
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

    def createProject(self, title="Create new project", directory=None, name=None):
        self.lineEditName.setText(name or '')
        self.comboBoxKeywords.lineEdit().setText("")
        self.application().projectManager.keywordsListModel.unselectAllItems()
        self.pushButtonCreate.setEnabled(False)
        self.checkBoxUseTemplate.setChecked(False)
        self.checkBoxUseSourceFolder.setChecked(True)
        if self.exec_() == self.Accepted:
            return self.projectCreated
