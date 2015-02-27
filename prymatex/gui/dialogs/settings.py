#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.core.components import PrymatexDialog

from prymatex.ui.dialogs.treewidget import Ui_TreeWidgetDialog

class SettingsDialog(PrymatexDialog, Ui_TreeWidgetDialog, QtWidgets.QDialog):
    """Settings dialog, it's hold by the application under configdialog property"""
    def __init__(self, **kwargs):
        super(SettingsDialog, self).__init__(**kwargs)
        self.setupUi(self)
        self.setObjectName("SettingsDialog")
        
        self.treeView.setModel(self.application().settingsManager.sortFilterSettingsProxyModel)

        self.stackedWidget = QtWidgets.QStackedWidget(self.splitter)
        self.widgetsLayout.addWidget(self.stackedWidget)

    def initialize(self, **kwargs):
        super(SettingsDialog, self).initialize(**kwargs)
        self.selectFirstIndex()

    def selectFirstIndex(self):
        firstIndex = self.treeView.model().index(0, 0)
        rect = self.treeView.visualRect(firstIndex)
        self.treeView.setSelection(rect, QtCore.QItemSelectionModel.ClearAndSelect)
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
        self.setWindowTitle("Settings - %s" % widget.title())
