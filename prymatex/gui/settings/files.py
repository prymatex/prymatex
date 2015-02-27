#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets

from prymatex.utils import text, encoding

from prymatex.ui.configure.files import Ui_Files
from prymatex.models.settings import SettingsTreeNode

class FilesSettingsWidget(SettingsTreeNode, Ui_Files, QtWidgets.QWidget):
    NAMESPACE = "general"

    def __init__(self, component_class, **kwargs):
        super(FilesSettingsWidget, self).__init__(component_class, nodeName="files", **kwargs)
        self.setupUi(self)
        self.loadEncodings()
        self.setupLineEndings()

    def loadSettings(self):
        super(FilesSettingsWidget, self).loadSettings()
        self.setTitle("Files")
        self.setIcon(self.application().resources().get_icon("settings-files"))

    def setupLineEndings(self):
        """Populate line endings"""
        for _, os_name, description in text.EOLS:
            self.comboBoxEndOfLine.addItem(description, os_name)

    @QtCore.Slot(int)
    def on_comboBoxLineEnding_activated(self, index):
        data = self.comboBoxLineEnding.itemData(index)
        self.settings.set('defaultEndOfLine', data)

    @QtCore.Slot(int)
    def on_comboBoxEncoding_activated(self, index):
        data = self.comboBoxEncoding.itemData(index)
        self.settings.set('defaultEncoding', data)

    def loadEncodings(self):
        """Populate ComboBoxEncoding"""
        for codec, aliases, language in encoding.CODECS:
            self.comboBoxEncoding.addItem("%s (%s)" % (language.split(",")[0].title(), codec), codec)
