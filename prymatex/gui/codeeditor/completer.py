#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, Qt, QtWidgets, API
from prymatex.qt.extensions import HtmlLinkItemDelegate

from prymatex.core import config

# http://doc.qt.digia.com/4.6/tools-customcompleter.html
# ----------------------- Model
class CompleterListModel(QtCore.QAbstractListModel):
    def __init__(self, *args, **kwargs):
        """docstring for __init__"""
        super().__init__(*args, **kwargs)
        self.completions = []
    
    def setCompletions(self, completions):
        self.modelAboutToBeReset.emit()
        self.completions = completions
        self.modelReset.emit()
        
    def rowCount(self, parent=None):
        return len(self.completions)

    def index(self, row, column, parent = QtCore.QModelIndex()):
        if row < len(self.completions):
            return self.createIndex(row, column, parent)
        else:
            return QtCore.QModelIndex()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        completion = self.completions[index.row()]
        if role in (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole):
            return "<i>%s</i>" % completion
        elif role == QtCore.Qt.ToolTipRole:
            return completion
        elif role == QtCore.Qt.MatchRole:
            #return text.fuzzy_match(self.prefix, suggestion) and self.prefix or suggestion
            return completion

# ----------------------- Completer
class CodeEditorCompleter(QtWidgets.QCompleter):
    def __init__(self, editor):
        """docstring for __init__"""
        super().__init__(parent=editor)
        self.editor = editor
        self.__model = CompleterListModel(parent=editor)
        self.popup().setAlternatingRowColors(True)
        #self.popup().setItemDelegateForColumn(0, HtmlLinkItemDelegate(self.popup()))
        # Role
        self.setCompletionRole(QtCore.Qt.MatchRole)
        self.setWidget(self.editor)
    
    def setPalette(self, palette):
        self.popup().setPalette(palette)
        self.popup().viewport().setPalette(palette)
            
    def setCompletions(self, completions):
        self.__model.setCompletions(completions)
 
    def complete(self, rect):
        self.setModel(self.__model)
        rect.setWidth(self.popup().sizeHintForColumn(0)
            + self.popup().verticalScrollBar().sizeHint().width())
        super().complete(rect)
        self.popup().setCurrentIndex(self.completionModel().index(0,0))
