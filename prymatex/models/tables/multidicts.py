#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

class SelectableMultiDictTableModel(QtCore.QAbstractTableModel):
    COLUMN_NAMES = 0
    COLUMN_VALUES = 1
    def __init__(self, parent = None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.changes = {}
        self.selected = {}
        self.dictionaries = []
        self.lastEditableDictionary = None

    def mapFromData(self, data):
        #Return variable as list of dicts [{'name': name, 'value': value, 'selected': True}...]
        if data is None:
            return []
        elif hasattr(data, 'iteritems'):
            return map(lambda (name, value): {'name': name, 'value': value, 'selected': True}, data.iteritems())
        return data

    def dictionaryNames(self):
        return map(lambda d: d["name"], self.dictionaries)
        

    def dictionaryByName(self, name):
        for dictionary in self.dictionaries:
            if dictionary['name'] == name:
                return dictionary

    def addDictionary(self, name, data, editable = False, selectable = False, visible = True):
        dictionary = {
            'name': name,
            'data': self.mapFromData(data),
            'editable': editable,
            'selectable': selectable,
            'visible': visible
        } 
        self.dictionaries.append(dictionary)
        if editable:
            self.lastEditableDictionary = dictionary
        self.layoutChanged.emit()
    
    def clear(self):
        self.changes = {}
        self.selected = {}
        self.dictionaries = []
        self.layoutChanged.emit()
        
    def setVisibility(self, name, visible):
        dictionary = self.dictionaryByName(name)
        dictionary['visible'] = visible
        self.layoutChanged.emit()
        
    def mapToDictionary(self, index):
        currentDict = None
        for currentDict in self.dictionaries:
            if currentDict["visible"]:
                varCount = len(currentDict['data'])
                if index < varCount:
                    break
                index -= varCount
        return index, currentDict

    def variableGroupTablePosition(self, dictionary, top = True):
        position = 0
        for currentDict in self.dictionaries:
            if currentDict["visible"]:
                if currentDict == dictionary:
                    break
                position += len(currentDict['data'])
        if not top:
            position += len(currentDict['data'])
        return position

    def allEditableVariables(self):
        return reduce(lambda l, dictionary: l + (dictionary['editable'] and dictionary['data'] or []), self.dictionaries, [])
    
    def get_value(self, index):
        i = index.row()
        j = index.column()
        row, dictionary = self.mapToDictionary(i)
        value = self.changes.get((i, j), dictionary["data"][row][j == self.COLUMN_NAMES and "name" or "value"])
        selected = self.selected.get((i, j), dictionary["data"][row]["selected"])
        return value, selected, dictionary

        
    def rowCount(self, parent = None):
        if not self.dictionaries:
            return 0
        return reduce(lambda count, dictionary: count + (dictionary['visible'] and len(dictionary['data']) or 0), self.dictionaries, 0)
    
    def columnCount(self, parent = None):
        return 2
    
    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid(): 
            return None
        value, selected, dictionary = self.get_value(index)
        if role == QtCore.Qt.CheckStateRole and index.column() == 0 and dictionary['selectable']:
            return QtCore.Qt.Unchecked if not selected else QtCore.Qt.Checked
        elif role in [ QtCore.Qt.DisplayRole, QtCore.Qt.EditRole ]:
            return value
        
    def setData(self, index, value, role):
        """Retornar verdadero si se puedo hacer el cambio, falso en caso contrario"""

        if not index.isValid(): return False
        row, dictionary = self.mapToDictionary(index.row())

        if role == QtCore.Qt.EditRole:
            if index.column() == self.COLUMN_NAMES and any(map(lambda v: v['name'] == value, dictionary['data'])):
                return False
            else:
                self.changes[(index.row(), index.column())] = value
            self.dataChanged.emit(index, index)
            return True
        elif role == QtCore.Qt.CheckStateRole:
            self.changes[(index.row(), index.column())] = value is QtCore.Qt.Checked
            self.dataChanged.emit(index, index)
            return True
        return False
        
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                if section == 0:
                    return "Name"
                elif section == 1:
                    return "Value"

    def insertVariable(self, name = None):
        dictionary = self.dictionaryByName(name) if name else self.lastEditableDictionary
        if dictionary is not None and dictionary['editable']:
            position = self.variableGroupTablePosition(dictionary)
            self.beginInsertRows(QtCore.QModelIndex(), position, position)
            dictionary['data'].insert(0, {'variable': "", 'value': "", 'selected': True})
            self.endInsertRows()

    def removeRows(self, position, rows, parent = QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)
        row, dictionary = self.mapToDictionary(position)
        if not dictionary["editable"]:
            return False
        for _ in range(rows):
            dictionary['data'].pop(row)
        self.endRemoveRows()
        return True

    def flags(self, index):
        row, dictionary = self.mapToDictionary(index.row())
        flags = QtCore.QAbstractTableModel.flags(self, index)
        if dictionary['selectable']:
            flags |= QtCore.Qt.ItemIsUserCheckable
        if dictionary['editable']:
            flags |= QtCore.Qt.ItemIsEditable            
        return flags
