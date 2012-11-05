#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore

from prymatex import resources

#=========================================================
# Process
#=========================================================
class ExternalProcessTableModel(QtCore.QAbstractTableModel):
    STATES_STRING = {0: "NotRunning",
                     1: "Starting",
                     2: "Running" }
    STATES_ICONS = {0: resources.getIcon("porcess-not-running"),
                    1: resources.getIcon("porcess-starting"),
                    2: resources.getIcon("porcess-running") }
                    
    def __init__(self, manager, parent = None): 
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.manager = manager
        self.processItems = []

    def index(self, row, column, parent = None):
        return self.createIndex(row, column, self.processItems[row])
    
    def rowCount (self, parent = None):
        return len(self.processItems)
        
    def columnCount(self, parent):
        return 3

    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        item = self.processItems[index.row()]
        if role in [ QtCore.Qt.DisplayRole, QtCore.Qt.ToolTipRole ]:
            if index.column() == 0:
                return item["process"].pid()
            elif index.column() == 1:
                return item["description"]
            elif index.column() == 2:
                return self.STATES_STRING[item["process"].state()]
        elif role == QtCore.Qt.DecorationRole and index.column() == 0:
            return self.STATES_ICONS[item["process"].state()]
            
    def findRowIndex(self, process):
        items = filter(lambda item: item["process"] == process, self.processItems)
        assert len(items) == 1, "No puede tener mas de uno"
        return self.processItems.index(items[0])
        
    def processForIndex(self, index):
        return self.processItems[index.row()]["process"]
    
    def appendProcess(self, process, description = ""):
        self.beginInsertRows(QtCore.QModelIndex(), len(self.processItems), len(self.processItems))
        self.processItems.append({ "process":  process, "description": description })
        self.endInsertRows()

    def removeProcess(self, process):
        index = self.findRowIndex(process)
        self.beginRemoveRows(QtCore.QModelIndex(), index, index)
        self.processItems.pop( index )
        self.endRemoveRows()
        
    def getAllItems(self):
        return map(lambda item: item["process"], self.processItems)
