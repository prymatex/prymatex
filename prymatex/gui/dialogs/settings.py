#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex.ui.dialogs.treewidget import Ui_TreeWidgetDialog
from prymatex.gui.settings.models import PMXNamespacedModel, PMXSettingsProxyModel

class PMXSettingsDialog(QtGui.QDialog, Ui_TreeWidgetDialog):
    """Settings dialog, it's hold by the application under configdialog property
    """
    def __init__(self, application):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.application = application
        
        self.baseWindowTitle = self.windowTitle()
        
        self.model = PMXNamespacedModel(self)
        
        self.proxyModelSettings = PMXSettingsProxyModel(self)
        self.proxyModelSettings.setSourceModel(self.model)
        
        self.treeView.setModel(self.proxyModelSettings)
        
        self.stackedWidget = QtGui.QStackedWidget(self.splitter)
        #self.stackedWidget.setFrameShape(QtGui.QFrame.StyledPanel)
        #self.stackedWidget.setFrameShadow(QtGui.QFrame.Sunken)
        
        self.widgetsLayout.addWidget(self.stackedWidget)
        
    def on_lineEditFilter_textChanged(self, text):
        self.proxyModelSettings.setFilterRegExp(QtCore.QRegExp(text, QtCore.Qt.CaseInsensitive))
    
    def on_treeView_pressed(self, index):
        treeNode = self.proxyModelSettings.node(index)
        self.setCurrentSettingWidget(treeNode)
        
    def on_treeView_activated(self, index):
        treeNode = self.proxyModelSettings.node(index)
        self.setCurrentSettingWidget(treeNode)
    
    def setCurrentSettingWidget(self, widget):
        self.stackedWidget.setCurrentWidget(widget)
        self.textLabelTitle.setText(widget.titles)
        #TODO: Si no es un proxy
        self.setWindowTitle("%s - %s" % (self.baseWindowTitle, widget.title))
    
    def register(self, widget):
        index = self.stackedWidget.addWidget(widget)
        self.model.addSetting(widget)
    
    def loadSettings(self):
        for index in xrange(self.stackedWidget.count()):
            self.stackedWidget.widget(index).loadSettings()