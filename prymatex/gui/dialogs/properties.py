#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex.ui.dialogs.settings import Ui_SettingsDialog

class PMXSettingsDialog(QtGui.QDialog, Ui_SettingsDialog):
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        
        self.treeModel = tree.TreeModel(self)
        
        self.proxyModelSettings = QtGui.QSortFilterProxyModel(self)
        self.proxyModelSettings.setSourceModel(self.treeModel)
        
        self.treeViewSetting.setModel(self.proxyModelSettings)
        
    def on_lineEditFilter_textChanged(self, text):
        self.proxyModelSettings.setFilterRegExp(QtCore.QRegExp(text, QtCore.Qt.CaseInsensitive))
    
    def on_treeViewSettings_activated(self, index):
        self.treeTextToSectionTitle(index)
    
    def treeTextToSectionTitle(self, index = None):
        ''' Grab the index title taking into account inital settings '''
        if index:
            sIndex = self.proxyModelSettings.mapToSource(index)
        else:
            sIndex = self.proxyModelSettings.index(0, 0)
        item = self.model.itemFromIndex(sIndex)
        if index:
            self.container.layout().setCurrentIndex(item.stackIndex)
        title = self.container.layout().currentWidget().windowTitle()
        #self.labelTitle.setText(title)
        self.updateTitle(title)
    
    def updateTitle(self, subTitle):
        self.setWindowTitle("%s - %s" % (self.baseWindowTitle, subTitle))
    
    firstTitleTaken = False
    def showEvent(self, event):
        if not self.firstTitleTaken:
            self.treeTextToSectionTitle(index = None)
            self.firstTitleTaken = True
        super(PMXSettingsDialog, self).showEvent(event)
    
    def register(self, widgetClass, parentNode = None):
        widgetClass.application = self.application
        widget = widgetClass(self)
        index = self.stackLayout.addWidget(widget)
        item = PMXSettingsItem(widget.windowTitle(), index)
        item.setIcon(widget.windowIcon())
        self.model.appendRow(item)
        