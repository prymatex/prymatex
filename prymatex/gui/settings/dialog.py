#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from prymatex.core.base import PMXObject
from prymatex.ui.settings.dialog import Ui_SettingsDialog

class PMXSettingsItem(QtGui.QStandardItem):
    def __init__(self, name, index, parent = None):
        QtGui.QStandardItem.__init__(self, parent)    
        self.setText(name)
        self.setEditable(False)
        self.stackIndex = index

class PMXSettingsDialog(QtGui.QDialog, Ui_SettingsDialog, PMXObject):
    """
    Settings dialog, it's hold by the application under
    configdialog property
    """
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.model = QtGui.QStandardItemModel(self)
        
        self.proxyModelSettings = QtGui.QSortFilterProxyModel(self)
        self.proxyModelSettings.setSourceModel(self.model)
        
        self.treeViewSettings.setModel(self.proxyModelSettings)
        self.treeViewSettings.setHeaderHidden(True)
        self.treeViewSettings.setAnimated(True)
        
        self.stackLayout = QtGui.QStackedLayout()
        self.container.setLayout(self.stackLayout)
        
    def on_lineEditFilter_textChanged(self, text):
        self.proxyModelSettings.setFilterRegExp(QtCore.QRegExp(text, QtCore.Qt.CaseInsensitive))
    
    def on_treeViewSettings_activated(self, index):
        sIndex = self.proxyModelSettings.mapToSource(index)
        item = self.model.itemFromIndex(sIndex)
        self.container.layout().setCurrentIndex(item.stackIndex)
        title = self.container.layout().currentWidget().windowTitle()
        self.labelTitle.setText(title)
        
    def register(self, widget, parentNode = None):
        index = self.stackLayout.addWidget(widget)
        item = PMXSettingsItem(widget.windowTitle(), index)
        item.setIcon(widget.windowIcon())
        self.model.appendRow(item)
        
    