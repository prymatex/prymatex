#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex.gui.settings.models import PMXPropertyTreeNode
from prymatex.ui.settings.environment import Ui_Environment

class PMXEnvVariablesTableModel(QtCore.QAbstractTableModel):
    userVariablesChanged = QtCore.pyqtSignal(list)
    def __init__(self, parent = None):
        super(PMXEnvVariablesTableModel, self).__init__(parent)
        self.variables = []
        
    def setVariables(self, user, system):
        if user is None:
            user = []
        self.variables = user + map(lambda (variable, value): {'variable': variable, 'value': value, 'system': True, 'enabled': True}, system.iteritems())
        self.layoutChanged.emit()
        
    def setSettingValue(self):
        variables = filter(lambda item: 'system' not in item, self.variables)
        if all(map(lambda variable: bool(variable['variable']), variables)):
            self.userVariablesChanged.emit(variables)
    
    def rowCount(self, parent = None):
        return len(self.variables)
    
    def columnCount(self, parent = None):
        return 2
    
    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid(): 
            return None
        
        if role == QtCore.Qt.CheckStateRole and index.column() == 0:
            if 'system' not in self.variables[index.row()]:
                return QtCore.Qt.Unchecked if not self.variables[index.row()]['enabled'] else QtCore.Qt.Checked
        elif role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if index.column() == 0:
                return self.variables[index.row()]['variable']
            else:
                return self.variables[index.row()]['value']

    def setData(self, index, value, role):
        '''
            Retornar verdadero si se puedo hacer el camio, falso en caso contratio
        '''
        if not index.isValid(): return False

        if role == QtCore.Qt.EditRole:
            new_value = value
            if index.column() == 0 and any(map(lambda value: value['variable'] == new_value, self.variables)):
                return False
            elif index.column() == 0:
                self.variables[index.row()]['variable'] = new_value
            else:
                self.variables[index.row()]['value'] = new_value
            self.setSettingValue()
            self.dataChanged.emit(index, index)
            return True;
        elif role == QtCore.Qt.CheckStateRole:
            self.variables[index.row()]['enabled'] = value
            self.setSettingValue()
            self.dataChanged.emit(index, index)
            return True
        return False
        
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                if section == 0:
                    return "Variable"
                elif section == 1:
                    return "Value"

    def insertRows(self, position, rows, parent = QtCore.QModelIndex()):
        if any(map(lambda value: value['variable'] == "", self.variables)):
            return False
        self.beginInsertRows(parent, position, position + rows - 1)
        for _ in range(rows):
            self.variables.insert(position, {'variable': "", 'value': "", 'enabled': True})
        self.endInsertRows()
        return True

    def removeRows(self, position, rows, parent = QtCore.QModelIndex()):
        if any(map(lambda value: 'system' in value, self.variables[position:position + 1])):
            return False
        self.beginRemoveRows(parent, position, position + rows - 1);
        for _ in range(rows):
            self.variables.pop(position)
        self.setSettingValue()
        self.endRemoveRows()
        return True

    def flags(self, index):
        if 'system' in self.variables[index.row()]:
            return QtCore.Qt.ItemIsEnabled
        else:
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable

class PMXEnvironmentWidget(QtGui.QWidget, PMXPropertyTreeNode, Ui_Environment):
    """Environment variables
    """
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
        self.model.setVariables(self.project.shellVariables, self.project.environment )

    def setupVariablesTableModel(self):
        self.model = PMXEnvVariablesTableModel(self)
        self.model.userVariablesChanged.connect(self.on_variablesModel_userVariablesChanged)
        self.tableView.setModel(self.model)
        
        self.tableView.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.tableView.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.tableView.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.model.rowsInserted.connect(self.tableView.resizeRowsToContents)
        self.model.rowsRemoved.connect(self.tableView.resizeRowsToContents)
        self.tableView.resizeRowsToContents()

    def on_variablesModel_userVariablesChanged(self, variables):
        self.application.projectManager.updateProject(self.project, shellVariables = variables)

    def on_pushAdd_pressed(self):
        self.model.insertRows(0, 1)
        
    def on_pushRemove_pressed(self):
        index = self.tableView.currentIndex()
        self.model.removeRows(index.row() , 1)