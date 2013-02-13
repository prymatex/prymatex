#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from prymatex.core.components import PMXBaseDialog

from prymatex.ui.dialogs.treewidget import Ui_TreeWidgetDialog
from prymatex.models.properties import (PropertyTreeNode, PropertiesTreeModel,
    PropertiesProxyModel)

class PropertiesDialog(QtGui.QDialog, Ui_TreeWidgetDialog, PMXBaseDialog):
    """Properties dialog, it's hold by the project docker"""
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        PMXBaseDialog.__init__(self)
        self.setupUi(self)
        self.setObjectName("PropertiesDialog")
        
        self.stackedWidget = QtGui.QStackedWidget(self.splitter)
        self.widgetsLayout.addWidget(self.stackedWidget)
    
    def setModel(self, propertiesModel):
        self.treeView.setModel(propertiesModel)
        
    def selectFirstIndex(self):
        firstIndex = self.treeView.model().index(0, 0)
        rect = self.treeView.visualRect(firstIndex)
        self.treeView.setSelection(rect, QtGui.QItemSelectionModel.ClearAndSelect)
        treeNode = self.treeView.model().node(firstIndex)
        self.setCurrentPropertyWidget(treeNode)

    def on_lineEditFilter_textChanged(self, text):
        self.treeView.model().setFilterRegExp(QtCore.QRegExp(text, QtCore.Qt.CaseInsensitive))
        self.selectFirstIndex()
    
    def on_treeView_pressed(self, index):
        treeNode = self.treeView.model().node(index)
        self.setCurrentPropertyWidget(treeNode)
        
    def on_treeView_activated(self, index):
        treeNode = self.treeView.model().node(index)
        self.setCurrentPropertyWidget(treeNode)
    
    def setCurrentPropertyWidget(self, widget):
        index = self.stackedWidget.indexOf(widget)
        if index == -1:
            index = self.stackedWidget.addWidget(widget)
        widget.edit(self.treeView.model().fileSystemItem)
        self.stackedWidget.setCurrentIndex(index)
        self.stackedWidget.setCurrentWidget(widget)
        self.textLabelTitle.setText(widget.title())
        self.textLabelPixmap.setPixmap(widget.icon().pixmap(20, 20))
        self.setWindowTitle("Properties - %s" % widget.title())

    
    def exec_(self, fileSystemItem):
        self.treeView.model().setFilterFileSystem(fileSystemItem)
        self.selectFirstIndex()
        return QtGui.QDialog.exec_(self)
        
