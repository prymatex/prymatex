#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import QDialog, QVBoxLayout, QPushButton, QFileDialog, QVariant
from PyQt4.QtCore import pyqtSignal, QDir
from PyQt4.Qt import SIGNAL
from PyQt4.QtGui import QCompleter, QFileSystemModel, QMessageBox
from os.path import isdir, abspath
from prymatex.core.base import PMXObject
from prymatex.ui.multiclose import Ui_SaveMultipleDialog
from prymatex.ui.newtemplate import Ui_NewFromTemplateDialog

if __name__ == '__main__':
    import sys
    from os.path import abspath, dirname, join
    path = join(abspath(dirname(__file__)), '..', )
    print path
    sys.path.append( path )
    
class MultiCloseDialog(QtGui.QDialog, Ui_SaveMultipleDialog):
    '''
    @todo: Implement PMXTabWidget model
    '''
    def __init__(self, parent):
        super(MultiCloseDialog, self).__init__(parent)
        self.setupUi(self)

from PyQt4.Qt import QDialog

class PMXNewFromTemplateDialog(QDialog, Ui_NewFromTemplateDialog, PMXObject):
    newFileCreated = pyqtSignal(str)
    
    def __init__(self, parent):
        super(PMXNewFromTemplateDialog, self).__init__(parent)
        self.setupUi(self)
        model = QFileSystemModel(self)
        model.setRootPath("")
        model.setFilter(QDir.Dirs)
        self.completerFileSystem = QCompleter(model, self)
        self.lineLocation.setCompleter(self.completerFileSystem)
        
        self.templateProxyModel = self.pmxApp.supportManager.templateProxyModel
        self.comboTemplates.setModel(self.templateProxyModel)
        self.comboTemplates.setModelColumn(0)
        self.buttonCreate.setDefault(True)
    
    def on_buttonChoose_pressed(self):
        path = QFileDialog.getExistingDirectory(self, self.trUtf8("Choose Location for Template"))
        if path:
            self.lineLocation.setText(path)

    def on_buttonCreate_pressed(self):
        #TODO: Validar que los lineEdit tengan texto
        template = self.comboTemplates.itemData(self.comboTemplates.currentIndex())
        environment = template.buildEnvironment(directory = unicode(self.lineLocation.text()), name = unicode(self.lineFileName.text()))
        if not template:
            QMessageBox.question(self, "Information requiered", 
                                 "You did not suply all the information required "
                                 "for the file", 
                                 buttons=QMessageBox.Cancel | QMessageBox.Retry, 
                                 defaultButton=QMessageBox.NoButton)
        template.resolve(environment)
        self.newFileCreated.emit(environment['TM_NEW_FILE'])
        self.close()
    
    def check_valid_location(self):
        ''' Disable file '''
        location = unicode(self.lineLocation.text())
        if not isdir(location):
            self.buttonCreate.setEnabled(False)
            return
        filename = unicode(self.lineFileName)
        if not filename:
            self.buttonCreate.setEnabled(False)
            return
        self.buttonCreate.setEnabled(True)
             
    def on_lineFileName_textChanged(self, text):
        self.check_valid_location()
    
    def on_lineLocation_textChanged(self, text):
        self.check_valid_location()
            
    def on_buttonClose_pressed(self):
        self.close()
    