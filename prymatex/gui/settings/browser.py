#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from prymatex.qt import QtGui, QtCore
from prymatex.qt.QtNetwork import QNetworkProxy

from prymatex import resources
from prymatex.ui.configure.browser import Ui_Browser
from prymatex.models.settings import SettingsTreeNode
from prymatex.gui.dockers.browser import BrowserDock

class NetworkSettingsWidget(QtGui.QWidget, SettingsTreeNode, Ui_Browser):
    """Setup browser"""
    TITLE = "Browser"
    ICON = resources.getIcon("internet-web-browser")
    
    def __init__(self, settingGroup, profile = None, parent = None):
        QtGui.QWidget.__init__(self, parent)
        SettingsTreeNode.__init__(self, "browser", settingGroup, profile)
        self.setupUi(self)
        
        self.checks = [(self.checkBoxDeveloperExtrasEnabled, BrowserDock.DeveloperExtrasEnabled),
            (self.checkBoxPluginsEnabled, BrowserDock.PluginsEnabled),
            (self.checkBoxPrivateBrowsingEnabled, BrowserDock.PrivateBrowsingEnabled),
            (self.checkBoxJavaEnabled, BrowserDock.JavaEnabled),
            (self.checkBoxAutoLoadImages, BrowserDock.AutoLoadImages),
            (self.checkBoxJavascriptEnabled, BrowserDock.JavascriptEnabled),
        ]
        
        for check, flag in self.checks:
            check.toggled.connect(self.on_browserWebSettings_toggled)
        
    def loadSettings(self):
        SettingsTreeNode.loadSettings(self)
        
        # Flags
        flags = int(self.settingGroup.value('defaultWebSettings'))
        for check, flag in self.checks:
            check.setChecked(bool(flags & flag))
        
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
        
    def on_browserWebSettings_toggled(self, checked):
        flags = 0
        for check, flag in self.checks:
            if check.isChecked():
                flags |= flag
        self.settingGroup.setValue('defaultWebSettings', flags)
