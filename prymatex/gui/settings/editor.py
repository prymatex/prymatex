#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from prymatex import resources
from prymatex.ui.configure.editor import Ui_EditorWidget
from prymatex.models.settings import SettingsTreeNode
from prymatex.gui.codeeditor.editor import CodeEditor
    
class PMXEditorWidget(QtGui.QWidget, SettingsTreeNode, Ui_EditorWidget):
    TITLE = "Editor"
    ICON = resources.getIcon("accessories-text-editor")
    
    def __init__(self, settingGroup, parent = None):
        QtGui.QWidget.__init__(self, parent)
        SettingsTreeNode.__init__(self, "editor", settingGroup)
        self.setupUi(self)
        self.checkBoxLineNumbers.toggled.connect(self.on_gutterOption_toggled)
        self.checkBoxFolding.toggled.connect(self.on_gutterOption_toggled)
        self.checkBoxBookmarks.toggled.connect(self.on_gutterOption_toggled)

    def loadSettings(self):
        flags = int(self.settingGroup.value('defaultFlags'))
        self.checkBoxFolding.setChecked(flags & CodeEditor.ShowFolding)
        self.checkBoxBookmarks.setChecked(flags & CodeEditor.ShowBookmarks)
        self.checkBoxLineNumbers.setChecked(flags & CodeEditor.ShowLineNumbers)
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
            flags |= CodeEditor.ShowFolding
        if self.checkBoxBookmarks.isChecked():
            flags |= CodeEditor.ShowBookmarks
        if self.checkBoxLineNumbers.isChecked():
            flags |= CodeEditor.ShowLineNumbers
        self.settingGroup.setValue('defaultFlags', flags)
        
    @QtCore.pyqtSlot(int)
    def on_comboBoxDefaultSyntax_activated(self, index):
        model = self.comboBoxDefaultSyntax.model()
        node = model.mapToSource(model.createIndex(index, 0))
        self.settingGroup.setValue('defaultSyntax', str(node.internalPointer().uuid).upper())
    