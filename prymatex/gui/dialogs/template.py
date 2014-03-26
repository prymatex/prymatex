#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from prymatex.qt import QtCore, QtGui
from prymatex.core.components import PrymatexDialog

from prymatex.utils.i18n import ugettext as _
from prymatex.gui.dialogs.environment import EnvironmentDialog

from prymatex.ui.dialogs.template import Ui_TemplateDialog

class TemplateDialog(PrymatexDialog, Ui_TemplateDialog, QtGui.QDialog):
    def __init__(self, **kwargs):
        super(TemplateDialog, self).__init__(**kwargs)
        self.setupUi(self)
        self.application = QtGui.QApplication.instance()
        self.setupComboTemplates()
        
        #Completer para los paths
        model = QtGui.QFileSystemModel(self)
        model.setRootPath(QtCore.QDir.rootPath())
        model.setFilter(QtCore.QDir.Dirs)
        self.completerFileSystem = QtGui.QCompleter(model, self)
        self.lineLocation.setCompleter(self.completerFileSystem)
        
        self.buttonCreate.setDefault(True)
        self.fileCreated = None
        self.userEnvironment = {}
    
    def initialize(self, **kwargs):
        super(TemplateDialog, self).initialize(**kwargs)
        self.environmentDialog = self.mainWindow.findChild(QtGui.QDialog, "EnvironmentDialog")
    
    def setupComboTemplates(self):
        tableView = QtGui.QTableView(self)
        tableView.setModel(self.application.supportManager.templateProxyModel)
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
        self.comboTemplates.setModel(self.application.supportManager.templateProxyModel);
        self.comboTemplates.setView(tableView)
        self.comboTemplates.setModelColumn(0)
        
    def on_buttonChoose_pressed(self):
        directory = self.lineLocation.text()
        path = QtGui.QFileDialog.getExistingDirectory(self, _("Choose location for template"), directory)
        if path:
            self.lineLocation.setText(path)
        
    def on_buttonCreate_pressed(self):
        templateModel = self.comboTemplates.model()
        template = templateModel.node(templateModel.createIndex(self.comboTemplates.currentIndex(), 0))
        if template is not None:
            
            #Build environment for template
            environment = template.buildEnvironment(fileDirectory = self.lineLocation.text(), fileName = self.lineFileName.text())
            for var in self.userEnvironment:
                if var['enabled']:
                    environment[var['variable']] = var['value']

            template.execute(environment, self.afterRunTemplate)
       
    def afterRunTemplate(self, filePath):
        self.fileCreated = filePath
        self.accept()
        
    def check_valid_location(self):
        """ Disable file """
        if os.path.isdir(self.lineLocation.text()) and self.lineFileName.text():
            self.buttonCreate.setEnabled(True)
             
    def on_lineFileName_textChanged(self, text):
        self.check_valid_location()
    
    def on_lineLocation_textChanged(self, text):
        self.check_valid_location()

    def on_buttonClose_pressed(self):
        self.reject()
    
    def on_buttonEnvironment_pressed(self):
        name = self.lineFileName.text()
        location = self.lineLocation.text()
        templateModel = self.comboTemplates.model()
        template = templateModel.node(templateModel.createIndex(self.comboTemplates.currentIndex(), 0))
        
        tEnv = template.buildEnvironment(fileName = name, fileDirectory = location, localVars = True)
        self.userEnvironment = self.environmentDialog.editEnvironment(self.userEnvironment, template = tEnv)
             
    def createFile(self, title="Create file from template", fileDirectory = "", fileName = "", parent = None):
        self.setWindowTitle(title)
        self.lineFileName.setText(fileName)
        self.lineLocation.setText(fileDirectory)
        self.buttonCreate.setEnabled(False)
        if self.exec_() == self.Accepted:
            self.application.openFile(self.fileCreated)
            return self.fileCreated
