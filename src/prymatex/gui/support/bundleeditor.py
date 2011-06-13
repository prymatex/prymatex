#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex.core.base import PMXObject
from prymatex.gui.support.ui_editor import Ui_bundleEditor
from prymatex.gui.support.widgets import PMXSnippetWidget, PMXCommandWidget, PMXDragCommandWidget
from prymatex.gui.support.widgets import PMXBundleWidget,PMXTemplateFileWidget, PMXTemplateWidget
from prymatex.gui.support.widgets import PMXPreferenceWidget, PMXLanguageWidget, PMXEditorBaseWidget

class PMXBundleEditor(Ui_bundleEditor, QtGui.QWidget, PMXObject):
    '''
        Prymatex Bundle Editor
    '''
    def __init__(self, parent = None):
        super(PMXBundleEditor, self).__init__(parent)
        self.setupUi(self)
        self.configSelectTop()
        self.configTreeView()
        self.configToolbar()
        self.configEditorWidgets()
        self.configActivation()

    def on_comboBoxItemFilter_changed(self, index):
        value = self.comboBoxItemFilter.itemData(index).toString()
        self.proxyTreeModel.setFilterRegExp(value)
    
    #==========================================================
    # Toolbar
    #==========================================================
    def on_actionCommand_triggered(self):
        print "Command"
    def on_actionDragCommand_triggered(self):
        print "DragCommand"
    def on_actionLanguage_triggered(self):
        print "Language"
    def on_actionSnippet_triggered(self):
        print "Snippet"
    def on_actionTemplate_triggered(self):
        print "Template"
    def on_actionTemplateFile_triggered(self):
        print "TemplateFile"
    def on_actionPreferences_triggered(self):
        print "Preferences"
    def on_actionBundle_triggered(self):
        print "Bundle"
        
    def configToolbar(self):
        self.toolbarMenu = QtGui.QMenu("Menu", self)
        action = QtGui.QAction("New Command", self)
        action.triggered.connect(self.on_actionCommand_triggered)
        self.toolbarMenu.addAction(action)
        action = QtGui.QAction("New Drag Command", self)
        action.triggered.connect(self.on_actionDragCommand_triggered)
        self.toolbarMenu.addAction(action)
        action = QtGui.QAction("New Language", self)
        action.triggered.connect(self.on_actionLanguage_triggered)
        self.toolbarMenu.addAction(action)
        action = QtGui.QAction("New Snippet", self)
        action.triggered.connect(self.on_actionSnippet_triggered)
        self.toolbarMenu.addAction(action)
        action = QtGui.QAction("New Template", self)
        action.triggered.connect(self.on_actionTemplate_triggered)
        self.toolbarMenu.addAction(action)
        self.templateFileAction = QtGui.QAction("New Template File", self)
        self.templateFileAction.triggered.connect(self.on_actionTemplateFile_triggered)
        self.templateFileAction.setDisabled(True)
        self.toolbarMenu.addAction(self.templateFileAction)
        action = QtGui.QAction("New Preferences", self)
        action.triggered.connect(self.on_actionPreferences_triggered)
        self.toolbarMenu.addAction(action)
        self.toolbarMenu.addSeparator()
        action = QtGui.QAction("New Bundle", self)
        action.triggered.connect(self.on_actionBundle_triggered)
        self.toolbarMenu.addAction(action)
        self.pushButtonAdd.setMenu(self.toolbarMenu)
        
    def configSelectTop(self):
        self.comboBoxItemFilter.addItem("Show all", QtCore.QVariant(""))
        self.comboBoxItemFilter.addItem(QtGui.QIcon(":/bundles/resources/bundles/languages.png"), "Syntaxs", QtCore.QVariant("syntax"))
        self.comboBoxItemFilter.addItem(QtGui.QIcon(":/bundles/resources/bundles/snippets.png"), "Snippets", QtCore.QVariant("snippet"))
        self.comboBoxItemFilter.addItem(QtGui.QIcon(":/bundles/resources/bundles/macros.png"), "Macros", QtCore.QVariant("macro"))
        self.comboBoxItemFilter.addItem(QtGui.QIcon(":/bundles/resources/bundles/commands.png"), "Commands", QtCore.QVariant("command"))
        self.comboBoxItemFilter.addItem(QtGui.QIcon(":/bundles/resources/bundles/drag-commands.png"), "DragCommands", QtCore.QVariant("dragcommand"))
        self.comboBoxItemFilter.addItem(QtGui.QIcon(":/bundles/resources/bundles/preferences.png"), "Preferences", QtCore.QVariant("preference"))
        self.comboBoxItemFilter.addItem(QtGui.QIcon(":/bundles/resources/bundles/templates.png"), "Templates", QtCore.QVariant("template*"))
        self.comboBoxItemFilter.currentIndexChanged[int].connect(self.on_comboBoxItemFilter_changed)
        
    def configTreeView(self, manager = None):
        self.proxyTreeModel = self.pmxApp.supportManager.bundleProxyTreeModel
        self.treeView.setModel(self.proxyTreeModel)
        self.treeView.setHeaderHidden(True)
        self.treeView.setAnimated(True)
        self.treeView.activated.connect(self.treeViewItemActivated)
        
    def configEditorWidgets(self):
        self.stackedWidget = QtGui.QStackedWidget()
        self.stackedWidget.setFrameShape(QtGui.QFrame.StyledPanel)
        self.stackedWidget.setFrameShadow(QtGui.QFrame.Sunken)
        self.editorsLayout.insertWidget(1, self.stackedWidget)
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
            self.indexes[editor.TYPE] = self.stackedWidget.addWidget(editor)
        self.beginEdit(self.editors[-1], None)
    
    #===========================================================
    # Activation
    #===========================================================
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and obj == self.lineKeyEquivalentActivation:
            keyseq = QtGui.QKeySequence(int(event.modifiers()) + event.key())
            self.lineKeyEquivalentActivation.setText(keyseq.toString())
            return True
        elif event.type() == QtCore.QEvent.KeyRelease and obj == self.lineKeyEquivalentActivation:
            keyseq = int(event.modifiers()) + event.key()
            self.stackedWidget.currentWidget().setKeyEquivalent(keyseq)
            return True
        return super(PMXBundleEditor, self).eventFilter(obj, event)
        
    def on_comboBoxActivation_changed(self, index):
        self.lineKeyEquivalentActivation.setVisible(index == 0)
        self.lineTabTriggerActivation.setVisible(index == 1)
    
    def on_lineEditScope_edited(self, text):
        self.stackedWidget.currentWidget().setScope(unicode(text))
    
    def on_lineTabTriggerActivation_edited(self, text):
        self.stackedWidget.currentWidget().setTabTrigger(unicode(text))
    
    def configActivation(self):
        self.comboBoxActivation.addItem("Key Equivalent")
        self.comboBoxActivation.addItem("Tab Trigger")
        self.comboBoxActivation.currentIndexChanged[int].connect(self.on_comboBoxActivation_changed)
        self.lineKeyEquivalentActivation.installEventFilter(self)
        #textEdited: solo cuando cambias el texto desde la gui
        self.lineTabTriggerActivation.textEdited.connect(self.on_lineTabTriggerActivation_edited)
        self.lineEditScope.textEdited.connect(self.on_lineEditScope_edited)
    
    def beginEdit(self, editor, item):
        editor.edit(item)
        self.stackedWidget.setCurrentWidget(editor)
        self.labelTitle.setText(editor.title)
        scope = editor.getScope()
        tabTrigger = editor.getTabTrigger()
        keyEquivalent = editor.getKeyEquivalent()
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
        
        #TODO: ver si tengo que guardar el current editor
        current = self.stackedWidget.currentWidget()
        if current.isChanged:
            print current.changes
            
        self.templateFileAction.setEnabled(treeItem.TYPE == "template" or treeItem.TYPE == "templatefile")
        
        if treeItem.TYPE in self.indexes:
            index = self.indexes[treeItem.TYPE]
            editor = self.editors[index]
            self.beginEdit(editor, treeItem)
