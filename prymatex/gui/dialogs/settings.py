#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui
from prymatex.core.components import PMXBaseDialog

from prymatex.ui.dialogs.treewidget import Ui_TreeWidgetDialog

class SettingsDialog(QtGui.QDialog, Ui_TreeWidgetDialog, PMXBaseDialog):
    """Settings dialog, it's hold by the application under configdialog property"""
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        PMXBaseDialog.__init__(self)
        self.setupUi(self)
        self.setObjectName("SettingsDialog")
        
        self.baseWindowTitle = self.windowTitle()
        
        self.treeView.setModel(self.application.profileManager.sortFilterSettingsProxyModel)

        self.stackedWidget = QtGui.QStackedWidget(self.splitter)
        self.widgetsLayout.addWidget(self.stackedWidget)


    def initialize(self, mainWindow):
        PMXBaseDialog.initialize(self, mainWindow)
        self.selectFirstIndex()


    def selectFirstIndex(self):
        firstIndex = self.treeView.model().index(0, 0)
        rect = self.treeView.visualRect(firstIndex)
        self.treeView.setSelection(rect, QtGui.QItemSelectionModel.ClearAndSelect)
        treeNode = self.treeView.model().node(firstIndex)
        self.setCurrentSettingWidget(treeNode)


    def on_lineEditFilter_textChanged(self, text):
        self.treeView.model().setFilterRegExp(QtCore.QRegExp(text, QtCore.Qt.CaseInsensitive))
        self.selectFirstIndex()


    def on_treeView_pressed(self, index):
        treeNode = self.treeView.model().node(index)
        self.setCurrentSettingWidget(treeNode)

    
    def on_treeView_activated(self, index):
        treeNode = self.treeView.model().node(index)
        self.setCurrentSettingWidget(treeNode)


    def setCurrentSettingWidget(self, widget):
        index = self.stackedWidget.indexOf(widget)
        if index == -1:
            index = self.stackedWidget.addWidget(widget)
        self.stackedWidget.setCurrentIndex(index)
        self.textLabelTitle.setText(widget.title())
        self.textLabelPixmap.setPixmap(widget.icon().pixmap(20, 20))
        self.setWindowTitle("%s - %s" % (self.baseWindowTitle, widget.title()))
