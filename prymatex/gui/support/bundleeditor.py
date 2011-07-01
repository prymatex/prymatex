#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex.core.base import PMXObject
from prymatex.core.config import pmxConfigPorperty
from prymatex.ui.bundleeditor import Ui_bundleEditor
from prymatex.gui.support.widgets import PMXSnippetWidget, PMXCommandWidget, PMXDragCommandWidget
from prymatex.gui.support.widgets import PMXBundleWidget,PMXTemplateFileWidget, PMXTemplateWidget
from prymatex.gui.support.widgets import PMXPreferenceWidget, PMXLanguageWidget, PMXEditorBaseWidget

class PMXBundleEditor(Ui_bundleEditor, QtGui.QWidget, PMXObject):
    #http://manual.macromates.com/en/expert_preferences.html
    #When you create a new item in the bundle editor without having selected a bundle first, then the bundle with the UUID held by this defaults key is used as the target
    defaultBundleForNewBundleItems = pmxConfigPorperty(default = u'B7BC3FFD-6E4B-11D9-91AF-000D93589AF6', tm_name = u'OakDefaultBundleForNewBundleItems')
    
    class Meta:
        settings = 'BundleEditor'
        
    def __init__(self, parent = None):
        super(PMXBundleEditor, self).__init__(parent)
        self.setupUi(self)
        self.manager = self.pmxApp.supportManager
        #Cargar los widgets editores
        self.configEditorWidgets()
        #Configurar filter, tree, toolbar y activaciones
        self.configSelectTop()
        self.configTreeView()
        self.configToolbar()
        self.configActivation()
        self.configure()

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
        self.setCurrentEditor(self.editors[-1])
        
    #==========================================================
    # Toolbar
    #==========================================================
    def getBundleForIndex(self, index):
        bundle = None
        if not index.isValid():
            bundle = self.proxyTreeModel.sourceModel().getBundle(self.defaultBundleForNewBundleItems)
        else:
            bundle = self.proxyTreeModel.mapToSource(index).internalPointer()
            while bundle.TYPE != 'bundle':
                bundle = bundle.parent
        return bundle
    
    def createBundleItem(self, itemName, itemType):
        index = self.treeView.currentIndex()
        bundle = self.getBundleForIndex(index)
        treeItem = self.manager.createBundleItem(itemName, itemType, bundle)
        index = self.proxyTreeModel.index(treeItem.row(), 0, self.proxyTreeModel.index(treeItem.bundle.row(), 0 , QtCore.QModelIndex()))
        self.treeView.setCurrentIndex(index)
        self.treeView.edit(index)
        self.editTreeItem(treeItem)
        
    def on_actionCommand_triggered(self):
        self.createBundleItem(u"untitled", "command")
        
    def on_actionDragCommand_triggered(self):
        self.createBundleItem(u"untitled", "dragcommand")
        
    def on_actionLanguage_triggered(self):
        self.createBundleItem(u"untitled", "syntax")
        
    def on_actionSnippet_triggered(self):
        self.createBundleItem(u"untitled", "snippet")
        
    def on_actionTemplate_triggered(self):
        self.createBundleItem(u"untitled", "template")
        
    def on_actionTemplateFile_triggered(self):
        index = self.treeView.currentIndex()
        if index.isValid():
            template = self.proxyTreeModel.mapToSource(index).internalPointer()
            if template.TYPE == 'templatefile':
                template = template.parent
        self.manager.createTemplateFile(u"untitled", template)
        print "TemplateFile"
        
    def on_actionPreferences_triggered(self):
        self.createBundleItem(u"untitled", "preference")

    def on_actionBundle_triggered(self):
        bundle = self.manager.createBundle("untitled")
        index = self.proxyTreeModel.index(bundle.row(), 0, QtCore.QModelIndex())
        self.treeView.setCurrentIndex(index)
        
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

    #==========================================================
    # Filter Top Bar
    #==========================================================
    def on_comboBoxItemFilter_changed(self, index):
        value = self.comboBoxItemFilter.itemData(index).toString()
        self.proxyTreeModel.setFilterRegExp(value)
    
    def configSelectTop(self):
        self.comboBoxItemFilter.addItem("Show all", QtCore.QVariant(""))
        self.comboBoxItemFilter.addItem(QtGui.QIcon(":/bundles/resources/bundles/languages.png"), "Languages", QtCore.QVariant("syntax"))
        self.comboBoxItemFilter.addItem(QtGui.QIcon(":/bundles/resources/bundles/snippets.png"), "Snippets", QtCore.QVariant("snippet"))
        self.comboBoxItemFilter.addItem(QtGui.QIcon(":/bundles/resources/bundles/macros.png"), "Macros", QtCore.QVariant("macro"))
        self.comboBoxItemFilter.addItem(QtGui.QIcon(":/bundles/resources/bundles/commands.png"), "Commands", QtCore.QVariant("command"))
        self.comboBoxItemFilter.addItem(QtGui.QIcon(":/bundles/resources/bundles/drag-commands.png"), "DragCommands", QtCore.QVariant("dragcommand"))
        self.comboBoxItemFilter.addItem(QtGui.QIcon(":/bundles/resources/bundles/preferences.png"), "Preferences", QtCore.QVariant("preference"))
        self.comboBoxItemFilter.addItem(QtGui.QIcon(":/bundles/resources/bundles/templates.png"), "Templates", QtCore.QVariant("template*"))
        self.comboBoxItemFilter.currentIndexChanged[int].connect(self.on_comboBoxItemFilter_changed)
    
    #==========================================================
    # Tree View
    #==========================================================
    def getEditorForTreeItem(self, treeItem):
        if treeItem.TYPE in self.indexes:
            index = self.indexes[treeItem.TYPE]
            return self.editors[index]

    def on_proxyTreeModel_dataChanged(self, sindex, eindex):
        current = self.stackedWidget.currentWidget()
        self.labelTitle.setText(current.title)
        
    def on_treeView_Activated(self, index):
        treeItem = self.proxyTreeModel.mapToSource(index).internalPointer()
        self.templateFileAction.setEnabled(treeItem.TYPE == "template" or treeItem.TYPE == "templatefile")
        self.editTreeItem(treeItem)
        
    def configTreeView(self, manager = None):
        self.proxyTreeModel = self.pmxApp.supportManager.bundleProxyTreeModel
        #self.proxyTreeModel.sort(0)
        self.proxyTreeModel.dataChanged.connect(self.on_proxyTreeModel_dataChanged)
        self.treeView.setModel(self.proxyTreeModel)
        self.treeView.setHeaderHidden(True)
        self.treeView.setAnimated(True)
        self.treeView.activated.connect(self.on_treeView_Activated)
        self.treeView.pressed.connect(self.on_treeView_Activated)
        
    #===========================================================
    # Activation
    #===========================================================
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and obj == self.lineKeyEquivalentActivation:
            keyseq = int(event.modifiers()) + event.key()
            print "press", keyseq
            self.stackedWidget.currentWidget().setKeyEquivalent(keyseq)
            self.lineKeyEquivalentActivation.setText(QtGui.QKeySequence(keyseq).toString())
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
    
    def editTreeItem(self, treeItem):
        #TODO: ver si tengo que guardar el current editor
        current = self.stackedWidget.currentWidget()
        if current.isChanged:
            if current.TYPE != "":
                if current.TYPE == "bundle":
                    self.manager.updateBundle(current.bundleItem, **current.changes)
                else:
                    self.manager.updateBundleItem(current.bundleItem, **current.changes)
            
        editor = self.getEditorForTreeItem(treeItem)
        if editor != None:
            editor.edit(treeItem)
            self.setCurrentEditor(editor)
            
    def setCurrentEditor(self, editor):
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
