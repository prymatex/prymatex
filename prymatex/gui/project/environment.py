#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex.gui.project.models import PMXPropertyTreeNode
from prymatex.ui.configure.environment import Ui_Environment
from prymatex.gui.models.environment import EnvironmentTableModel

class EnvironmentWidget(QtGui.QWidget, PMXPropertyTreeNode, Ui_Environment):
    """Environment variables"""
    NAMESPACE = ""
    TITLE = "Enviroment Variables"
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        PMXPropertyTreeNode.__init__(self, "environment")
        self.setupUi(self)
        self.setupVariablesTableModel()
        self.project = None

    def acceptFileSystemItem(self, fileSystemItem):
        return fileSystemItem.isproject
    
    def edit(self, project):
        self.project = project
        self.model.clear()
        self.model.addGroup('user', self.project.shellVariables, editable = True, checkable=True, foreground=QtCore.Qt.blue)
        self.model.addGroup('project', self.project.environment)
        self.model.addGroup('prymatex', self.application.supportManager.buildEnvironment(systemEnvironment = False), visible = False)

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
        self.model.setVisibility('project', checked)
    
    @QtCore.pyqtSlot(bool)        
    def on_checkBox3_clicked(self, checked):
        self.model.setVisibility('prymatex', checked)
        
    def on_variablesModel_variablesChanged(self, group, variables):
        self.application.projectManager.updateProject(self.project, shellVariables = variables)

    def on_pushAdd_pressed(self):
        self.model.insertRows(0, 1)
        
    def on_pushRemove_pressed(self):
        index = self.tableView.currentIndex()
        self.model.removeRows(index.row() , 1)