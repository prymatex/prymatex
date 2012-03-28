#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from PyQt4 import QtCore, QtGui

from prymatex.ui.dialogs.newfromtemplate import Ui_NewFromTemplateDialog
from prymatex.utils.i18n import ugettext as _

class PMXNewFromTemplateDialog(QtGui.QDialog, Ui_NewFromTemplateDialog):
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
        self.comboTemplates.setModel(self.templateProxyModel)
        self.comboTemplates.setModelColumn(0)
        self.buttonCreate.setDefault(True)
        self.fileCreated = None
    
    def getNewLocation(self):
        application = QtGui.QApplication.instance()
        projectDock = self.parent().projects
        from prymatex.gui.dockers.projects import PMXProjectDock
        assert isinstance(projectDock, PMXProjectDock), "Error de proyecto %s" % type(projectDock)
        path = application.fileManager.getDirectory(projectDock.currentPath()) 
        print path
        return path
        
    
    def on_buttonChoose_pressed(self):
        directory = self.lineLocation.text()
        path = QtGui.QFileDialog.getExistingDirectory(self, _("Choose location for template"), directory)
        if path:
            self.lineLocation.setText(path)
        
    def on_buttonCreate_pressed(self):
        index = self.templateProxyModel.mapToSource(self.templateProxyModel.createIndex(self.comboTemplates.currentIndex(), 0))
        if index.isValid():
            template = index.internalPointer()
            environment = template.buildEnvironment(fileDirectory = self.lineLocation.text(), fileName = self.lineFileName.text())
            self.fileCreated = template.execute(environment)
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

    @classmethod
    def newFileFromTemplate(cls, fileDirectory = "", fileName = "", parent = None):
        '''
        @return: new file path or None
        '''
        dlg = cls(parent = parent)
        dlg.lineFileName.setText(fileName)
        dlg.lineLocation.setText(dlg.getNewLocation())
        dlg.buttonCreate.setEnabled(False)
        if dlg.exec_() == cls.Accepted:
            return dlg.fileCreated
    