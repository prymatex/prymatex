#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import fnmatch
import os

from prymatex.qt import QtCore, QtGui
from prymatex import resources

from prymatex.utils import text as texttools
from prymatex.models.selectable import SelectableModelMixin

#====================================================
# Checkable List
#====================================================
class CheckableListModel(QtCore.QAbstractListModel):
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
            return item["selected"]
        elif role == QtCore.Qt.ToolTipRole:
            return item


    def setData(self, index, data, role):
        item = self.__items[index.row()]
        if role == QtCore.Qt.CheckStateRole:
            item["selected"] = data
            self.dataChanged.emit(index, index)
            return True


    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable


    # ------------------ Custom functions
    def clear(self):
        for item in self.__items:
            item["selected"] = 0


    def setSelected(self, item, selected = True):
        value = filter(lambda k: k["name"] == item, self.__items)
        if value:
            value = value.pop()
            index = self.__items.index(value)
            value["selected"] = selected and 2 or 0
            index = self.index(index)
            self.dataChanged.emit(index, index)
    

    def selectedItems(self):
        return map(lambda item: item["name"], filter(lambda item: item["selected"] == 2, self.__items))


    # ------------------ Add remove keywords
    def addItem(self, item, selected = False):
        value = filter(lambda k: k["name"] == item, self.__items)
        if not value:
            self.beginInsertRows(QtCore.QModelIndex(), len(self.__items), len(self.__items))
            self.__items.append({"name": item, "selected": selected and 2 or 0})
            self.endInsertRows()
        
    def addItems(self, items):
        for item in items:
            self.addItem(item)


    def removeItem(self, item):
        value = filter(lambda k: k["name"] == item, self.__items)
        if value:
            self.beginRemoveRows(QtCore.QModelIndex(), self.__items.index(value), self.__items.index(value))
            self.__items.remove(value)
            self.endRemoveRows()
                
    def removeItems(self, items):
        for item in items:
            self.removeItem(item)