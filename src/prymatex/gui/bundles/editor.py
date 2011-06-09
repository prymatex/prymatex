#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex.core.base import PMXObject
from prymatex.gui.bundles.ui_editor import Ui_bundleEditor
from prymatex.gui.bundles.models import PMXBundleTreeModel
from prymatex.gui.bundles.widgets import PMXSnippetWidget, PMXCommandWidget, PMXDragCommandWidget
from prymatex.gui.bundles.widgets import PMXBundleWidget,PMXTemplateFileWidget, PMXTemplateWidget
from prymatex.gui.bundles.widgets import PMXPreferenceWidget, PMXLanguageWidget, PMXEditorBaseWidget

class PMXBundleEditor(Ui_bundleEditor, QtGui.QWidget, PMXObject):
    '''
        Prymatex Bundle Editor
    '''
    def __init__(self, parent = None):
        super(PMXBundleEditor, self).__init__(parent)
        self.setupUi(self)
        self.configEditorWidgets()
        self.configSelectTop()
        self.configTreeView()
        self.configActivation()

    def on_comboBoxItemFilter_changed(self, index):
        value = self.comboBoxItemFilter.itemData(index).toString()
        self.proxyTreeModel.setFilterRegExp(value)
        
    def configSelectTop(self):
        self.comboBoxItemFilter.addItem("Show all", QtCore.QVariant(""))
        self.comboBoxItemFilter.addItem("Syntaxs", QtCore.QVariant("syntax"))
        self.comboBoxItemFilter.addItem("Snippets", QtCore.QVariant("snippet"))
        self.comboBoxItemFilter.addItem("Macros", QtCore.QVariant("macro"))
        self.comboBoxItemFilter.addItem("Commands", QtCore.QVariant("command"))
        self.comboBoxItemFilter.addItem("DragCommands", QtCore.QVariant("dragcommand"))
        self.comboBoxItemFilter.addItem("Preferences", QtCore.QVariant("preference"))
        self.comboBoxItemFilter.addItem("Templates", QtCore.QVariant("template*"))
        self.comboBoxItemFilter.currentIndexChanged[int].connect(self.on_comboBoxItemFilter_changed)
        
    def configTreeView(self, manager = None):
        self.proxyTreeModel = self.pmxApp.supportManager.bundleProxyTreeModel
        self.treeView.setModel(self.proxyTreeModel)
        self.treeView.setHeaderHidden(True)
        self.treeView.setAnimated(True)
        self.treeView.activated.connect(self.treeViewItemActivated)
        
    def configEditorWidgets(self):
        self.stackLayout = QtGui.QStackedLayout()
        self.editorsLayout.insertLayout(1, self.stackLayout)
        self.indexes = {}
        self.editors = [ PMXSnippetWidget(self),
                         PMXCommandWidget(self),
                         PMXDragCommandWidget(self),
                         PMXBundleWidget(self),
                         PMXTemplateFileWidget(self),
                         PMXTemplateWidget(self),
                         PMXPreferenceWidget(self),
                         PMXLanguageWidget(self),
                         PMXEditorBaseWidget(self) ]
        for editor in self.editors:
            self.indexes[editor.TYPE] = self.stackLayout.addWidget(editor)
        self.noneWidgetIndex = len(self.editors) - 1
        self.stackLayout.currentChanged.connect(self.on_currentEditorWidget_changed)
        self.stackLayout.setCurrentIndex(self.noneWidgetIndex)
    
    #===========================================================
    # Activation
    #===========================================================
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and obj == self.lineKeyEquivalentActivation:
            keyseq = QtGui.QKeySequence(int(event.modifiers()) + event.key())
            self.lineKeyEquivalentActivation.setText(keyseq.toString())
            return True
        elif event.type() == QtCore.QEvent.KeyRelease and obj == self.lineKeyEquivalentActivation:
            keyseq = QtGui.QKeySequence(int(event.modifiers()) + event.key())
            print "listo"
            return True
        return super(PMXBundleEditor, self).eventFilter(obj, event)

        
    def on_comboBoxActivation_changed(self, index):
        self.lineKeyEquivalentActivation.setVisible(index == 0)
        self.lineTabTriggerActivation.setVisible(index == 1)
        
    def configActivation(self):
        self.comboBoxActivation.addItem("Key Equivalent")
        self.comboBoxActivation.addItem("Tab Trigger")
        self.comboBoxActivation.currentIndexChanged[int].connect(self.on_comboBoxActivation_changed)
        self.lineKeyEquivalentActivation.installEventFilter(self)
    
    def on_currentEditorWidget_changed(self, index):
        widget = self.stackLayout.currentWidget()
        self.labelTitle.setText(widget.title)
        scope = widget.scope
        tabTrigger = widget.tabTrigger
        keyEquivalent = widget.keyEquivalent
        self.lineEditScope.setEnabled(scope is not None)
        self.lineKeyEquivalentActivation.setEnabled(keyEquivalent is not None)
        self.lineTabTriggerActivation.setEnabled(tabTrigger is not None)
        self.comboBoxActivation.setEnabled(tabTrigger is not None or keyEquivalent is not None)
        if scope is not None:
            self.lineEditScope.setText(scope)
        else:
            self.lineEditScope.clear()
        if not keyEquivalent and not tabTrigger:
            self.lineKeyEquivalentActivation.clear()
            self.lineTabTriggerActivation.clear()
            self.comboBoxActivation.setCurrentIndex(0)
            self.lineTabTriggerActivation.setVisible(False)
        else:
            if keyEquivalent is not None:
                self.lineKeyEquivalentActivation.setText(QtGui.QKeySequence(keyEquivalent).toString())
            if tabTrigger is not None:
                self.lineTabTriggerActivation.setText(tabTrigger)
            index = 0 if keyEquivalent else 1
            self.comboBoxActivation.setCurrentIndex(index)
        
    def treeViewItemActivated(self, index):
        treeItem = self.proxyTreeModel.mapToSource(index).internalPointer()
        if treeItem.TYPE in self.indexes: 
            index = self.indexes[treeItem.TYPE]
            editor = self.editors[index]
            editor.edit(treeItem)
            
            #TODO: ver si tengo que guardar el current editor
            self.stackLayout.setCurrentIndex(index)
