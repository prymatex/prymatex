#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex.ui.dialogs.settings import Ui_SettingsDialog
from prymatex.gui.settings.models import PMXSettingsModel, PMXSettingsProxyModel

class PMXPropertiesDialog(QtGui.QDialog, Ui_SettingsDialog):
    """Properties dialog, it's hold by the project docker
    """
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        
        self.baseWindowTitle = self.windowTitle()
        
        self.model = PMXSettingsModel(self)
        
        self.proxyModelProperties = PMXSettingsProxyModel(self)
        self.proxyModelProperties.setSourceModel(self.model)
        
        self.treeViewSetting.setModel(self.proxyModelProperties)
        
        self.stackedWidget = QtGui.QStackedWidget(self.splitter)
        self.stackedWidget.setFrameShape(QtGui.QFrame.StyledPanel)
        self.stackedWidget.setFrameShadow(QtGui.QFrame.Sunken)
        
        self.widgetsLayout.addWidget(self.stackedWidget)
        
    def on_lineEditFilter_textChanged(self, text):
        self.proxyModelProperties.setFilterRegExp(QtCore.QRegExp(text, QtCore.Qt.CaseInsensitive))
    
    def on_treeViewSetting_pressed(self, index):
        treeNode = self.proxyModelProperties.node(index)
        self.setCurrentSettingWidget(treeNode)
        
    def on_treeViewSetting_activated(self, index):
        treeNode = self.proxyModelProperties.node(index)
        self.setCurrentSettingWidget(treeNode)
    
    def setCurrentSettingWidget(self, widget):
        self.stackedWidget.setCurrentWidget(widget)
        self.updateTitle(widget.windowTitle())
    
    def updateTitle(self, subTitle):
        self.setWindowTitle("%s - %s" % (self.baseWindowTitle, subTitle))
    
    def register(self, widget):
        index = self.stackedWidget.addWidget(widget)
        self.model.addSetting(widget)
    
    def loadSettings(self):
        for index in xrange(self.stackedWidget.count()):
            self.stackedWidget.widget(index).loadSettings()