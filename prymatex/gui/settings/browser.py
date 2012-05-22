#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from PyQt4 import QtGui, QtCore
from PyQt4.QtNetwork import QNetworkProxy

from prymatex import resources
from prymatex.ui.configure.browser import Ui_BrowserWidget
from prymatex.gui.settings.models import PMXSettingTreeNode

class PMXNetworkWidget(QtGui.QWidget, PMXSettingTreeNode, Ui_BrowserWidget):
    """Setup browser"""
    TITLE = "Browser"
    ICON = resources.getIcon("browser")
    
    def __init__(self, settingGroup, parent = None):
        QtGui.QWidget.__init__(self, parent)
        PMXSettingTreeNode.__init__(self, "browser", settingGroup)
        self.setupUi(self)
    
    def filterString(self):
        return "proxyportnetwork" + PMXSettingTreeNode.filterString(self)
    
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
