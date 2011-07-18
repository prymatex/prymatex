#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui

from prymatex.gui.config.widgets import PMXConfigBaseWidget
from prymatex.core.base import PMXObject
from prymatex.ui.configenvironment import Ui_EnvVariables

class PMXEnvVariablesTableModel(QtCore.QAbstractTableModel):
    def __init__(self, settingGroup, parent = None):
        super(PMXEnvVariablesTableModel, self).__init__(parent)
        self.values = [[], [], []]
        self.settingGroup = settingGroup
        shellVariables = self.settingGroup.value('shellVariables')
        for var in shellVariables:
            self.values[0].append(var['variable'])
            self.values[1].append(var['value'])
            self.values[2].append(var['enabled'])
    
    def setSettingValue(self):
        variables = []
        for index in range(len(self.values[0])):
            if self.values[0][index] != "":
                var = {}
                var['variable'] = self.values[0][index]
                var['value'] = self.values[1][index]
                var['enabled'] = self.values[2][index]
                variables.append(var)
        self.settingGroup.setValue('shellVariables', variables)
    
    def rowCount(self, parent):
        return len(self.values[0])
    
    def columnCount(self, parent):
        return 2
    
    def data(self, index, role):
        if not index.isValid: return QtCore.QVariant()
        
        if role == QtCore.Qt.CheckStateRole and index.column() == 0:
            return QtCore.Qt.Unchecked if not self.values[2][index.row()] else QtCore.Qt.Checked 
        elif role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return QtCore.QVariant(self.values[index.column()][index.row()])

    def setData(self, index, value, role):
        '''
            Retornar verdadero si se puedo hacer el camio, falso en caso contratio
        '''
        if not index.isValid(): return False

        if role == QtCore.Qt.EditRole:
            new_value = unicode(value.toPyObject());
            if index.column() == 0:
                #Ver si no esta repetido el valor de la variable
                try:
                    old_index = self.values[index.column()].index(new_value)
                    if not old_index == index.row():
                        return False
                except ValueError:
                    pass
            self.values[index.column()][index.row()] = new_value
            self.setSettingValue()
            self.dataChanged.emit(index, index)
            return True;
        elif role == QtCore.Qt.CheckStateRole:
            self.values[2][index.row()] = value.toBool()
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
        if "" in self.values[0]:
            return False
        self.beginInsertRows(parent, position, position + rows - 1)
        for _ in range(rows):
            self.values[0].insert(position, "")
            self.values[1].insert(position, "")
            self.values[2].insert(position, True)
        self.endInsertRows()
        return True

    def removeRows(self, position, rows, parent = QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1);
        for _ in range(rows):
            self.values[0].pop(position)
            self.values[1].pop(position)
            self.values[2].pop(position)
            self.setSettingValue()
        self.endRemoveRows()
        return True

    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable

class PMXEnvVariablesWidgets(PMXConfigBaseWidget, Ui_EnvVariables, PMXObject):
    '''
    Variables
    '''
    def __init__(self, parent = None):
        super(PMXEnvVariablesWidgets, self).__init__(parent)
        self.setupUi(self)
        self.configure()
        self.model = PMXEnvVariablesTableModel(self.pmxApp.settings.getGroup('Manager'))
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        
    def on_pushAdd_pressed(self):
        self.model.insertRows(0, 1)
        
    def on_pushRemove_pressed(self):
        index = self.tableView.currentIndex()
        self.model.removeRows(index.row() , 1)
