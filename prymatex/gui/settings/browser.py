#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from PyQt4.QtNetwork import QNetworkProxy

from prymatex.ui.configure.browser import Ui_BrowserWidget
from prymatex.gui.settings.models import PMXSettingTreeNode

class PMXNetworkWidget(QtGui.QWidget, PMXSettingTreeNode, Ui_BrowserWidget):
    """Setup browser
    """
    TITLE = "Browser"
    def __init__(self, settingGroup, parent = None):
        QtGui.QWidget.__init__(self, parent)
        PMXSettingTreeNode.__init__(self, "browser", settingGroup)
        self.setupUi(self)
    
    def filterString(self):
        return "proxyportnetwork" + PMXSettingTreeNode.filterString(self)
    
    def proxyManual(self, value):
        url = QtCore.QUrl(value)
        self.lineProxyAddress.setText(url.host())
        self.spinProxyPort.setValue(int(url.port()))
        self._proxyManual = url
    
    def proxyEnviromentVariable(self, value):
        self._proxyEnviromentVariable = value
