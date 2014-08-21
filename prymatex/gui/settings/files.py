#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex.utils import text, encoding

from prymatex.ui.configure.files import Ui_Files
from prymatex.models.settings import SettingsTreeNode

class FilesSettingsWidget(SettingsTreeNode, Ui_Files, QtGui.QWidget):
    NAMESPACE = "general"

    def __init__(self, **kwargs):
        super(FilesSettingsWidget, self).__init__(nodeName = "files", **kwargs)
        self.setupUi(self)
        self.setTitle("Files")
        self.setIcon(self.resources().get_icon("settings-files"))
        self.loadEncodings()
        self.setupLineEndings()

    def loadSettings(self):
        super(FilesSettingsWidget, self).loadSettings()

    def setupLineEndings(self):
        """Populate line endings"""
        for _, os_name, description in text.EOLS:
            self.comboBoxEndOfLine.addItem(description, os_name)

    @QtCore.Slot(int)
    def on_comboBoxLineEnding_activated(self, index):
        data = self.comboBoxLineEnding.itemData(index)
        self.settings.setValue('defaultEndOfLine', data)

    @QtCore.Slot(int)
    def on_comboBoxEncoding_activated(self, index):
        data = self.comboBoxEncoding.itemData(index)
        self.settings.setValue('defaultEncoding', data)

    def loadEncodings(self):
        """Populate ComboBoxEncoding"""
        for codec, aliases, language in encoding.CODECS:
            self.comboBoxEncoding.addItem("%s (%s)" % (language.split(",")[0].title(), codec), codec)
