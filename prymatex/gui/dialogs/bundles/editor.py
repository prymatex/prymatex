#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from prymatex import resources
from prymatex.ui.support.editor import Ui_BundleEditor
from prymatex.gui.support import widgets
from prymatex.gui.dialogs.bundles.filter import BundleFilterDialog

class BundleEditorDialog(QtGui.QDialog, Ui_BundleEditor):
    BASE_EDITOR = -1 #El ultimo es el editor base, no tiene nada
    
    def __init__(self, application, manager):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.namespace = None
        self.application = application
        self.manager = manager
        self.proxyTreeModel = self.manager.bundleProxyTreeModel
        
        self.finished.connect(self.on_bundleEditor_finished)
        
        #Cargar los widgets editores
        self.configEditorWidgets()
        
        #Configurar filter, tree, toolbar y activaciones
        self.configSelectTop()
        self.configTreeView()
        self.configToolbar()
        self.configActivation()

    def on_bundleEditor_finished(self, code):
        self.saveChanges()


    # ---------------- custom execs
    def exec_(self):
        #Limiar el editor
        self.setCurrentEditor(self.editors[-1])
        #Quitar seleccion
        firstIndex = self.proxyTreeModel.index(0, 0)
        self.treeView.setSelection(self.treeView.visualRect(firstIndex), QtGui.QItemSelectionModel.Clear)
        
        return QtGui.QDialog.exec_(self)


    def execEditor(self, typeFilter = None, namespaceFilter = None, title = "Bundle Editor"):
        # Title
        self.setWindowTitle(title)
        
        # Set namespace and filters
        self.namespace = namespaceFilter
        self.proxyTreeModel.setFilterNamespace(namespaceFilter)
        self.proxyTreeModel.setFilterBundleItemType(typeFilter)
        index = self.comboBoxItemFilter.findData(typeFilter)
        self.comboBoxItemFilter.setCurrentIndex(index)
        
        # Go!
        self.exec_()


    def execCommand(self):
        return self.execEditor("command")


    def execLanguage(self):
        return self.execEditor("syntax")


    def execSnippet(self):
        return self.execEditor("snippet")


    def configEditorWidgets(self):
        self.stackedWidget = QtGui.QStackedWidget()
        self.stackedWidget.setFrameShape(QtGui.QFrame.StyledPanel)
        self.stackedWidget.setFrameShadow(QtGui.QFrame.Sunken)
        self.editorsLayout.insertWidget(1, self.stackedWidget)
        self.indexes = {}
        self.editors = [ widgets.SnippetEditorWidget(self),
                         widgets.CommandEditorWidget(self),
                         widgets.DragCommandEditorWidget(self),
                         widgets.BundleEditorWidget(self),
                         widgets.TemplateEditorFileWidget(self),
                         widgets.TemplateEditorWidget(self),
                         widgets.PreferenceEditorWidget(self),
                         widgets.LanguageEditorWidget(self),
                         widgets.MacroEditorWidget(self),
                         widgets.ProjectEditorWidget(self),
                         widgets.NoneEditorWidget(self) ]
        for editor in self.editors:
            self.indexes[editor.TYPE] = self.stackedWidget.addWidget(editor)


    # ----------------- Toolbar create and delete bundle items
    def getBundleForIndex(self, index):
        if not index.isValid():
            return self.manager.getDefaultBundle()
        bundle = self.proxyTreeModel.node(index)
        while bundle.TYPE != 'bundle':
            bundle = bundle.parentNode()
        return bundle
    
    def createBundleItem(self, itemName, itemType):
        index = self.treeView.currentIndex()
        bundle = self.getBundleForIndex(index)
        bundleItemNode = self.manager.createBundleItem(itemName, itemType, bundle, self.namespace)
        sIndex = self.manager.bundleTreeModel.createIndex(bundleItemNode.row(), 0, bundleItemNode)
        index = self.proxyTreeModel.mapFromSource(sIndex)
        self.treeView.setCurrentIndex(index)
        self.editTreeItem(bundleItemNode)
        self.treeView.edit(index)
        
    @QtCore.pyqtSlot()
    def on_actionCommand_triggered(self):
        self.createBundleItem(u"untitled", "command")

    @QtCore.pyqtSlot()        
    def on_actionDragCommand_triggered(self):
        self.createBundleItem(u"untitled", "dragcommand")

    @QtCore.pyqtSlot()        
    def on_actionLanguage_triggered(self):
        self.createBundleItem(u"untitled", "syntax")

    @QtCore.pyqtSlot()        
    def on_actionSnippet_triggered(self):
        self.createBundleItem(u"untitled", "snippet")

    @QtCore.pyqtSlot()        
    def on_actionTemplate_triggered(self):
        self.createBundleItem(u"untitled", "template")

    @QtCore.pyqtSlot()        
    def on_actionProject_triggered(self):
        self.createBundleItem(u"untitled", "project")

    @QtCore.pyqtSlot()        
    def on_actionTemplateFile_triggered(self):
        index = self.treeView.currentIndex()
        if index.isValid():
            template = self.proxyTreeModel.node(index)
            if template.TYPE == 'templatefile':
                template = template.parentNode()
        self.manager.createTemplateFile(u"untitled", template, self.namespace)

    @QtCore.pyqtSlot()
    def on_actionPreferences_triggered(self):
        self.createBundleItem(u"untitled", "preference")

    @QtCore.pyqtSlot()
    def on_actionBundle_triggered(self):
        bundleNode = self.manager.createBundle("untitled", self.namespace)
        sIndex = self.manager.bundleTreeModel.createIndex(bundleNode.row(), 0, bundleNode)
        index = self.proxyTreeModel.mapFromSource(sIndex)
        self.treeView.setCurrentIndex(index)
        self.editTreeItem(bundleNode)
        self.treeView.edit(index)

    @QtCore.pyqtSlot()
    def on_pushButtonRemove_pressed(self):
        index = self.treeView.currentIndex()
        if index.isValid():
            item = self.proxyTreeModel.node(index)
            if item.TYPE == 'bundle':
                self.manager.deleteBundle(item)
            elif item.TYPE == 'templatefile':
                self.manager.deleteTemplateFile(item)
            else:
                self.manager.deleteBundleItem(item)

    @QtCore.pyqtSlot()
    def on_pushButtonFilter_pressed(self):
        self.bundleFilterDialog.show()

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
        action = QtGui.QAction("New Project", self)
        action.triggered.connect(self.on_actionProject_triggered)
        self.toolbarMenu.addAction(action)
        self.templateFileAction = QtGui.QAction("New Template File", self)
        self.templateFileAction.triggered.connect(self.on_actionTemplateFile_triggered)
        self.toolbarMenu.addAction(self.templateFileAction)
        action = QtGui.QAction("New Preferences", self)
        action.triggered.connect(self.on_actionPreferences_triggered)
        self.toolbarMenu.addAction(action)
        self.toolbarMenu.addSeparator()
        action = QtGui.QAction("New Bundle", self)
        action.triggered.connect(self.on_actionBundle_triggered)
        self.toolbarMenu.addAction(action)
        
        def conditionalEnabledTemplateFile():
            node = self.proxyTreeModel.node(self.treeView.currentIndex())
            self.templateFileAction.setEnabled(not node.isRootNode() and (node.TYPE in ["template", "templatefile", "project"]))
        self.toolbarMenu.aboutToShow.connect(conditionalEnabledTemplateFile)
        
        self.pushButtonAdd.setMenu(self.toolbarMenu)
        
        #Bundle global filter dialog
        self.bundleFilterDialog = BundleFilterDialog(self)
        self.bundleFilterDialog.setModel(self.manager.bundleProxyModel)


    # ------------------- Filter bundle items
    def on_comboBoxItemFilter_returnPressed(self):
        self.proxyTreeModel.setFilterBundleItemType(None)
        self.proxyTreeModel.setFilterRegExp(".*%s.*" % self.comboBoxItemFilter.currentText())


    @QtCore.pyqtSlot(int)
    def on_comboBoxItemFilter_activated(self, index):
        value = self.comboBoxItemFilter.itemData(index)
        self.proxyTreeModel.setFilterBundleItemType(value)


    def configSelectTop(self):
        self.comboBoxItemFilter.addItem("Show all")
        self.comboBoxItemFilter.addItem(resources.getIcon("bundle-item-syntax"), "Languages", "syntax")
        self.comboBoxItemFilter.addItem(resources.getIcon("bundle-item-snippet"), "Snippets", "snippet")
        self.comboBoxItemFilter.addItem(resources.getIcon("bundle-item-macro"), "Macros", "macro")
        self.comboBoxItemFilter.addItem(resources.getIcon("bundle-item-command"), "Commands", "command")
        self.comboBoxItemFilter.addItem(resources.getIcon("bundle-item-dragcommand"), "DragCommands", "dragcommand")
        self.comboBoxItemFilter.addItem(resources.getIcon("bundle-item-preference"), "Preferences", "preference")
        self.comboBoxItemFilter.addItem(resources.getIcon("bundle-item-template"), "Templates", "template templatefile")
        self.comboBoxItemFilter.addItem(resources.getIcon("bundle-item-project"), "Projects", "project templatefile")
        self.comboBoxItemFilter.setInsertPolicy(QtGui.QComboBox.NoInsert)
        self.comboBoxItemFilter.lineEdit().returnPressed.connect(self.on_comboBoxItemFilter_returnPressed)
        

    # --------------------------- Tree View display the bundle items model
    def getEditorBase(self):
        return self.editors[self.BASE_EDITOR]


    def getEditorForTreeItem(self, treeItem):
        if not treeItem.isRootNode() and treeItem.TYPE in self.indexes:
            index = self.indexes[treeItem.TYPE]
            return self.editors[index]


    def on_bundleTreeModel_rowsInserted(self, parent, start, end):
        sIndex = self.manager.bundleTreeModel.index(start, 0, parent)
        index = self.proxyTreeModel.mapFromSource(sIndex)
        node = self.proxyTreeModel.node(index)
        self.treeView.setCurrentIndex(index)
        self.editTreeItem(node)
        self.treeView.edit(index)


    def on_proxyTreeModel_dataChanged(self, sindex, eindex):
        current = self.stackedWidget.currentWidget()
        self.labelTitle.setText(current.title)

        
    def on_treeView_selectionChanged(self, selected, deselected):
        indexes = selected.indexes()
        if indexes:
            treeItem = self.proxyTreeModel.node(indexes[0])
            self.editTreeItem(treeItem)
        else:
            self.editTreeItem(None)

            
    def configTreeView(self, manager = None):
        self.proxyTreeModel.dataChanged.connect(self.on_proxyTreeModel_dataChanged)
        
        self.treeView.setModel(self.proxyTreeModel)
        self.treeView.setHeaderHidden(True)
        self.treeView.setAnimated(True)
        self.treeView.selectionModel().selectionChanged.connect(self.on_treeView_selectionChanged)


    # -------------------- Activation
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and obj == self.lineKeyEquivalentActivation:
            keyseq = int(event.modifiers()) + event.key()
            self.stackedWidget.currentWidget().setKeyEquivalent(keyseq)
            self.lineKeyEquivalentActivation.setText(QtGui.QKeySequence(keyseq).toString())
            return True
        return QtGui.QDialog.eventFilter(self, obj, event)


    @QtCore.pyqtSlot(int)
    def on_comboBoxActivation_currentIndexChanged(self, index):
        self.lineKeyEquivalentActivation.setVisible(index == 0)
        self.lineTabTriggerActivation.setVisible(index == 1)


    @QtCore.pyqtSlot(str)
    def on_lineEditScope_textEdited(self, text):
        self.stackedWidget.currentWidget().setScope(text)


    @QtCore.pyqtSlot(str)
    def on_lineTabTriggerActivation_textEdited(self, text):
        self.stackedWidget.currentWidget().setTabTrigger(text)


    def configActivation(self):
        self.comboBoxActivation.addItem("Key Equivalent")
        self.comboBoxActivation.addItem("Tab Trigger")
        self.lineKeyEquivalentActivation.installEventFilter(self)


    def saveChanges(self):
        #TODO: ver si tengo que guardar el current editor
        current = self.stackedWidget.currentWidget()
        if current.isChanged:
            if current.TYPE != "":
                if current.TYPE == "bundle":
                    self.manager.updateBundle(current.bundleItem, self.namespace, **current.changes)
                elif current.TYPE == "templatefile":
                    self.manager.updateTemplateFile(current.bundleItem, self.namespace, **current.changes)
                else:
                    self.manager.updateBundleItem(current.bundleItem, self.namespace, **current.changes)


    def editTreeItem(self, treeItem):
        self.saveChanges()
        editor = self.getEditorForTreeItem(treeItem) if treeItem is not None else self.getEditorBase()
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
