# -*- coding: utf-8 -*-
# Copyright © 2011 by Vinay Sajip. All rights reserved. See accompanying LICENSE.txt for details.
from qt import QtCore, QtGui, Qt

from ui_colprefs import Ui_ColPrefsDialog
import copy

class ColumnItem(QtGui.QListWidgetItem):
    def __init__(self, parent, column):
        super(ColumnItem, self).__init__(parent, QtGui.QListWidgetItem.UserType)
        self.column = column

    def data(self, role):
        result = None
        if role == Qt.DisplayRole:
            result = self.column.title
        elif role == Qt.CheckStateRole:
            if self.column.visible:
                result = Qt.Checked
            else:
                result = Qt.Unchecked
        return result

    def setData(self, role, value):
        if role == Qt.CheckStateRole:
            self.column.visible = value

class ColPrefsDialog(QtGui.QDialog, Ui_ColPrefsDialog):
    def __init__(self, parent, columns):
        super(ColPrefsDialog, self).__init__(parent)
        self.columns = [copy.copy(c) for c in columns]
        self.setupUi(self)
        self.connect(self, QtCore.SIGNAL('accepted()'), self.on_accept)

    def setupUi(self, w):
        super(ColPrefsDialog, self).setupUi(w)
        thelist = self.list
        thelist.setDragDropMode(QtGui.QAbstractItemView.InternalMove)

        for col in self.columns:
            item = ColumnItem(thelist, col)

    def on_accept(self):
        thelist = self.list
        n = thelist.count()
        columns = []
        for i in range(n):
            item = thelist.item(i)
            columns.append(item.column)
        self.columns = columns
