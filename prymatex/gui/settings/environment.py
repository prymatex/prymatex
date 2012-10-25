#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from PyQt4 import QtCore, QtGui

from prymatex import resources
from prymatex.models.settings import SettingsTreeNode
from prymatex.ui.configure.environment import Ui_Environment
from prymatex.gui.models.environment import EnvironmentTableModel

class PMXEnvVariablesWidget(QtGui.QWidget, SettingsTreeNode, Ui_Environment):
    """Environment variables
    """
    NAMESPACE = "general"
    TITLE = "Enviroment Variables"
    ICON = resources.getIcon("codevariable")
    
    def __init__(self, settingGroup, parent = None):
        QtGui.QWidget.__init__(self, parent)
        SettingsTreeNode.__init__(self, "environment", settingGroup)
        self.setupUi(self)
        self.setupVariablesTableModel()
    
    def loadSettings(self):
        self.model.addGroup('user', self.application.supportManager.shellVariables, editable = True, checkable=True, foreground=QtCore.Qt.blue)
        self.model.addGroup('prymatex', self.application.supportManager.environment)
        self.model.addGroup('system', os.environ, foreground=QtCore.Qt.red, visible = False)

    def setupVariablesTableModel(self):
        self.model = EnvironmentTableModel(self)
        self.model.variablesChanged.connect(self.on_variablesModel_userVariablesChanged)
        self.tableView.setModel(self.model)
        
        self.tableView.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.tableView.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.tableView.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.model.rowsInserted.connect(self.tableView.resizeRowsToContents)
        self.model.rowsRemoved.connect(self.tableView.resizeRowsToContents)
        self.tableView.resizeRowsToContents()
        
        self.checkBox1.setText("User")
        self.checkBox1.setChecked(True)
        self.checkBox2.setText("Prymatex")
        self.checkBox2.setChecked(True)
        self.checkBox3.setText("System")

    @QtCore.pyqtSlot(bool)
    def on_checkBox1_clicked(self, checked):
        self.model.setVisibility('user', checked)

    @QtCore.pyqtSlot(bool)        
    def on_checkBox2_clicked(self, checked):
        self.model.setVisibility('prymatex', checked)
    
    @QtCore.pyqtSlot(bool)
    def on_checkBox3_clicked(self, checked):
        self.model.setVisibility('system', checked)
        
    def on_variablesModel_userVariablesChanged(self, group, variables):
        self.settingGroup.setValue('shellVariables', variables)

    def on_pushAdd_pressed(self):
        self.model.insertVariable()
        
    def on_pushRemove_pressed(self):
        index = self.tableView.currentIndex()
        self.model.removeRows(index.row() , 1)