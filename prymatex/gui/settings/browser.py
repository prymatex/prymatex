#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from PyQt4.QtNetwork import QNetworkProxy

from prymatex.ui.settings.network import Ui_Network
from prymatex.gui.settings.models import PMXSettingTreeNode

class PMXNetworkWidget(QtGui.QWidget, PMXSettingTreeNode, Ui_Network):
    '''Setup network connection
    '''
    
    def __init__(self, settingGroup, parent = None):
        QtGui.QWidget.__init__(self, parent)
        PMXSettingTreeNode.__init__(self, "network", settingGroup)
        self.setupUi(self)

        self.radioAutomatically.setToolTip("Not implemented yet")
        self.radioAutomatically.setEnabled(False)
        for radio in (
                      self.radioAutomatically,
                      self.radioBasedOnVariables,
                      self.radioDirect,
                      self.radioManual,
                      self.radioPAC,
                      ):
            radio.toggled.connect(self.changeProxyMode)
        
        self.mapping = {
                        self.radioAutomatically: 'automatic',
                        self.radioBasedOnVariables: 'enviroment',
                        self.radioDirect: 'direct',
                        self.radioManual: 'manual',
                        self.radioPAC: 'pac',                
        }
        
        self.comboProxyType.addItem("HTTP Proxy", QNetworkProxy.HttpProxy)
        self.comboProxyType.addItem("Socks 5 Proxy", QNetworkProxy.Socks5Proxy)
    
    def changeProxyMode(self, checked):
        if checked:
            self.proxyType = self.mapping[self.sender()]

    def proxyType(self, value):
        if   value == 'direct':
            if not self.radioDirect.isChecked():
                self.radioDirect.setChecked(True)
            proxy = QNetworkProxy(QNetworkProxy.NoProxy)
            QNetworkProxy.setApplicationProxy(proxy)
        elif value == 'pac':
            if not self.radioPAC.isChecked():
                self.radioPAC.setChecked(True)
        elif value == 'manual':
            if not self.radioManual.isChecked():
                self.radioManual.setChecked(True)
        elif value == 'enviroment':
            if not self.radioBasedOnVariables.isChecked():
                self.radioBasedOnVariables.setChecked(True)
        elif value == 'automatic':
            if not self.radioAutomatically.isChecked():
                self.radioAutomatically.setChecked(True)
        else:
            raise ValueError("%s is not a valid proxyType value" % value)
        
    def proxyManual(self, value):
        url = QtCore.QUrl(value)
        self.lineProxyAddress.setText(url.host())
        self.spinProxyPort.setValue(int(url.port()))
        self._proxyManual = url
    
    def proxyEnviromentVariable(self, value):
        self._proxyEnviromentVariable = value
