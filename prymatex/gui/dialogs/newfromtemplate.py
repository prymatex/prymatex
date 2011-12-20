#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from PyQt4 import QtCore, QtGui
from prymatex.core.base import PMXObject
from prymatex.ui.dialogs.newfromtemplate import Ui_NewFromTemplateDialog

class PMXNewFromTemplateDialog(QtGui.QDialog, Ui_NewFromTemplateDialog, PMXObject):
    def __init__(self, parent = None):
        super(PMXNewFromTemplateDialog, self).__init__(parent)
        self.setupUi(self)
        model = QtGui.QFileSystemModel(self)
        model.setRootPath(QtCore.QDir.rootPath())
        model.setFilter(QtCore.QDir.Dirs)
        self.completerFileSystem = QtGui.QCompleter(model, self)
        self.lineLocation.setCompleter(self.completerFileSystem)
        
        self.templateProxyModel = self.application.supportManager.templateProxyModel
        self.comboTemplates.setModel(self.templateProxyModel)
        self.comboTemplates.setModelColumn(0)
        self.buttonCreate.setDefault(True)
        self.fileCreated = None
    
    def on_buttonChoose_pressed(self):
        directory = self.application.fileManager.getDirectory()
        path = QtGui.QFileDialog.getExistingDirectory(self, _("Choose Location for Template"), directory)
        if path:
            self.lineLocation.setText(path)
        
    def on_buttonCreate_pressed(self):
        index = self.templateProxyModel.mapToSource(self.templateProxyModel.createIndex(self.comboTemplates.currentIndex(), 0))
        if index.isValid():
            template = index.internalPointer()
            environment = template.buildEnvironment(directory = self.lineLocation.text(), name = self.lineFileName.text())
            template.resolve(environment)
            self.fileCreated = environment['TM_NEW_FILE']
            self.accept()
        else:
            #TODO: Mostrar error
            pass
        
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

    def getNewFileFromTemplate(self, fileDirectory = "", fileName = ""):
        self.lineFileName.setText(fileName)
        self.buttonCreate.setEnabled(False)
        if self.exec_() == self.Accepted:
            return self.fileCreated