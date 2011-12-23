#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from prymatex.ui.dialogs.bundleselector import Ui_BundleSelectorDialog

class PMXBundleSelectorDialog(QtGui.QDialog, Ui_BundleSelectorDialog):
    '''
    This dialog allow the user to search through commands, snippets and macros in the current scope easily.
    An instance is hold in the main window and triggered with an action.
    '''
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        
        self.lineFilter.installEventFilter(self)
        self.tableBundleItems.installEventFilter(self)
        
        self.setWindowFlags(QtCore.Qt.Dialog)
        self.model = QtGui.QStandardItemModel(self)
        self.proxy = QtGui.QSortFilterProxyModel(self)
        self.tableBundleItems.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.proxy.setSourceModel(self.model)
        self.tableBundleItems.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.tableBundleItems.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.tableBundleItems.setModel(self.proxy)
        
    def select(self, items):
        self.item = None
        self.items = items
        self.model.clear()
        self.lineFilter.clear()
        self.lineFilter.setFocus()
        for item in items:
            self.model.appendRow([ QtGui.QStandardItem(QtGui.QIcon(item.icon), item.name), QtGui.QStandardItem(item.trigger) ])
        self.tableBundleItems.selectRow(0)
        self.exec_()
        return self.item
    
    def eventFilter(self, obj, event):
        '''Filters lineEdit key strokes to select model items'''
        if obj is self.lineFilter:
            if event.type() == QtCore.QEvent.KeyPress:
                key = event.key() 
                if key == QtCore.Qt.Key_Down:
                    self.tableBundleItems.setFocus()
                    self.tableBundleItems.event(event)
                    obj.setFocus()
                    return True
                elif key == QtCore.Qt.Key_Up:
                    self.tableBundleItems.setFocus()
                    self.tableBundleItems.event(event)
                    obj.setFocus()
                    return True
        elif obj is self.tableBundleItems:
            if event.type() == QtCore.QEvent.KeyPress:
                self.lineFilter.setFocus()
                self.lineFilter.event(event)
                return True
        return QtGui.QWidget.eventFilter(self, obj, event)
            
    def on_lineFilter_textChanged(self, text):
        regexp = QtCore.QRegExp("*%s*" % text, QtCore.Qt.CaseInsensitive, QtCore.QRegExp.Wildcard)
        self.proxy.setFilterRegExp(regexp)
        self.tableBundleItems.selectRow(0)
        
    def on_tableBundleItems_activated(self, index):
        sIndex = self.proxy.mapToSource(index)
        self.item = self.items[sIndex.row()]
        self.accept()
        
    def on_tableBundleItems_doubleClicked(self, index):
        sIndex = self.proxy.mapToSource(index)
        self.item = self.items[sIndex.row()]
        self.accept()
    
    
        
    def on_lineFilter_returnPressed(self):
        index = self.tableBundleItems.selectedIndexes()[0]
        if index.isValid():
            sIndex = self.proxy.mapToSource(index)
            self.item = self.items[sIndex.row()]
            self.accept()