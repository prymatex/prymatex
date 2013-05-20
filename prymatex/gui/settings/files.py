#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore
from prymatex import resources

from prymatex.utils.text import EOLS
from prymatex.utils.encoding import CODECS

from prymatex.ui.configure.files import Ui_Files
from prymatex.models.settings import SettingsTreeNode

class FilesSettingsWidget(QtGui.QWidget, SettingsTreeNode, Ui_Files):
    NAMESPACE = "general"
    TITLE = "Files"
    ICON = resources.getIcon("drive-harddisk")


    def __init__(self, settingGroup, profile = None, parent = None):
        QtGui.QWidget.__init__(self, parent)
        SettingsTreeNode.__init__(self, "files", settingGroup, profile)
        self.setupUi(self)
        self.loadEncodings()
        self.setupLineEndings()


    def loadSettings(self):
        print(self.settingGroup.value('defaultEncoding'))


    def setupLineEndings(self):
        """Populate line endings"""
        for _, os_name, description in EOLS:
            self.comboBoxEndOfLine.addItem(description, os_name)


    @QtCore.Slot(int)
    def on_comboBoxLineEnding_activated(self, index):
        data = self.comboBoxLineEnding.itemData(index)
        self.settingGroup.setValue('defaultEndOfLine', data)


    @QtCore.Slot(int)
    def on_comboBoxEncoding_activated(self, index):
        data = self.comboBoxEncoding.itemData(index)
        self.settingGroup.setValue('defaultEncoding', data)


    def loadEncodings(self):
        """Populate ComboBoxEncoding"""
        for codec, aliases, language in CODECS:
            self.comboBoxEncoding.addItem("%s (%s)" % (language.split(",")[0].title(), codec), codec)
