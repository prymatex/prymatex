#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex.ui.configure.environment import Ui_Environment
from prymatex.gui.models.environment import EnvironmentTableModel

class EnvironmentWidget(QtGui.QWidget, Ui_Environment):
    """Environment variables"""
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.setupVariablesTableModel()

    def setupVariablesTableModel(self):
        self.model = EnvironmentTableModel(self)
        self.model.variablesChanged.connect(self.on_variablesModel_variablesChanged)
        self.tableView.setModel(self.model)
        
        self.tableView.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.tableView.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.tableView.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.model.rowsInserted.connect(self.tableView.resizeRowsToContents)
        self.model.rowsRemoved.connect(self.tableView.resizeRowsToContents)
        self.tableView.resizeRowsToContents()
        
        self.checkBox1.setText("User")
        self.checkBox1.setChecked(True)
        self.checkBox2.setText("Project")
        self.checkBox2.setChecked(True)
        self.checkBox3.setText("Prymatex")

    @QtCore.pyqtSlot(bool)
    def on_checkBox1_clicked(self, checked):
        self.model.setVisibility('user', checked)

    @QtCore.pyqtSlot(bool)        
    def on_checkBox2_clicked(self, checked):
        self.model.setVisibility('template', checked)
    
    @QtCore.pyqtSlot(bool)        
    def on_checkBox3_clicked(self, checked):
        self.model.setVisibility('prymatex', checked)
        
    def on_variablesModel_variablesChanged(self, group, variables):
        print group, variables

    def on_pushAdd_pressed(self):
        self.model.insertVariable()
        
    def on_pushRemove_pressed(self):
        index = self.tableView.currentIndex()
        self.model.removeRows(index.row() , 1)

class EnvironmentDialog(QtGui.QDialog):
    def __init__(self, parent):
        """docstring for __init__"""
        QtGui.QDialog.__init__(self, parent)
        self.setObjectName("EnvironmentDialog")
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.environmentWidget = EnvironmentWidget(self)
        self.environmentWidget.setObjectName("environmentWidget")
        self.verticalLayout.addWidget(self.environmentWidget)
        self.application = QtGui.QApplication.instance()
        
    def addGroup(self, *largs, **kwargs):
        self.environmentWidget.model.addGroup(*largs, **kwargs)
                
    @classmethod
    def editEnvironment(cls, parent = None, userVariables = {}, templateVariables = {}):
        dlg = cls(parent)
        dlg.addGroup('user', userVariables, editable = True, checkable=True, foreground=QtCore.Qt.blue)
        dlg.addGroup('template', templateVariables)
        dlg.addGroup('prymatex', dlg.application.supportManager.buildEnvironment(systemEnvironment = False), visible = False)
        dlg.exec_()
        return userVariables