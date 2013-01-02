#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections

from prymatex.qt import QtCore, QtGui

from prymatex.models.selectable import SelectableModel, SelectableProxyModel
from prymatex.models.delegates import HtmlItemDelegate
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
        self.listItems.installEventFilter(self)
        
        self.setWindowFlags(QtCore.Qt.Dialog)
        self.listItems.setItemDelegate(HtmlItemDelegate(self))
        self.listItems.setResizeMode(QtGui.QListView.Adjust)
        
    def select(self, data, title = "Select item", 
        filterFunction = lambda text, item: str(item).find(text) != -1,
        sortFunction = lambda leftItem, rightItem: True):
        """ @param items: List of rows, each row has a list of columns, and each column is a dict with "title", "image", "tooltip"
            @return: The selected row """

        self.setWindowTitle(title)
        
        self.selectedRow = None
        self.lineFilter.clear()
        self.lineFilter.setFocus()
        
        model = None
        if isinstance(data, collections.Iterable):
            self.dataModel = SelectableProxyModel(filterFunction, sortFunction, parent = self)
            self.dataModel.setSourceModel(SelectableModel(list(data)))
        elif isinstance(data, QtCore.QAbstractItemModel):
            self.dataModel = data
        else:
            raise Exception("No Data")
        self.listItems.setModel(self.dataModel)
                
        self.listItems.setCurrentIndex(self.dataModel.index(0, 0))
        self.exec_()
        
        return self.selectedRow
    
    
    def eventFilter(self, obj, event):
        '''Filters lineEdit key strokes to select model items'''
        if obj is self.lineFilter:
            if event.type() == QtCore.QEvent.KeyPress:
                key = event.key() 
                if key == QtCore.Qt.Key_Down:
                    self.listItems.setFocus()
                    self.listItems.event(event)
                    obj.setFocus()
                    return True
                elif key == QtCore.Qt.Key_Up:
                    self.listItems.setFocus()
                    self.listItems.event(event)
                    obj.setFocus()
                    return True
        elif obj is self.listItems:
            if event.type() == QtCore.QEvent.KeyPress:
                self.lineFilter.setFocus()
                self.lineFilter.event(event)
                return True
        return QtGui.QWidget.eventFilter(self, obj, event)
            
    def on_lineFilter_textChanged(self, text):
        self.dataModel.setFilterString(text)
        self.listItems.setCurrentIndex(self.dataModel.index(0, 0))
        
    def on_listItems_activated(self, index):
        self.selectedRow = self.dataModel.mapToSourceItem(index)
        self.accept()
        
    def on_listItems_doubleClicked(self, index):
        self.selectedRow = self.dataModel.mapToSourceItem(index)
        self.accept()
    
    def on_lineFilter_returnPressed(self):
        indexes = self.listItems.selectedIndexes()
        if indexes:
            self.selectedRow = self.dataModel.mapToSourceItem(indexes[0])
            self.accept()
