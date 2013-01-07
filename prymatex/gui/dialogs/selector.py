#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from prymatex.delegates import HtmlItemDelegate
from prymatex.ui.dialogs.selector import Ui_SelectorDialog


class SelectorDialog(QtGui.QDialog, Ui_SelectorDialog):
    '''
    This dialog allow the user to search through commands, snippets and macros in the current scope easily.
    An instance is hold in the main window and triggered with an action.
    '''
    TIMEOUT_SORT = 2000
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        
        self.model = None
        self.sortTimer = QtCore.QTimer(self)
        self.sortTimer.timeout.connect(self.on_sortTimer_timeout)
        self.sortTimer.setSingleShot(True)
        
        self.lineFilter.installEventFilter(self)
        self.listItems.installEventFilter(self)
        
        self.setWindowFlags(QtCore.Qt.Dialog)
        self.listItems.setItemDelegate(HtmlItemDelegate(self))
        self.listItems.setResizeMode(QtGui.QListView.Adjust)


    def setModel(self, model):
        if self.model != model:
            self.lineFilter.setVisible(model.isFilterable())
            if model.isFilterable():
                self.lineFilter.clear()
                self.lineFilter.setFocus()
            self.model = model
            self.listItems.setModel(self.model)
        else:
            self.lineFilter.clear()
            self.lineFilter.setFocus()
        self.listItems.setCurrentIndex(self.model.index(0, 0))


    def select(self, model, title = "Select item"):
        """ @param items: List of rows, each row has a list of columns, and each column is a dict with "title", "image", "tooltip"
            @return: The selected row """

        self.setWindowTitle(title)
        self.selected = None
        
        model.initialize(self)
        self.setModel(model)
        
        self.exec_()
        self.sortTimer.stop()
        
        return self.selected
    
    
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


    def on_sortTimer_timeout(self):
        self.model.sort(0)
        self.listItems.setCurrentIndex(self.model.index(0, 0))
        
        
    # Not autoconnect, connect on model's needs
    def on_lineFilter_textChanged(self, text):
        self.model.setFilterString(text)
        if self.model.isSortable() and not self.sortTimer.isActive():
            self.sortTimer.start(self.TIMEOUT_SORT)
        else:
            self.listItems.setCurrentIndex(self.model.index(0, 0))


    def on_listItems_activated(self, index):
        self.selected = self.model.item(index)
        self.accept()


    def on_listItems_doubleClicked(self, index):
        self.selected = self.model.item(index)
        self.accept()


    def on_lineFilter_returnPressed(self):
        indexes = self.listItems.selectedIndexes()
        if indexes:
            self.selected = self.model.item(indexes[0])
            self.accept()
