#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

#====================================================
# Themes Style Table Model
#====================================================
class ThemeStylesTableModel(QtCore.QAbstractTableModel):
    def __init__(self, manager, parent = None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.manager = manager
        self.styles = []
        self.headers = ['Element', 'Fg', 'Bg', 'Font Style']

    # ---------------------- QtCore.QAbstractTableModel overrides
    def rowCount(self, parent):
        return len(self.styles)

    def columnCount(self, parent):
        return 4

    def data(self, index, role):
        if not index.isValid(): 
            return QtCore.QVariant() 
        column = index.column()
        item = self.styles[index.row()]
        style = item.styleItem()
        if role in [ QtCore.Qt.DisplayRole, QtCore.Qt.EditRole ]:
            if column == 0:
                return style.name
            elif column == 1:
                return item.foreground()
            elif column == 2:
                return item.background()
            elif column == 3:
                return item.fontStyle()
        elif role == QtCore.Qt.FontRole:
            if column == 0:
                font = QtGui.QFont()
                if 'bold' in item.fontStyle():
                    font.setBold(True)
                if 'underline' in item.fontStyle():
                    font.setUnderline(True)
                if 'italic' in item.fontStyle():
                    font.setItalic(True)
                return font
        elif role is QtCore.Qt.ForegroundRole:
            if column == 0:
                return item.foreground()
        elif role is QtCore.Qt.BackgroundColorRole:
            if column == 0:
                return item.background()
            elif column == 1:
                return item.foreground()
            elif column == 2:
                return item.background()
        elif role is QtCore.Qt.UUIDRole:
            return style.uuidAsText()

    def setData(self, index, value, role):
        """Retornar verdadero si se puedo hacer el camio, falso en caso contratio"""
        if not index.isValid(): return False

        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()
            item = self.styles[row]
            style = item.styleItem()
            if column == 0:
                self.manager.updateThemeStyle(style, name=value)
            elif column == 1:
                self.manager.updateThemeStyle(style, settings={'foreground':value })
            elif column == 2:
                self.manager.updateThemeStyle(style, settings={'background':value })
            elif column == 3:
                self.manager.updateThemeStyle(style, settings={'fontStyle':" ".join(value) })
            self.dataChanged.emit(index, index)
            return True
        return False

    def flags(self, index):
        if not index.isValid():  
            return QtCore.Qt.NoItemFlags  
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.headers[section]

    def index(self, row, column, parent = QtCore.QModelIndex()):
        style = self.styles[row]
        if style:
            return self.createIndex(row, column, style)
        else:
            return QtCore.QModelIndex()

    # -------------------- Custom functions
    def style(self, index):
        if index.isValid():
            return index.internalPointer()
    
    def appendStyle(self, style):
        self.beginInsertRows(QtCore.QModelIndex(), len(self.styles), len(self.styles))
        self.styles.append(style)
        self.endInsertRows()

    def removeStyle(self, style):
        index = self.styles.index(style)
        self.beginRemoveRows(QtCore.QModelIndex(), index, index)
        self.styles.remove(style)
        self.endRemoveRows()
