#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from prymatex import resources
from prymatex.ui.configure.editor import Ui_EditorWidget
from prymatex.gui.settings.models import PMXSettingTreeNode
from prymatex.gui.codeeditor.editor import PMXCodeEditor
    
class PMXEditorWidget(QtGui.QWidget, PMXSettingTreeNode, Ui_EditorWidget):
    TITLE = "Editor"
    ICON = resources.getIcon("gearfile")
    
    def __init__(self, settingGroup, parent = None):
        QtGui.QWidget.__init__(self, parent)
        PMXSettingTreeNode.__init__(self, "editor", settingGroup)
        self.setupUi(self)
        self.checkBoxLineNumbers.toggled.connect(self.on_gutterOption_toggled)
        self.checkBoxFolding.toggled.connect(self.on_gutterOption_toggled)
        self.checkBoxBookmarks.toggled.connect(self.on_gutterOption_toggled)

    def loadSettings(self):
        flags = int(self.settingGroup.value('defaultFlags'))
        self.checkBoxFolding.setChecked(flags & PMXCodeEditor.ShowFolding)
        self.checkBoxBookmarks.setChecked(flags & PMXCodeEditor.ShowBookmarks)
        self.checkBoxLineNumbers.setChecked(flags & PMXCodeEditor.ShowLineNumbers)
        self.comboBoxDefaultSyntax.setModel(self.application.supportManager.syntaxProxyModel);
        self.comboBoxDefaultSyntax.setModelColumn(0)
        uuid = self.settingGroup.value('defaultSyntax')
        syntax = self.application.supportManager.getBundleItem(uuid)
        model = self.comboBoxDefaultSyntax.model()
        index = model.findItemIndex(syntax)
        self.comboBoxDefaultSyntax.setCurrentIndex(index)
        
    def on_gutterOption_toggled(self, checked):
        flags = 0
        if self.checkBoxFolding.isChecked():
            flags |= PMXCodeEditor.ShowFolding
        if self.checkBoxBookmarks.isChecked():
            flags |= PMXCodeEditor.ShowBookmarks
        if self.checkBoxLineNumbers.isChecked():
            flags |= PMXCodeEditor.ShowLineNumbers
        self.settingGroup.setValue('defaultFlags', flags)
        
    @QtCore.pyqtSlot(int)
    def on_comboBoxDefaultSyntax_activated(self, index):
        model = self.comboBoxDefaultSyntax.model()
        node = model.mapToSource(model.createIndex(index, 0))
        self.settingGroup.setValue('defaultSyntax', str(node.internalPointer().uuid).upper())
    