#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex.ui.configure.filemanager import Ui_FileManager
from prymatex.models.settings import SettingsTreeNode

class FileManagerSettingsWidget(QtGui.QWidget, SettingsTreeNode, Ui_FileManager):
    NAMESPACE = "general"
    TITLE = "Files"
    def __init__(self, settingGroup, parent = None):
        QtGui.QWidget.__init__(self, parent)
        SettingsTreeNode.__init__(self, "files", settingGroup)
        self.setupUi(self)
        #self.loadEncodings()
        #self.setupLineEndings()

    def setupLineEndings(self):
        """Populate line endings
        """
        self.comboBoxEndOfLine.addItem(r"Unix (\n)", "unix")
    
    @QtCore.pyqtSlot(int)
    def on_comboBoxLineEnding_activated(self, index):
        data = self.comboBoxLineEnding.itemData(index)
        self.settingGroup.setValue('lineEnding', data)

    @QtCore.pyqtSlot(int)
    def on_comboBoxEncoding_activated(self, index):
        data = self.comboBoxEncoding.itemData(index)
        self.settingGroup.setValue('encoding', data)
        
    def loadEncodings(self):
        """
        Populate ComboBox from constants
        """
        
        for codec_line in TM_CODECS.split('\n'):
            if not codec_line:
                continue
            userData, titleInformation = codec_line.split('    ', 1)
            title_data = titleInformation.split('   ')
            if len(title_data) > 1:
                title = "%s (%s)" % (title_data[-1].strip().title(), title_data[0])
            else:
                title = "%s (%s)" % (title_data, userData)
            self.comboBoxEncoding.addItem(title.strip().title(), userData.replace('_', '-'))
