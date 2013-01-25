#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import codecs

from prymatex.qt import QtCore, QtGui
from prymatex.qt.helpers import create_menu, extend_menu_section

from prymatex.core import PMXBaseDock

from prymatex import resources
from prymatex.utils.i18n import ugettext as _
from prymatex.core.settings import pmxConfigPorperty

from prymatex.gui.dialogs.template import PMXNewFromTemplateDialog
from prymatex.gui.dialogs.project import PMXNewProjectDialog
from prymatex.gui.dialogs.messages import CheckableMessageBox
from prymatex.gui.dialogs.input import ReplaceRenameInputDialog
from prymatex.gui.dialogs.bundles.filter import BundleFilterDialog

from prymatex.ui.dockers.projects import Ui_ProjectsDock

from prymatex.gui.dockers.fstasks import PMXFileSystemTasks

from prymatex.models.projects import ProjectTreeNode
from prymatex.models.projects.lists import SelectableProjectFileModel

class PMXProjectDock(QtGui.QDockWidget, Ui_ProjectsDock, PMXFileSystemTasks, PMXBaseDock):
    SHORTCUT = "F8"
    ICON = resources.getIcon("project-development")
    PREFERED_AREA = QtCore.Qt.LeftDockWidgetArea

    #=======================================================================
    # Settings
    #=======================================================================
    SETTINGS_GROUP = 'Projects'
    @pmxConfigPorperty(default = '')
    def customFilters(self, filters):
        print filters
        filters = map(lambda p: p.strip(), filters.split(","))
        self.selectableProjectFileModel.setBaseFilters(filters)
        self.projectTreeProxyModel.setFilterRegExp(",".join(filters))
    
    def __init__(self, parent):
        QtGui.QDockWidget.__init__(self, parent)
        PMXBaseDock.__init__(self)
        self.setupUi(self)
        self.projectManager = self.application.projectManager
        self.fileManager = self.application.fileManager
        self.projectTreeProxyModel = self.projectManager.projectTreeProxyModel
    
        self.setupPropertiesDialog()
        self.setupTreeViewProjects()
        
        # Model for selector dialog
        self.selectableProjectFileModel = SelectableProjectFileModel(self.projectManager, self.fileManager, parent = self)
        
        # Bundle Filter Dialog
        self.bundleFilterDialog = BundleFilterDialog(self)
        self.bundleFilterDialog.setWindowTitle("Select Related Bundles")
        self.bundleFilterDialog.setModel(self.projectManager.projectMenuProxyModel)
        self.bundleFilterDialog.setHelpVisible(False)
        
    def initialize(self, mainWindow):
        PMXBaseDock.initialize(self, mainWindow)
        #TODO: ver el tema de proveer servicios esta instalacion en la main window es pedorra
        mainWindow.projects = self
    
    @classmethod
    def contributeToSettings(cls):
        from prymatex.gui.settings.project import ProjectSettingsWidget
        from prymatex.gui.settings.addons import AddonsSettingsWidgetFactory
        return [ ProjectSettingsWidget, AddonsSettingsWidgetFactory("project") ]
    
    # Contributes to Main Menu
    @classmethod
    def contributeToMainMenu(cls, addonClasses):
        navigation = {
            'text': 'Navigation',
            'items': [
                "-",
                {'text': 'Go To Project File',
                 'callback': cls.on_actionGoToProjectFile_triggered,
                 'shortcut': 'Meta+Ctrl+Shift+F',
                 }
            ]}
        menuContributions = { "Navigation": navigation}
        for addon in addonClasses:
            update_menu(menuContributions, addon.contributeToMainMenu())
        return menuContributions
    
    # ------------------ Menu Actions
    def on_actionGoToProjectFile_triggered(self):
        filePath = self.mainWindow.selectorDialog.select(self.selectableProjectFileModel, title=_("Select Project File"))
        if filePath is not None:
            index = self.projectTreeProxyModel.indexForPath(filePath)
            self.treeViewProjects.setCurrentIndex(index)
            self.application.openFile(filePath)

    def addFileSystemNodeFormater(self, formater):
        self.projectTreeProxyModel.addNodeFormater(formater)
    
    def saveState(self):
        expandedIndexes = filter(lambda index: self.treeViewProjects.isExpanded(index), self.projectTreeProxyModel.persistentIndexList())
        expandedPaths = map(lambda index: self.projectTreeProxyModel.node(index).path(), expandedIndexes)
        return { "expanded": expandedPaths }

    def restoreState(self, state):
        #Expanded Nodes
        map(lambda index: index.isValid() and self.treeViewProjects.setExpanded(index, True), 
            map(lambda path: self.projectTreeProxyModel.indexForPath(path), state["expanded"]))

    def environmentVariables(self):
        environment = PMXBaseDock.environmentVariables(self)
        indexes = self.treeViewProjects.selectedIndexes()
        if indexes:
            node = self.currentNode()
            paths = map(lambda node: self.application.fileManager.normcase(node.path()),
                        [ self.projectTreeProxyModel.node(index) for index in indexes ])
            environment.update({
                'TM_SELECTED_FILE': node.path(), 
                'TM_SELECTED_FILES': " ".join(["'%s'" % path for path in paths ])
            })
        return environment
        
    def keyPressEvent(self, event):
        if not self.runKeyHelper(event):
            return QtGui.QDockWidget.keyPressEvent(self, event)

    def setupPropertiesDialog(self):
        from prymatex.gui.dialogs.properties import PMXPropertiesDialog
        
        from prymatex.gui.properties.project import ProjectPropertiesWidget
        from prymatex.gui.properties.environment import EnvironmentPropertiesWidget
        from prymatex.gui.properties.resource import ResoucePropertiesWidget
        
        self.application.populateComponent(PMXPropertiesDialog)
        self.propertiesDialog = PMXPropertiesDialog(self)
        
        self.application.extendComponent(ProjectPropertiesWidget)
        self.application.extendComponent(EnvironmentPropertiesWidget)
        self.application.extendComponent(ResoucePropertiesWidget)
        self.propertiesDialog.register(ProjectPropertiesWidget(self))
        self.propertiesDialog.register(EnvironmentPropertiesWidget(self))
        self.propertiesDialog.register(ResoucePropertiesWidget(self))
        #TODO: Para cada add-on registrar los correspondientes properties

    def setupTreeViewProjects(self):
        self.treeViewProjects.setModel(self.projectTreeProxyModel)
        
        self.treeViewProjects.setHeaderHidden(True)
        self.treeViewProjects.setUniformRowHeights(False)
        
        #Setup Context Menu
        optionsMenu = { 
            "text": "Project Options",
            "items": [
                {   "text": "Order",
                    "items": [
                        (self.actionOrderByName, self.actionOrderBySize, self.actionOrderByDate, self.actionOrderByType),
                        "-", self.actionOrderDescending, self.actionOrderFoldersFirst
                    ]
                }
            ]
        }

        self.actionOrderFoldersFirst.setChecked(True)
        self.actionOrderByName.trigger()
        
        self.projectOptionsMenu, _ = create_menu(self, optionsMenu)
        self.pushButtonOptions.setMenu(self.projectOptionsMenu)

        #Connect context menu
        self.treeViewProjects.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeViewProjects.customContextMenuRequested.connect(self.showProjectTreeViewContextMenu)
        
        #=======================================================================
        # Drag and Drop (see the proxy model)
        #=======================================================================
        self.treeViewProjects.setDragEnabled(True)
        self.treeViewProjects.setAcceptDrops(True)
        self.treeViewProjects.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.treeViewProjects.setDropIndicatorShown(True)

        self.treeViewProjects.setAlternatingRowColors(True)
        self.treeViewProjects.setAnimated(True)
        
        # Selection Mode
        self.treeViewProjects.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
    
    #================================================
    # Build Menus
    #================================================
    def buildContextMenu(self, index):    
        contextMenu = { 
            "text": "Context",
            "items": [
                {   "text": "New",
                    "items": [
                        self.actionNewFolder, self.actionNewFile, "-", self.actionNewFromTemplate, self.actionNewProject,
                    ]
                },
                "--refresh",
                self.actionRefresh,
                "--bundles"
            ]
        }
        if index.isValid():
            node = self.projectTreeProxyModel.node(index)
            self.extendFileSystemItemMenu(contextMenu, node)
            self.extendAddonsItemMenu(contextMenu, node)
            self.extendProjectBundleItemMenu(contextMenu, node)
        # contextMenu, contextMenuActions = create_menu(contextMenu, self, useSeparatorName = True)
        contextMenu, contextMenuActions = create_menu(self, contextMenu)
        
        for action in contextMenuActions:
            if hasattr(action, "callback"):
                action.triggered.connect(action.callback)

        contextMenu.aboutToShow.connect(self.on_contextMenu_aboutToShow)
        contextMenu.aboutToHide.connect(self.on_contextMenu_aboutToHide)
        contextMenu.triggered.connect(self.on_contextMenu_triggered)
        return contextMenu
        
    def on_contextMenu_aboutToShow(self):      
        # TODO Quiza un metodo que haga esto en el manager  
        self.application.supportManager.setEditorAvailable(False)
        self.application.supportManager.blockSignals(True)
                
    def on_contextMenu_aboutToHide(self):
        self.application.supportManager.setEditorAvailable(True)
        def restore_supportManager_signals():
            self.application.supportManager.blockSignals(False)
        # TODO No estoy muy contento con esto pero que le vamos a hacer
        QtCore.QTimer.singleShot(0, restore_supportManager_signals)

    def on_contextMenu_triggered(self, action):
        if hasattr(action, "bundleTreeNode"):
            node = self.currentNode()
            env =   {   'TM_FILEPATH': node.path(),
                        'TM_FILENAME': node.nodeName(),
                        'TM_DIRECTORY': node.nodeParent().path() } if node.isfile else {   'TM_DIRECTORY': node.path() }
            
            env.update(node.project().environmentVariables())
            self.mainWindow.insertBundleItem(action.bundleTreeNode, environment = env)
    
    def extendFileSystemItemMenu(self, menu, node):
        extend_menu_section(menu, ["--open", self.actionOpenSystemEditor, "--handlepaths", self.actionDelete, self.actionRename])
        #extend_menu_section(menu, ["--interact", self.actionSetInTerminal ], section = -1)
        # TODO Quiza sea mejor ponerle un type y controlar contra una cadena
        if isinstance(node, ProjectTreeNode):
            extend_menu_section(menu, [self.actionPaste, self.actionRemove], section = "handlepaths", position = 0)
            #extend_menu_section(menu, [self.actionCloseProject, self.actionOpenProject], section = "refresh")
            #extend_menu_section(menu, [self.actionBashInit], section = "interact")
            extend_menu_section(menu, [self.actionProjectBundles, self.actionSelectRelatedBundles], section = "bundles")
        else:
            extend_menu_section(menu, [self.actionCut, self.actionCopy, self.actionPaste], section = "handlepaths", position = 0)
        if node.isfile:
            extend_menu_section(menu, self.actionOpen, section = "open", position = 0)

        #El final
        extend_menu_section(menu, ["--properties", self.actionProperties], section = -1)

    def extendAddonsItemMenu(self, menu, node):
        #Menu de los addons
        addonMenues = [ "-" ]
        for addon in self.addons:
            addonMenues.extend(addon.contributeToContextMenu(node))
        if len(addonMenues) > 1:
            extend_menu_section(menu, addonMenues, section = 'properties')
        
    def extendProjectBundleItemMenu(self, menu, node):
        #Menu de los bundles relacionados al proyecto
        #Try get all bundles for project bundle definition
        bundles = map(lambda uuid: self.application.supportManager.getManagedObject(uuid), node.project().bundleMenu or [])
        #Filter None bundles
        bundles = filter(lambda bundle: bundle is not None, bundles)
        #Sort by name
        bundles = sorted(bundles, key=lambda bundle: bundle.name)
        if bundles:
            bundleMenues = map(lambda bundle: self.application.supportManager.menuForBundle(bundle), bundles)
            extend_menu_section(menu, bundleMenues, section = "bundles", position = 0)

    #================================================
    # Tree View Project
    #================================================
    def showProjectTreeViewContextMenu(self, point):
        index = self.treeViewProjects.indexAt(point)
        if not index.isValid():
            index = self.treeViewProjects.currentIndex()
        self.buildContextMenu(index).popup(self.treeViewProjects.mapToGlobal(point))
    
    def on_treeViewProjects_doubleClicked(self, index):
        self.on_actionOpen_triggered()

    def currentPath(self):
        return self.projectTreeProxyModel.filePath(self.treeViewProjects.currentIndex())

    def currentNode(self):
        return self.projectTreeProxyModel.node(self.treeViewProjects.currentIndex())
        
    def currentDirectory(self):
        return self.application.fileManager.directory(self.currentPath())

    #================================================
    # Actions Create, Delete, Rename objects
    #================================================      
    @QtCore.pyqtSlot()
    def on_actionNewFile_triggered(self):
        currentDirectory = self.currentDirectory()
        filePath = self.createFile(currentDirectory)
        if filePath is not None:
            self.application.openFile(filePath)
            #TODO: si esta en auto update ver como hacer los refresh
            self.projectTreeProxyModel.refreshPath(currentDirectory)
    
    @QtCore.pyqtSlot()
    def on_actionNewFromTemplate_triggered(self):
        currentDirectory = self.currentDirectory()
        filePath = self.createFileFromTemplate(currentDirectory)
        if filePath is not None:
            self.application.openFile(filePath)
            #TODO: si esta en auto update ver como hacer los refresh
            self.projectTreeProxyModel.refreshPath(currentDirectory)
    
    @QtCore.pyqtSlot()
    def on_actionNewFolder_triggered(self):
        currentDirectory = self.currentDirectory()
        dirPath = self.createDirectory(currentDirectory)
        if dirPath is not None:
            #TODO: si esta en auto update ver como hacer los refresh
            self.projectTreeProxyModel.refreshPath(currentDirectory)

    @QtCore.pyqtSlot()
    def on_actionNewProject_triggered(self):
        PMXNewProjectDialog.getNewProject(self)

    @QtCore.pyqtSlot()
    def on_actionDelete_triggered(self):
        # TODO: Cuidado porque si van cambiando los index puede ser que esto no se comporte como se espera
        # es mejor unos maps antes para pasarlos a path
        for index in self.treeViewProjects.selectedIndexes():
            treeNode = self.projectTreeProxyModel.node(index)
            if treeNode.isproject:
                #Es proyecto
                question = CheckableMessageBox.questionFactory(self,
                    "Delete project",
                    "Are you sure you want to delete project '%s' from the workspace?" % treeNode.name,
                    "Delete project contents on disk (cannot be undone)",
                    QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel,
                    QtGui.QMessageBox.Ok
                )
                question.setDetailedText("Project location:\n%s" % treeNode.path())
                ret = question.exec_()
                if ret == QtGui.QMessageBox.Ok:
                    self.application.projectManager.deleteProject(treeNode, removeFiles = question.isChecked())
            else:
                self.deletePath(treeNode.path())
            self.projectTreeProxyModel.refresh(index.parent())

    @QtCore.pyqtSlot()
    def on_actionRemove_triggered(self):
        treeNode = self.currentNode()
        if treeNode.isproject:
            ret = QtGui.QMessageBox.question(self,
                "Remove project",
                "Are you sure you want to remove project '%s' from the workspace?" % treeNode.name,
                QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel,
                QtGui.QMessageBox.Ok
            )
            if ret == QtGui.QMessageBox.Ok:
                self.application.projectManager.removeProject(treeNode)

    @QtCore.pyqtSlot()
    def on_actionRename_triggered(self):
        self.renamePath(self.currentPath())
        self.projectTreeProxyModel.refresh(self.treeViewProjects.currentIndex())

    @QtCore.pyqtSlot()
    def on_actionCloseProject_triggered(self):
        treeNode = self.currentNode()
        if treeNode.isproject:
            self.application.projectManager.closeProject(treeNode)
    
    @QtCore.pyqtSlot()
    def on_actionOpenProject_triggered(self):
        treeNode = self.currentNode()
        if treeNode.isproject:
            self.application.projectManager.openProject(treeNode)
    
    @QtCore.pyqtSlot()
    def on_actionProperties_triggered(self):
        self.propertiesDialog.exec_(self.currentNode())

    @QtCore.pyqtSlot()
    def on_actionRefresh_triggered(self):
        indexes = self.treeViewProjects.selectedIndexes()
        for index in indexes:
            self.projectTreeProxyModel.refresh(index)

    @QtCore.pyqtSlot()
    def on_actionOpen_triggered(self):
        node = self.currentNode()
        if node.isfile:
            self.application.openFile(node.path())
        
    @QtCore.pyqtSlot()
    def on_actionOpenSystemEditor_triggered(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("file://%s" % self.currentPath(), QtCore.QUrl.TolerantMode))
    
    @QtCore.pyqtSlot()
    def on_pushButtonCollapseAll_pressed(self):
        self.treeViewProjects.collapseAll()

    @QtCore.pyqtSlot(bool)
    def on_pushButtonSync_toggled(self, checked):
        if checked:
            #Conectar señal
            self.mainWindow.currentEditorChanged.connect(self.on_mainWindow_currentEditorChanged)
            self.on_mainWindow_currentEditorChanged(self.mainWindow.currentEditor())
        else:
            #Desconectar señal
            self.mainWindow.currentEditorChanged.disconnect(self.on_mainWindow_currentEditorChanged)
    
    def on_mainWindow_currentEditorChanged(self, editor):
        if editor is not None and not editor.isNew():
            index = self.projectTreeProxyModel.indexForPath(editor.filePath)
            self.treeViewProjects.setCurrentIndex(index)

    @QtCore.pyqtSlot()
    def on_actionProjectBundles_triggered(self):
        project = self.currentNode()
        self.application.bundleEditorDialog.execEditor(namespaceFilter = project.namespace)
    
    @QtCore.pyqtSlot()
    def on_actionSelectRelatedBundles_triggered(self):
        project = self.currentNode()
        self.projectManager.projectMenuProxyModel.setCurrentProject(project)
        self.bundleFilterDialog.exec_()
        
    @QtCore.pyqtSlot()
    def on_actionCopy_triggered(self):
        mimeData = self.projectTreeProxyModel.mimeData( self.treeViewProjects.selectedIndexes() )
        self.application.clipboard().setMimeData(mimeData)
        
    @QtCore.pyqtSlot()
    def on_actionCut_triggered(self):
        mimeData = self.projectTreeProxyModel.mimeData( self.treeViewProjects.selectedIndexes() )
        self.application.clipboard().setMimeData(mimeData)
        
    @QtCore.pyqtSlot()
    def on_actionPaste_triggered(self):
        parentPath = self.currentPath()
        mimeData = self.application.clipboard().mimeData()
        if mimeData.hasUrls() and os.path.isdir(parentPath):
            for url in mimeData.urls():
                srcPath = url.toLocalFile()
                basename = self.application.fileManager.basename(srcPath)
                dstPath = os.path.join(parentPath, basename)
                while self.application.fileManager.exists(dstPath):
                    basename, ret = ReplaceRenameInputDialog.getText(self, _("Already exists"), 
                        _("Destiny already exists\nReplace or or replace?"), text = basename, )
                    if ret == ReplaceRenameInputDialog.Cancel: return
                    if ret == ReplaceRenameInputDialog.Replace: break
                    dstPath = os.path.join(parentPath, basename)
                if os.path.isdir(srcPath):
                    self.application.fileManager.copytree(srcPath, dstPath)
                else:
                    self.application.fileManager.copy(srcPath, dstPath)
            self.projectTreeProxyModel.refresh(self.treeViewProjects.currentIndex())

    #================================================
    # Custom filters
    #================================================
    @QtCore.pyqtSlot()
    def on_pushButtonCustomFilters_pressed(self):
        filters, accepted = QtGui.QInputDialog.getText(self, _("Custom Filter"), 
                                _("Enter the filters (separated by comma)\nOnly * and ? may be used for custom matching"), 
                                text = self.customFilters)
        if accepted:
            #Save and set filters
            self.settings.setValue('customFilters', filters)
            self.projectTreeProxyModel.setFilterRegExp(filters)
            
    #================================================
    # Sort and order Actions
    #================================================      
    @QtCore.pyqtSlot()
    def on_actionOrderByName_triggered(self):
        self.projectTreeProxyModel.sortBy("name", self.actionOrderFoldersFirst.isChecked(), self.actionOrderDescending.isChecked())
    
    @QtCore.pyqtSlot()
    def on_actionOrderBySize_triggered(self):
        self.projectTreeProxyModel.sortBy("size", self.actionOrderFoldersFirst.isChecked(), self.actionOrderDescending.isChecked())
    
    @QtCore.pyqtSlot()
    def on_actionOrderByDate_triggered(self):
        self.projectTreeProxyModel.sortBy("date", self.actionOrderFoldersFirst.isChecked(), self.actionOrderDescending.isChecked())
    
    @QtCore.pyqtSlot()
    def on_actionOrderByType_triggered(self):
        self.projectTreeProxyModel.sortBy("type", self.actionOrderFoldersFirst.isChecked(), self.actionOrderDescending.isChecked())
    
    @QtCore.pyqtSlot()
    def on_actionOrderDescending_triggered(self):
        self.projectTreeProxyModel.sortBy(self.projectTreeProxyModel.orderBy, self.actionOrderFoldersFirst.isChecked(), self.actionOrderDescending.isChecked())
    
    @QtCore.pyqtSlot()
    def on_actionOrderFoldersFirst_triggered(self):
        self.projectTreeProxyModel.sortBy(self.projectTreeProxyModel.orderBy, self.actionOrderFoldersFirst.isChecked(), self.actionOrderDescending.isChecked())

    #================================================
    # Helper actions
    #================================================
    def refresh(self):
        self.on_actionRefresh_triggered()
        
    def copy(self):
        self.on_actionCopy_triggered()
        
    def paste(self):
        self.on_actionPaste_triggered()
        
    def cut(self):
        self.on_actionCut_triggereda()

    def delete(self):
        self.on_actionDelete_triggered()
        
    def rename(self):
        self.on_actionRefresh_triggered()
