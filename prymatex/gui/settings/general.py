#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from prymatex import resources
from prymatex.ui.configure.general import Ui_GeneralWidget
from prymatex.gui.settings.models import PMXSettingTreeNode

class PMXGeneralWidget(QtGui.QWidget, PMXSettingTreeNode, Ui_GeneralWidget):
    TITLE = "General"
    ICON = resources.getIcon("gearconfigure")
    
    def __init__(self, settingGroup, parent = None):
        QtGui.QWidget.__init__(self, parent)
        PMXSettingTreeNode.__init__(self, "general", settingGroup)
        self.setupUi(self)

        #self.comboTabVisibility.addItem("Always shown", PMXTabWidget.TABBAR_ALWAYS_SHOWN)
        #self.comboTabVisibility.addItem("Show when more than one", PMXTabWidget.TABBAR_WHEN_MULTIPLE)
        #self.comboTabVisibility.addItem("Never show", PMXTabWidget.TABBAR_NEVER_SHOWN)

    @QtCore.pyqtSlot(int)
    def on_comboTabVisibility_currentIndexChanged(self, index):
        value = self.comboTabVisibility.itemData(index)
        self.settingGroup.setValue('showTabBar', value)
    
    def appendToCombo(self, text):
        current_index = self.comboApplicationTitle.currentIndex()
        current_text = self.comboApplicationTitle.currentText()
        text = unicode(current_text or '') + unicode(text or '')
        self.comboApplicationTitle.setItemText(current_index, text)
    
    def on_pushInsertAppName_pressed(self):
        self.appendToCombo("$APPNAME")
        
    def on_pushInsertFile_pressed(self):
        self.appendToCombo("$FILENAME")
        
    def on_pushInsertProject_pressed(self):
        self.appendToCombo("$PROJECT")
    
    @QtCore.pyqtSlot(str)
    def on_comboApplicationTitle_editTextChanged(self, text):
        self.settingGroup.setValue('windowTitleTemplate', text)
