#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import fnmatch
import os

from prymatex.qt import QtCore, QtGui
from prymatex import resources

from prymatex.models.selectable import SelectableModelMixin

#====================================================
# Checkable List
#====================================================
class CheckableListModel(QtCore.QAbstractListModel):
    selectionChanged = QtCore.Signal()
    
    def __init__(self, parent = None): 
        QtCore.QAbstractListModel.__init__(self, parent)
        self.__items = []

    # ------------------ QtCore.QAbstractListModel methods
    def rowCount(self, parent = None):
        return len(self.__items)

    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        item = self.__items[index.row()]
        if role == QtCore.Qt.DisplayRole:
            return item["name"]
        elif role == QtCore.Qt.CheckStateRole:
            return item["selected"] and 2 or 0
        elif role == QtCore.Qt.ToolTipRole:
            return item

    def setData(self, index, data, role):
        item = self.__items[index.row()]
        if role == QtCore.Qt.CheckStateRole:
            item["selected"] = data
            self.selectionChanged.emit()
            return True

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable

    # ------------------ Custom functions
    def clear(self):
        self.__items = []
        self.selectionChanged.emit()

    def setSelected(self, item, selected=True):
        value = [k for k in self.__items if k["name"] == item]
        if value:
            value = value.pop()
            value["selected"] = selected
            self.selectionChanged.emit()
    
    def selectedItems(self):
        return [item["name"] for item in [item for item in self.__items if item["selected"]]]

    def selectItems(self, names):
        for item in self.__items:
            item["selected"] = item["name"] in names
        self.selectionChanged.emit()

    def unselectAllItems(self):
        self.selectItems([])

    # ------------------ Add remove keywords
    def addItem(self, item, selected=False):
        value = [k for k in self.__items if k["name"] == item]
        if not value:
            self.beginInsertRows(QtCore.QModelIndex(), len(self.__items), len(self.__items))
            self.__items.append({"name": item, "selected": selected})
            self.endInsertRows()
        
    def addItems(self, items):
        for item in items:
            self.addItem(item)

    def removeItem(self, item):
        value = [k for k in self.__items if k["name"] == item]
        if value:
            self.beginRemoveRows(QtCore.QModelIndex(), self.__items.index(value), self.__items.index(value))
            self.__items.remove(value)
            self.endRemoveRows()
                
    def removeItems(self, items):
        for item in items:
            self.removeItem(item)
