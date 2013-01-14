#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from prymatex.qt import QtGui, QtCore
from prymatex.qt.QtNetwork import QNetworkProxy

from prymatex import resources
from prymatex.ui.configure.browser import Ui_BrowserWidget
from prymatex.models.settings import SettingsTreeNode

class NetworkSettingsWidget(QtGui.QWidget, SettingsTreeNode, Ui_BrowserWidget):
    """Setup browser"""
    TITLE = "Browser"
    ICON = resources.getIcon("internet-web-browser")
    
    def __init__(self, settingGroup, parent = None):
        QtGui.QWidget.__init__(self, parent)
        SettingsTreeNode.__init__(self, "browser", settingGroup)
        self.setupUi(self)
    
    def filterString(self):
        return "proxyportnetwork" + SettingsTreeNode.filterString(self)
    
    def on_lineEditProxy_textEdited(self, text):
        self.settingGroup.setValue("proxy", text)
        
    def on_radioButtonNoProxy_toggled(self, checked):
        print "radioButtonNoProxy", checked
    
    def on_radioButtonSystemProxy_toggled(self, checked):
        print os.environ.get('http_proxy', '')
        print "radioButtonSystemProxy", checked
        
    def on_radioButtonManualProxy_toggled(self, checked):
        self.lineEditProxy.setEnabled(checked)
        self.settingGroup.setValue("proxy", "")
        self.lineEditProxy.clear()
