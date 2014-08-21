#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from prymatex.qt import QtGui, QtCore
from prymatex.qt.QtNetwork import QNetworkProxy

from prymatex.ui.configure.browser import Ui_Browser
from prymatex.models.settings import SettingsTreeNode
from prymatex.gui.dockers.browser import BrowserDock

class NetworkSettingsWidget(SettingsTreeNode, Ui_Browser, QtGui.QWidget):
    def __init__(self, **kwargs):
        super(NetworkSettingsWidget, self).__init__(nodeName = "network", **kwargs)
        self.setupUi(self)
        self.setTitle("Network")
        self.setIcon(self.resources().get_icon("settings-network"))

        self.checks = [(self.checkBoxDeveloperExtrasEnabled, BrowserDock.DeveloperExtrasEnabled),
            (self.checkBoxPluginsEnabled, BrowserDock.PluginsEnabled),
            (self.checkBoxPrivateBrowsingEnabled, BrowserDock.PrivateBrowsingEnabled),
            (self.checkBoxJavaEnabled, BrowserDock.JavaEnabled),
            (self.checkBoxAutoLoadImages, BrowserDock.AutoLoadImages),
            (self.checkBoxJavascriptEnabled, BrowserDock.JavascriptEnabled),
        ]

        for check, flag in self.checks:
            check.clicked.connect(self.on_browserWebSettings_clicked)

        self.radios = [(self.radioButtonNoProxy, BrowserDock.NoProxy),
            (self.radioButtonSystemProxy, BrowserDock.SystemProxy),
            (self.radioButtonManualProxy, BrowserDock.ManualProxy)
        ]

    def loadSettings(self):
        super(NetworkSettingsWidget, self).loadSettings()

        # Flags
        flags = int(self.settings.value('defaultWebSettings'))
        for check, flag in self.checks:
            check.setChecked(bool(flags & flag))

        self.lineEditHomePage.setText(self.settings.value('homePage'))
        self.lineEditProxyAddress.setText(self.settings.value('proxyAddress'))

        proxyType = self.settings.value('proxyType')
        for radio in self.radios:
            radio[0].setChecked(proxyType == radio[1])
        self.lineEditProxyAddress.setEnabled(proxyType == BrowserDock.ManualProxy)

    def on_lineEditHomePage_textEdited(self, text):
        self.settings.setValue("homePage", text)

    def on_lineEditProxyAddress_textEdited(self, text):
        self.settings.setValue("proxyAddress", text)

    def on_radioButtonNoProxy_clicked(self, checked):
        self.settings.setValue('proxyType', BrowserDock.NoProxy)

    def on_radioButtonSystemProxy_clicked(self, checked):
        if checked:
            self.settings.setValue('proxyType', BrowserDock.SystemProxy)

    def on_radioButtonSystemProxy_clicked(self, checked):
        if checked:
            self.settings.setValue('proxyType', BrowserDock.SystemProxy)

    def on_radioButtonManualProxy_clicked(self, checked):
        self.lineEditProxyAddress.setEnabled(checked)
        if checked:
            self.settings.setValue('proxyType', BrowserDock.ManualProxy)

    def on_browserWebSettings_clicked(self, checked):
        flags = 0
        for check, flag in self.checks:
            if check.isChecked():
                flags |= flag
        self.settings.setValue('defaultWebSettings', flags)
