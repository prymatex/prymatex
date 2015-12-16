#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets

from prymatex.core.components import PrymatexDialog
from prymatex.core import config

# UI
from prymatex.ui.support.editor import Ui_BundleEditorDialog

from prymatex.gui.dialogs.bundles import widgets
from prymatex.gui.dialogs.bundles.filter import BundleFilterDialog

class BundleEditorDialog(PrymatexDialog, Ui_BundleEditorDialog, QtWidgets.QDialog):
    BASE_EDITOR = -1 #El ultimo es el editor base, no tiene nada
    
    def __init__(self, **kwargs):
        super(BundleEditorDialog, self).__init__(**kwargs)
        self.setupUi(self)
        self.namespace = None
        self.namespaces = []
        
        self.manager = self.application().supportManager
        self.proxyTreeModel = self.manager.bundleProxyTreeModel
        
        # Connect signals
        self.manager.bundleChanged.connect(self.on_manager_itemChanged)
        self.manager.bundleItemChanged.connect(self.on_manager_itemChanged)
        self.finished.connect(self.on_bundleEditor_finished)
        
        #Cargar los widgets editores
        self.configEditorWidgets()
        
        #Configurar filter, tree, toolbar y activaciones
        self.configSelectTop()
        self.configTreeView()
        self.configToolbar()
        self.configActivation()

    # --------------- signal handlers
    def on_manager_itemChanged(self, item):
        editor = self.currentEditor()
        if editor.bundleItem is not None and editor.bundleItem == item and editor.getName() != item.name:
            editor.setName(item.name)
            self.labelTitle.setText(editor.title())
            self.lineEditName.setText(editor.getName())

    def on_bundleEditor_finished(self, code):
        self.saveChanges()

    # ---------------- custom execs
    def exec_(self):
        #Limiar el editor
        self.setCurrentEditor(self.editors[-1])
        #Quitar seleccion
        firstIndex = self.proxyTreeModel.index(0, 0)
        self.treeView.setSelection(self.treeView.visualRect(firstIndex), QtCore.QItemSelectionModel.Clear)
        
        return super(BundleEditorDialog, self).exec_()

    def execEditor(self, types=None, namespaces=None, title="Bundle Editor"):
        # Title
        self.setWindowTitle(title)
        
        # Set namespace and filters
        self.namespace = namespaces and namespaces[0] or config.USR_NS_NAME
        self.proxyTreeModel.setFilterNamespace(namespaces)
        self.proxyTreeModel.setFilterBundleItemTypes(types)
        index = self.comboBoxItemFilter.findData(types)
        self.comboBoxItemFilter.setCurrentIndex(index)
        
        # Go!
        self.exec_()

    def execCommand(self):
        return self.execEditor(("command",))

    def execLanguage(self):
        return self.execEditor(("syntax",))

    def execSnippet(self):
        return self.execEditor(("snippet",))

    def configEditorWidgets(self):
        self.stackedWidget = QtWidgets.QStackedWidget()
        self.stackedWidget.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.stackedWidget.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.editorsLayout.insertWidget(1, self.stackedWidget)
        self.indexes = {}
        self.editors = [ widgets.SnippetEditorWidget(self),
                         widgets.CommandEditorWidget(self),
                         widgets.DragCommandEditorWidget(self),
                         widgets.BundleEditorWidget(self),
                         widgets.StaticFileEditorWidget(self),
                         widgets.TemplateEditorWidget(self),
                         widgets.PreferenceEditorWidget(self),
                         widgets.LanguageEditorWidget(self),
                         widgets.MacroEditorWidget(self),
                         widgets.ProjectEditorWidget(self),
                         widgets.NoneEditorWidget(self) ]
        for editor in self.editors:
            self.indexes[editor.type()] = self.stackedWidget.addWidget(editor)

    # ----------------- Toolbar create and delete bundle items
    def getBundleForIndex(self, index):
        if not index.isValid():
            return self.manager.getDefaultBundle()
        bundle = self.proxyTreeModel.node(index)
        while bundle.type() != 'bundle':
            bundle = bundle.nodeParent()
        return bundle

    def createBundleItem(self, itemType):
        index = self.treeView.currentIndex()
        bundle = self.getBundleForIndex(index)
        bundleItemNode = self.manager.createBundleItem(itemType, bundle, self.namespace)
        sIndex = self.manager.bundleTreeModel.createIndex(bundleItemNode.row(), 0, bundleItemNode)
        index = self.proxyTreeModel.mapFromSource(sIndex)
        self.treeView.setCurrentIndex(index)
        self.editTreeItem(bundleItemNode)
        self.treeView.edit(index)
        
    @QtCore.Slot()
    def on_actionCommand_triggered(self):
        self.createBundleItem("command")

    @QtCore.Slot()        
    def on_actionDragCommand_triggered(self):
        self.createBundleItem("dragcommand")

    @QtCore.Slot()        
    def on_actionLanguage_triggered(self):
        self.createBundleItem("syntax")

    @QtCore.Slot()        
    def on_actionSnippet_triggered(self):
        self.createBundleItem("snippet")

    @QtCore.Slot()        
    def on_actionTemplate_triggered(self):
        self.createBundleItem("template")

    @QtCore.Slot()        
    def on_actionProject_triggered(self):
        self.createBundleItem("project")

    @QtCore.Slot()        
    def on_actionStaticFile_triggered(self):
        index = self.treeView.currentIndex()
        if index.isValid():
            template = self.proxyTreeModel.node(index)
            if template.type() == 'staticfile':
                template = template.nodeParent()
        self.manager.createStaticFile(template, self.namespace)

    @QtCore.Slot()
    def on_actionPreferences_triggered(self):
        self.createBundleItem("preference")

    @QtCore.Slot()
    def on_actionBundle_triggered(self):
        bundleNode = self.manager.createBundle(self.namespace)
        sIndex = self.manager.bundleTreeModel.createIndex(bundleNode.row(), 0, bundleNode)
        index = self.proxyTreeModel.mapFromSource(sIndex)
        self.treeView.setCurrentIndex(index)
        self.editTreeItem(bundleNode)
        self.treeView.edit(index)

    @QtCore.Slot()
    def on_pushButtonRemove_pressed(self):
        index = self.treeView.currentIndex()
        if index.isValid():
            item = self.proxyTreeModel.node(index)
            if item.type() == 'bundle':
                self.manager.deleteBundle(item)
            elif item.type() == 'staticfile':
                self.manager.deleteStaticFile(item)
            else:
                self.manager.deleteBundleItem(item)

    @QtCore.Slot()
    def on_pushButtonFilter_pressed(self):
        self.bundleFilterDialog.show()

    def configToolbar(self):
        self.toolbarMenu = QtWidgets.QMenu("Menu", self)
        action = QtWidgets.QAction("New Command", self)
        action.triggered.connect(self.on_actionCommand_triggered)
        self.toolbarMenu.addAction(action)
        action = QtWidgets.QAction("New Drag Command", self)
        action.triggered.connect(self.on_actionDragCommand_triggered)
        self.toolbarMenu.addAction(action)
        action = QtWidgets.QAction("New Language", self)
        action.triggered.connect(self.on_actionLanguage_triggered)
        self.toolbarMenu.addAction(action)
        action = QtWidgets.QAction("New Snippet", self)
        action.triggered.connect(self.on_actionSnippet_triggered)
        self.toolbarMenu.addAction(action)
        action = QtWidgets.QAction("New Template", self)
        action.triggered.connect(self.on_actionTemplate_triggered)
        self.toolbarMenu.addAction(action)
        action = QtWidgets.QAction("New Project", self)
        action.triggered.connect(self.on_actionProject_triggered)
        self.toolbarMenu.addAction(action)
        self.staticFileAction = QtWidgets.QAction("New Static File", self)
        self.staticFileAction.triggered.connect(self.on_actionStaticFile_triggered)
        self.toolbarMenu.addAction(self.staticFileAction)
        action = QtWidgets.QAction("New Preferences", self)
        action.triggered.connect(self.on_actionPreferences_triggered)
        self.toolbarMenu.addAction(action)
        self.toolbarMenu.addSeparator()
        action = QtWidgets.QAction("New Bundle", self)
        action.triggered.connect(self.on_actionBundle_triggered)
        self.toolbarMenu.addAction(action)
        
        def conditionalEnabledStaticFile():
            node = self.proxyTreeModel.node(self.treeView.currentIndex())
            self.staticFileAction.setEnabled(not node.isRootNode() and (node.type() in ["template", "staticfile", "project"]))
        self.toolbarMenu.aboutToShow.connect(conditionalEnabledStaticFile)
        
        self.pushButtonAdd.setMenu(self.toolbarMenu)
        
        #Bundle global filter dialog
        self.bundleFilterDialog = BundleFilterDialog(self)
        self.bundleFilterDialog.setModel(self.manager.bundleProxyModel)

    # ------------------- Filter bundle items
    def on_comboBoxItemFilter_returnPressed(self):
        self.proxyTreeModel.setFilterBundleItemTypes(None)
        self.proxyTreeModel.setFilterRegExp(".*%s.*" % self.comboBoxItemFilter.currentText())

    @QtCore.Slot(int)
    def on_comboBoxItemFilter_activated(self, index):
        value = self.comboBoxItemFilter.itemData(index)
        self.proxyTreeModel.setFilterBundleItemTypes(value)

    def configSelectTop(self):
        self.comboBoxItemFilter.addItem("Show all", ())
        self.comboBoxItemFilter.addItem(self.resources().get_icon("bundle-item-syntax"), "Languages", ("syntax",))
        self.comboBoxItemFilter.addItem(self.resources().get_icon("bundle-item-snippet"), "Snippets", ("snippet",))
        self.comboBoxItemFilter.addItem(self.resources().get_icon("bundle-item-macro"), "Macros", ("macro",))
        self.comboBoxItemFilter.addItem(self.resources().get_icon("bundle-item-command"), "Commands", ("command",))
        self.comboBoxItemFilter.addItem(self.resources().get_icon("bundle-item-dragcommand"), "DragCommands", ("dragcommand",))
        self.comboBoxItemFilter.addItem(self.resources().get_icon("bundle-item-preference"), "Preferences", ("preference",))
        self.comboBoxItemFilter.addItem(self.resources().get_icon("bundle-item-template"), "Templates", ("template", "staticfile"))
        self.comboBoxItemFilter.addItem(self.resources().get_icon("bundle-item-project"), "Projects", ("project", "staticfile"))
        self.comboBoxItemFilter.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        self.comboBoxItemFilter.lineEdit().returnPressed.connect(self.on_comboBoxItemFilter_returnPressed)

    # --------------------------- Tree View display the bundle items model
    def getEditorBase(self):
        return self.editors[self.BASE_EDITOR]

    def getEditorForTreeItem(self, node):
        item = node.bundleItem()
        if not node.isRootNode() and item.type() in self.indexes:
            index = self.indexes[item.type()]
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
        self.labelTitle.setText(current.title())

    def on_treeView_selectionChanged(self, selected, deselected):
        indexes = selected.indexes()
        if indexes:
            treeItem = self.proxyTreeModel.node(indexes[0])
            self.editTreeItem(treeItem)
        else:
            self.editTreeItem(None)
            
    def configTreeView(self, manager=None):
        self.proxyTreeModel.dataChanged.connect(self.on_proxyTreeModel_dataChanged)
        
        self.treeView.setModel(self.proxyTreeModel)
        self.treeView.setHeaderHidden(True)
        self.treeView.setAnimated(True)
        self.treeView.selectionModel().selectionChanged.connect(self.on_treeView_selectionChanged)

    # -------------------- Activation
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and obj == self.lineEditKeyEquivalentActivation:
            keyseq = QtWidgets.QKeySequence(int(event.modifiers()) + event.key())
            self.stackedWidget.currentWidget().setKeySequence(keyseq)
            self.lineEditKeyEquivalentActivation.setText(keyseq.toString())
            return True
        return QtWidgets.QDialog.eventFilter(self, obj, event)

    @QtCore.Slot()
    def on_pushButtonCleanKeyEquivalent_pressed(self):
        self.stackedWidget.currentWidget().setKeySequence(None)
        self.lineEditKeyEquivalentActivation.setText("")

    @QtCore.Slot(str)
    def on_lineEditScopeSelector_textEdited(self, text):
        self.stackedWidget.currentWidget().setScope(text)

    @QtCore.Slot(str)
    def on_lineEditTabTriggerActivation_textEdited(self, text):
        self.stackedWidget.currentWidget().setTabTrigger(text)

    @QtCore.Slot(str)
    def on_lineEditName_textEdited(self, text):
        self.stackedWidget.currentWidget().setName(text)

    def configActivation(self):
        self.lineEditKeyEquivalentActivation.installEventFilter(self)

    def saveChanges(self):
        current = self.stackedWidget.currentWidget()
        if current.isChanged():
            if current.type() == "bundle":
                self.manager.updateBundle(current.bundleItem, self.namespace, **current.changes)
            elif current.type() == "staticfile":
                self.manager.updateStaticFile(current.bundleItem, self.namespace, **current.changes)
            else:
                self.manager.updateBundleItem(current.bundleItem, self.namespace, **current.changes)

    def editTreeItem(self, treeItem):
        self.saveChanges()
        editor = self.getEditorForTreeItem(treeItem) if treeItem is not None else self.getEditorBase()
        if editor != None:
            editor.edit(treeItem.bundleItem())
            self.setCurrentEditor(editor)

    def currentEditor(self):
        return self.stackedWidget.currentWidget()

    def setCurrentEditor(self, editor):
        self.stackedWidget.setCurrentWidget(editor)
        self.labelTitle.setText(editor.title())
        self.lineEditName.setText(editor.getName())
        self.lineEditSemanticClass.setText(editor.getSemanticClass())
        scope = editor.getScope()
        tabTrigger = editor.getTabTrigger()
        keySequence = editor.getKeySequence()
        semanticClass = editor.getSemanticClass()
        # Scope
        self.lineEditScopeSelector.setEnabled(scope is not None)
        self.lineEditScopeSelector.setText(scope is not None and scope or "")
        # KeySequence
        self.lineEditKeyEquivalentActivation.setEnabled(keySequence is not None)
        self.lineEditKeyEquivalentActivation.setText(keySequence and\
            keySequence.toString() or "")
        # TabTrigger
        self.lineEditTabTriggerActivation.setEnabled(tabTrigger is not None)
        self.lineEditTabTriggerActivation.setText(tabTrigger or "")
        # SemanticClass
        self.lineEditSemanticClass.setEnabled(semanticClass is not None)
        self.lineEditSemanticClass.setText(semanticClass or "")
