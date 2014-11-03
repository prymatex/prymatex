#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets

from prymatex.core.components import PrymatexDialog

from prymatex.ui.dialogs.treewidget import Ui_TreeWidgetDialog
from prymatex.models.properties import (PropertyTreeNode, PropertiesTreeModel,
    PropertiesProxyModel)

class PropertiesDialog(PrymatexDialog, Ui_TreeWidgetDialog, QtWidgets.QDialog):
    """Properties dialog, it's hold by the project docker"""
    def __init__(self, **kwargs):
        super(PropertiesDialog, self).__init__(**kwargs)
        self.setupUi(self)
        self.setObjectName("PropertiesDialog")
        
        self.stackedWidget = QtWidgets.QStackedWidget(self.splitter)
        self.widgetsLayout.addWidget(self.stackedWidget)

        self.finished.connect(self.on_propertiesDialog_finished)
    
    def on_propertiesDialog_finished(self, code):
        self.saveChanges()

    def setModel(self, propertiesModel):
        for widget in propertiesModel.configNodes():
            if isinstance(widget, QtWidgets.QWidget) and self.stackedWidget.indexOf(widget) == -1:
                self.stackedWidget.addWidget(widget)
        self.treeView.setModel(propertiesModel)
        
    def selectFirstIndex(self):
        firstIndex = self.treeView.model().index(0, 0)
        rect = self.treeView.visualRect(firstIndex)
        self.treeView.setSelection(rect, QtCore.QItemSelectionModel.ClearAndSelect)
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
        self.saveChanges()
        index = self.stackedWidget.indexOf(widget)
        widget.edit(self.treeView.model().fileSystemItem)
        self.stackedWidget.setCurrentIndex(index)
        self.stackedWidget.setCurrentWidget(widget)
        self.textLabelTitle.setText(widget.title())
        self.textLabelPixmap.setPixmap(widget.icon().pixmap(20, 20))
        self.setWindowTitle("Properties - %s" % widget.title())

    def saveChanges(self):
        self.stackedWidget.currentWidget().saveChanges()

    def exec_(self, fileSystemItem):
        self.treeView.model().setFilterFileSystem(fileSystemItem)
        self.selectFirstIndex()
        return super(PropertiesDialog, self).exec_()
        
