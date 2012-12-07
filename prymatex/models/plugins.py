#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore

from prymatex import resources

#=========================================================
# Plugins Table Model
#=========================================================
class PluginsTableModel(QtCore.QAbstractTableModel):
    def __init__(self, manager, parent = None): 
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.pluginManager = manager
        self.pluginDescriptors = self.pluginManager.plugins.values()

    def index(self, row, column, parent = None):
        return self.createIndex(row, column, self.pluginDescriptors[row])
    
    def rowCount (self, parent = None):
        return len(self.pluginDescriptors)
        
    def columnCount(self, parent):
        return 3

    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        plugin = self.pluginDescriptors[index.row()]
        if role in [ QtCore.Qt.DisplayRole, QtCore.Qt.ToolTipRole ]:
            if index.column() == 0:
                return plugin.id
            elif index.column() == 1:
                return plugin.name
            elif index.column() == 1:
                return plugin.description
        elif role == QtCore.Qt.DecorationRole and index.column() == 0:
            return plugin.icon
