#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from PyQt4 import QtCore, QtGui

from prymatex.utils.i18n import ugettext as _
from prymatex.ui.dialogs.project import Ui_NewProjectDialog
from prymatex.gui.dialogs.environment import EnvironmentDialog

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

        self.setupComboKeywords()        
        self.setupComboTemplates()
        self.buttonCreate.setDefault(True)
        self.projectCreated = None
        self.userEnvironment = []


    def setupComboKeywords(self):
        # Build project keywords
        self.comboBoxKeywords.setModel(self.application.projectManager.keywordsListModel)
        self.comboBoxKeywords.lineEdit().setText("")
        self.comboBoxKeywords.lineEdit().setReadOnly(True)


    def on_keywordsModel_dataChanged(self, topLeft, bottomRight):
        current = []
        for row in xrange(self.keywordsModel.rowCount()):
            index = self.keywordsModel.index(row, 0)
            if index.data(QtCore.Qt.CheckStateRole) == QtCore.Qt.Checked:
                current.append(index.data())
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
        while True:
            path = QtGui.QFileDialog.getExistingDirectory(self, _("Choose Location for Project"), directory)
            if path:
                if not os.path.exists(path): continue
                path = os.path.abspath(path)
                self.lineLocation.setText(path)
                self.lineProjectName.setText(os.path.basename(path))
            return


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
        self.userEnvironment = EnvironmentDialog.editEnvironment(self, self.userEnvironment, tEnv)
        
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
            for var in self.userEnvironment:
                if var['enabled']:
                    environment[var['variable']] = var['value']

            template.execute(environment, self.afterRunTemplate)
    
    @classmethod
    def getNewProject(cls, parent = None, directory = None, name = None):
        dlg = cls(parent)
        dlg.lineProjectName.setText(name or '')
        dlg.buttonCreate.setEnabled(not directory is None and not name is None)
        dlg.lineLocation.setText(directory or dlg.application.projectManager.workspaceDirectory)
        dlg.checkBoxUseTemplate.setChecked(False)
        if dlg.exec_() == dlg.Accepted:
            return dlg.projectCreated