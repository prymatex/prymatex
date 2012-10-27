#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

class EnvironmentTableModel(QtCore.QAbstractTableModel):
    variablesChanged = QtCore.pyqtSignal(str, list)
    
    def __init__(self, parent = None):
        super(EnvironmentTableModel, self).__init__(parent)
        self.variableGroups = []
        self.lastEditableGroup = None

    def mapFromVariables(self, variables):
        #Return variable as list of dicts [{'variable': name, 'value': value, 'enabled': True}...]
        if variables is None:
            return []
        elif hasattr(variables, 'iteritems'):
            return map(lambda (name, value): {'variable': name, 'value': value, 'enabled': True}, variables.iteritems())
        return variables
        
    def groupByName(self, name):
        for group in self.variableGroups:
            if group['name'] == name:
                return group
                
    def addGroup(self, name, variables, editable = False, checkable = False, visible = True, foreground = QtCore.Qt.black, background = QtCore.Qt.white):
        group = {
            'name': name,
            'variables': self.mapFromVariables(variables),
            'editable': editable,
            'checkable': checkable,
            'visible': visible,
            'foreground': foreground,
            'background': background
        } 
        self.variableGroups.append(group)
        if editable:
            self.lastEditableGroup = group
        self.layoutChanged.emit()
    
    def clear(self):
        self.variableGroups = []
        self.layoutChanged.emit()
        
    def setVisibility(self, name, visible):
        group = self.groupByName(name)
        group['visible'] = visible
        self.layoutChanged.emit()
        
    def mapToGroup(self, index):
        currentGroup = None
        for currentGroup in self.variableGroups:
            if currentGroup["visible"]:
                varCount = len(currentGroup['variables'])
                if index < varCount:
                    break
                index -= varCount
        return index, currentGroup

    def variableGroupTablePosition(self, group, top = True):
        position = 0
        for currentGroup in self.variableGroups:
            if currentGroup["visible"]:
                if currentGroup == group:
                    break
                position += len(currentGroup['variables'])
        if not top:
            position += len(currentGroup['variables'])
        return position

    def allEditableVariables(self):
        return reduce(lambda l, group: l + (group['editable'] and group['variables'] or []), self.variableGroups, [])
        
    def rowCount(self, parent = None):
        if not self.variableGroups:
            return 0
        return reduce(lambda count, group: count + (group['visible'] and len(group['variables']) or 0), self.variableGroups, 0)
    
    def columnCount(self, parent = None):
        return 2
    
    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid(): 
            return None
        row = index.row()
        row, group = self.mapToGroup(row)
        
        if role == QtCore.Qt.CheckStateRole and index.column() == 0:
            if group['checkable']:
                return QtCore.Qt.Unchecked if not group['variables'][row]['enabled'] else QtCore.Qt.Checked
        elif role in [ QtCore.Qt.DisplayRole, QtCore.Qt.EditRole ]:
            if index.column() == 0:
                return group['variables'][row]['variable']
            else:
                return group['variables'][row]['value']
        elif role == QtCore.Qt.ForegroundRole:
            return group["foreground"]
        elif role == QtCore.Qt.BackgroundColorRole:
            return group["background"]
        
    def setData(self, index, value, role):
        """Retornar verdadero si se puedo hacer el cambio, falso en caso contrario"""

        if not index.isValid(): return False
        row = index.row()
        row, group = self.mapToGroup(row)
        
        if role == QtCore.Qt.EditRole:
            new_value = value
            if index.column() == 0 and any(map(lambda value: value['variable'] == new_value, group['variables'])):
                return False
            elif index.column() == 0:
                group['variables'][row]['variable'] = new_value
            else:
                group['variables'][row]['value'] = new_value
            self.variablesChanged.emit(group['name'], group['variables'])
            self.dataChanged.emit(index, index)
            return True
        elif role == QtCore.Qt.CheckStateRole:
            group['variables'][row]['enabled'] = value
            self.variablesChanged.emit(group['name'], group['variables'])
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

    def insertVariable(self, groupName = None):
        group = self.groupByName(groupName) if groupName else self.lastEditableGroup
        if group is not None and group['editable']:
            position = self.variableGroupTablePosition(group)
            self.beginInsertRows(QtCore.QModelIndex(), position, position)
            group['variables'].insert(0, {'variable': "", 'value': "", 'enabled': True})
            self.endInsertRows()

    def removeRows(self, position, rows, parent = QtCore.QModelIndex()):
        if any(map(lambda value: 'system' in value, self.variables[position:position + 1])):
            return False
        self.beginRemoveRows(parent, position, position + rows - 1)
        row, group = self.mapToGroup(position)
        for _ in range(rows):
            group['variables'].pop(row)
        self.variablesChanged.emit(group['name'], group['variables'])
        self.endRemoveRows()
        return True

    def flags(self, index):
        row, group = self.mapToGroup(index.row())
        flags = QtCore.Qt.ItemIsEnabled
        if group['checkable']:
            flags |= QtCore.Qt.ItemIsUserCheckable
        if group['editable']:
            flags |= QtCore.Qt.ItemIsEditable            
        return flags