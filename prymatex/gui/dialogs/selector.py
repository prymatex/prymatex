#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections

from prymatex.qt import QtCore, QtGui

from prymatex.models.selectable import SelectableModel, SelectableProxyModel
from prymatex.models.delegates import HtmlDelegate
from prymatex.ui.dialogs.selector import Ui_SelectorDialog

class SelectorDialog(QtGui.QDialog, Ui_SelectorDialog):
    '''
    This dialog allow the user to search through commands, snippets and macros in the current scope easily.
    An instance is hold in the main window and triggered with an action.
    '''
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        
        self.lineFilter.installEventFilter(self)
        self.tableItems.installEventFilter(self)
        
        self.setWindowFlags(QtCore.Qt.Dialog)
        self.tableItems.setItemDelegate(HtmlDelegate())
        
    def select(self, data, title = "Select item"):
        """ @param items: List of rows, each row has a list of columns, and each column is a dict with "title", "image", "tooltip"
            @return: The selected row """

        self.setWindowTitle(title)
        
        self.selectedRow = None
        self.lineFilter.clear()
        self.lineFilter.setFocus()
        
        model = None
        if isinstance(data, collections.Iterable):
            self.dataModel = SelectableProxyModel(self)
            self.dataModel.setSourceModel(SelectableModel(list(data)))
        elif isinstance(data, QtCore.QAbstractItemModel):
            self.dataModel = data
        else:
            raise Exception("No Data")
        self.dataModel.rowsInserted.connect(self.on_dataModel_dataModified)
        self.dataModel.rowsRemoved.connect(self.on_dataModel_dataModified)
        self.dataModel.columnsInserted.connect(self.on_dataModel_dataModified)
        self.dataModel.columnsRemoved.connect(self.on_dataModel_dataModified)
        
        self.tableItems.setModel(self.dataModel)
        self.tableItems.resizeColumnsToContents()
        self.tableItems.resizeRowsToContents()
                
        self.tableItems.selectRow(0)
        self.exec_()
        
        self.dataModel.rowsInserted.disconnect(self.on_dataModel_dataModified)
        self.dataModel.rowsRemoved.disconnect(self.on_dataModel_dataModified)
        self.dataModel.columnsInserted.disconnect(self.on_dataModel_dataModified)
        self.dataModel.columnsRemoved.disconnect(self.on_dataModel_dataModified)        
        
        return self.selectedRow
    
    # ------------------ Model Signals
    def on_dataModel_dataModified(self, parent, start, end):
        self.tableItems.resizeRowsToContents()
        self.tableItems.resizeColumnsToContents()
        self.tableItems.selectRow(0)
    
    def eventFilter(self, obj, event):
        '''Filters lineEdit key strokes to select model items'''
        if obj is self.lineFilter:
            if event.type() == QtCore.QEvent.KeyPress:
                key = event.key() 
                if key == QtCore.Qt.Key_Down:
                    self.tableItems.setFocus()
                    self.tableItems.event(event)
                    obj.setFocus()
                    return True
                elif key == QtCore.Qt.Key_Up:
                    self.tableItems.setFocus()
                    self.tableItems.event(event)
                    obj.setFocus()
                    return True
        elif obj is self.tableItems:
            if event.type() == QtCore.QEvent.KeyPress:
                self.lineFilter.setFocus()
                self.lineFilter.event(event)
                return True
        return QtGui.QWidget.eventFilter(self, obj, event)
            
    def on_lineFilter_textChanged(self, text):
        self.dataModel.setFilterRegExp(QtCore.QRegExp("*%s*" % text, QtCore.Qt.CaseInsensitive, QtCore.QRegExp.Wildcard))
        self.tableItems.selectRow(0)
        
    def on_tableItems_activated(self, index):
        self.selectedRow = self.dataModel.mapToSourceRow(index)
        self.accept()
        
    def on_tableItems_doubleClicked(self, index):
        self.selectedRow = self.dataModel.mapToSourceRow(index)
        self.accept()
    
    def on_lineFilter_returnPressed(self):
        indexes = self.tableItems.selectedIndexes()
        if indexes:
            self.selectedRow = self.dataModel.mapToSourceRow(indexes[0])
            self.accept()
