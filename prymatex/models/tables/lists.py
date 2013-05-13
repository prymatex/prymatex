#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

class ListTableModel(QtCore.QAbstractTableModel):
    """Table Model"""
    def __init__(self, data, types=None, formats=None, xlabels=None, ylabels=None,
            editable=False, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.changes = {}
        self._data = data
        if self._data and not isinstance(self._data[0], (tuple, list)):
            self._fixed = True
            self._data = [ (e, ) for e in self._data ]

        if self._data:
            firstItem = self._data[0]
            types = types or [type(e) for e in firstItem]
            formats = formats or [ "%s" for _ in firstItem ]
        
        assert types is not None and formats is not None, "Type, format error"
        
        self._columnCount = len(types)
        self._types = types
        self._formats = formats if isinstance(formats, (list, tuple)) else\
            [ str(formats) for _ in range(self._columnCount) ]
        self._xlabels = xlabels
        self._ylabels = ylabels
        self._editable = editable if isinstance(editable, (list, tuple)) else\
            [ bool(editable) for _ in range(self._columnCount) ]
            

    def columnCount(self, qindex=QtCore.QModelIndex()):
        """Array column number"""
        return self._columnCount

    def rowCount(self, qindex=QtCore.QModelIndex()):
        """Array row number"""
        return len(self._data)

    def get_value(self, index):
        i = index.row()
        j = index.column()
        return self.changes.get((i, j), self._data[i][j])

    def get_format(self, index):
        return self._formats[index.column()]

    def is_editable(self, index):
        return self._editable[index.column()]

    def get_background(self, index):
        i = index.row()
        j = index.column()
        color = QtCore.Qt.green if (i, j) in self.changes else QtCore.Qt.red
        return color
        
    def get_type(self, index):
        return self._types[index.column()]
        
    def data(self, index, role=QtCore.Qt.DisplayRole):
        """Cell content"""
        if not index.isValid():
            return None
        value = self.get_value(index)
        if role == QtCore.Qt.DisplayRole:
            format = self.get_format(index)
            return format % value
        elif role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter
        elif role == QtCore.Qt.BackgroundColorRole:
            return self.get_background(index)


    def setData(self, index, value, role=QtCore.Qt.EditRole):
        """Cell content change"""
        if not index.isValid() or not self.is_editable(index):
            return False
        val = None
        ctype = self.get_type(index)
        if ctype in [ bool ]:
            val = value not in [ "false", "False", "0" ]
        else:
            try:
                val = ctype(value)
            except:
                pass
        
        if val is None:
            return False
            
        # Add change to self.changes
        self.changes[(index.row(), index.column())] = val
        self.dataChanged.emit(index, index)
        return True

    def flags(self, index):
        """Set editable flag"""
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        flags = QtCore.QAbstractTableModel.flags(self, index)
        
        if self.is_editable(index):
            flags |= QtCore.Qt.ItemIsEditable
        return flags

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        """Set header data"""
        if role != QtCore.Qt.DisplayRole:
            return None
        labels = self._xlabels if orientation == QtCore.Qt.Horizontal else self._ylabels
        if labels is None:
            return int(section)
        else:
            return labels[section]
