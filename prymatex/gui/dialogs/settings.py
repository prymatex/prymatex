#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex.ui.dialogs.settings import Ui_SettingsDialog
from prymatex.gui.settings.models import PMXSettingsModel, PMXSettingsProxyModel

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
        
        self.model = PMXSettingsModel(self)
        
        self.proxyModelSettings = PMXSettingsProxyModel(self)
        self.proxyModelSettings.setSourceModel(self.model)
        
        self.treeViewSetting.setModel(self.proxyModelSettings)
        
        self.stackedWidget = QtGui.QStackedWidget(self.splitter)
        self.stackedWidget.setFrameShape(QtGui.QFrame.StyledPanel)
        self.stackedWidget.setFrameShadow(QtGui.QFrame.Sunken)
        
    def on_lineEditFilter_textChanged(self, text):
        self.proxyModelSettings.setFilterRegExp(QtCore.QRegExp(text, QtCore.Qt.CaseInsensitive))
    
    def on_treeViewSetting_pressed(self, index):
        treeNode = self.proxyModelSettings.node(index)
        self.setCurrentSettingWidget(treeNode)
        
    def on_treeViewSetting_activated(self, index):
        treeNode = self.proxyModelSettings.node(index)
        self.setCurrentSettingWidget(treeNode)
    
    def setCurrentSettingWidget(self, widget):
        self.stackedWidget.setCurrentWidget(widget)
        self.updateTitle(widget.windowTitle())
    
    def updateTitle(self, subTitle):
        self.setWindowTitle("%s - %s" % (self.baseWindowTitle, subTitle))
    
    def register(self, widget):
        index = self.stackedWidget.addWidget(widget)
        self.model.appendSetting(widget)
    
    def loadDefaultSettings(self):
        pass
        #for widget in self.stackedWidget.widgets():
            #widget.loadDefaultSettings()