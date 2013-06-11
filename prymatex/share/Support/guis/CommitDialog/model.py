#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

class FilesTableModel(QtCore.QAbstractTableModel):
    HEADER_NAMES = ["S", "File"]
    def __init__(self, parent = None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.files = []
        
    def rowCount(self, parent = None):
        return len(self.files)
    
    def columnCount(self, parent = None):
        return len(self.HEADER_NAMES)
        
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.HEADER_NAMES[section]
    
    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid(): 
            return None
        f = self.files[ index.row() ]
        
        if role == QtCore.Qt.CheckStateRole and index.column() == 0:
            return QtCore.Qt.Checked if f['checked'] else QtCore.Qt.Unchecked
        elif role in [ QtCore.Qt.DisplayRole, QtCore.Qt.EditRole ]:
            if index.column() == 0:
                return f['status']
            elif index.column() == 1:
                return f['path']
        elif role in [QtCore.Qt.ForegroundRole]:
            if index.column() == 0:
                return QtCore.Qt.blue
        elif role in [QtCore.Qt.BackgroundColorRole]:
            if index.column() == 0:
                return QtCore.Qt.red

    def setData(self, index, value, role):
        """Retornar verdadero si se puedo hacer el cambio, falso en caso contrario"""

        if not index.isValid(): return False
        f = self.files[ index.row() ]
        
        if role == QtCore.Qt.CheckStateRole:
            f['checked'] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def setFiles(self, files):
        print(files)
        self.files = files
        self.layoutChanged.emit()
        
    def addFile(self, f):
        self.files.append(f)
        self.layoutChanged.emit()
    
    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable
        
    def selectedFiles(self):
        return [f["path"] for f in [f for f in self.files if f["checked"]]]