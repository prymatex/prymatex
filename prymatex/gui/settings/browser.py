#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.qt.QtNetwork import QNetworkProxy

from prymatex.ui.configure.browser import Ui_Browser
from prymatex.models.settings import SettingsTreeNode
from prymatex.gui.dockers.browser import BrowserDock

class NetworkSettingsWidget(SettingsTreeNode, Ui_Browser, QtWidgets.QWidget):
    def __init__(self, component_class, **kwargs):
        super(NetworkSettingsWidget, self).__init__(component_class, nodeName="network", **kwargs)
        self.setupUi(self)

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
	self.setTitle("Network")
        self.setIcon(self.application().resources().get_icon("settings-network"))

        # Flags
        flags = int(self.settings.get('defaultWebSettings'))
        for check, flag in self.checks:
            check.setChecked(bool(flags & flag))

        self.lineEditHomePage.setText(self.settings.get('homePage'))
        self.lineEditProxyAddress.setText(self.settings.get('proxyAddress'))

        proxyType = self.settings.get('proxyType')
        for radio in self.radios:
            radio[0].setChecked(proxyType == radio[1])
        self.lineEditProxyAddress.setEnabled(proxyType == BrowserDock.ManualProxy)

    def on_lineEditHomePage_textEdited(self, text):
        self.settings.set("homePage", text)

    def on_lineEditProxyAddress_textEdited(self, text):
        self.settings.set("proxyAddress", text)

    @QtCore.Slot(bool)
    def on_radioButtonNoProxy_clicked(self, checked):
        self.settings.set('proxyType', BrowserDock.NoProxy)

    @QtCore.Slot(bool)
    def on_radioButtonSystemProxy_clicked(self, checked):
        if checked:
            self.settings.set('proxyType', BrowserDock.SystemProxy)

    @QtCore.Slot(bool)
    def on_radioButtonSystemProxy_clicked(self, checked):
        if checked:
            self.settings.set('proxyType', BrowserDock.SystemProxy)

    @QtCore.Slot(bool)
    def on_radioButtonManualProxy_clicked(self, checked):
        self.lineEditProxyAddress.setEnabled(checked)
        if checked:
            self.settings.set('proxyType', BrowserDock.ManualProxy)

    @QtCore.Slot(bool)
    def on_browserWebSettings_clicked(self, checked):
        flags = 0
        for check, flag in self.checks:
            if check.isChecked():
                flags |= flag
        self.settings.set('defaultWebSettings', flags)
