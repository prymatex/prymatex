#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from prymatex.ui.configure.editor import Ui_EditorWidget
from prymatex.gui.settings.models import PMXSettingTreeNode

class PMXEditorWidget(QtGui.QWidget, PMXSettingTreeNode, Ui_EditorWidget):
    TITLE = "Editor"
    def __init__(self, settingGroup, parent = None):
        QtGui.QWidget.__init__(self, parent)
        PMXSettingTreeNode.__init__(self, "editor", settingGroup)
        self.setupUi(self)
    
    def loadSettings(self):
        print self.settingGroup.value('defaultFlags')
        print self.settingGroup.value('defaultSyntax')
