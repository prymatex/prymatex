#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex.ui.dialogs.settings import Ui_SettingsDialog

class PMXSettingsDialog(QtGui.QDialog, Ui_SettingsDialog):
    """
    Settings dialog, it's hold by the application under
    configdialog property
    """
    def __init__(self, application):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.application = application
        
        self.baseWindowTitle = self.windowTitle()
        
        self.model = QtGui.QStandardItemModel(self)
        
        self.proxyModelSettings = QtGui.QSortFilterProxyModel(self)
        self.proxyModelSettings.setSourceModel(self.model)
        
        self.treeViewSetting.setModel(self.proxyModelSettings)
        
        self.stackedWidget = QtGui.QStackedWidget()
        self.stackedWidget.setFrameShape(QtGui.QFrame.StyledPanel)
        self.stackedWidget.setFrameShadow(QtGui.QFrame.Sunken)
        self.settingLayout.insertWidget(0, self.stackedWidget)
        
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
    
    def register(self, widget):
        index = self.stackedWidget.addWidget(widget)
        #item = PMXSettingsItem(widget.windowTitle(), index)
        #item.setIcon(widget.windowIcon())
        #self.model.appendRow(item)
        