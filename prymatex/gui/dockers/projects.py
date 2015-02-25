#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import codecs

# Project Docker parents
from prymatex.core import PrymatexDock
from prymatex.ui.dockers.projects import Ui_ProjectsDock
from prymatex.gui.dockers.fstasks import FileSystemTasks

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.qt.helpers import create_menu, extend_menu_section
from prymatex.qt.extensions import CheckableMessageBox, ReplaceRenameInputDialog

from prymatex.utils.i18n import ugettext as _
from prymatex.core.settings import ConfigurableItem, ConfigurableHook

from prymatex.gui.dialogs.bundles.filter import BundleFilterDialog

from prymatex.models.projects import ProjectTreeNode
from prymatex.models.projects.lists import SelectableProjectFileProxyModel

class ProjectsDock(PrymatexDock, FileSystemTasks, Ui_ProjectsDock, QtWidgets.QDockWidget):
    SEQUENCE = ("Docks", "ProjectsDock", "Alt+X")
    ICON = "dock-projects"
    PREFERED_AREA = QtCore.Qt.LeftDockWidgetArea

    #=======================================================================
    # Settings
    #=======================================================================
    SETTINGS = 'ProjectsDock'
    @ConfigurableItem(default = '')
    def customFilters(self, filters):
        filters = [p.strip() for p in filters.split(",")]
        self.selectableProjectFileModel.setBaseFilters(filters)
        self.projectTreeProxyModel.setFilterRegExp(",".join(filters))
    
    @ConfigurableHook("code_editor.defaultTheme")
    def defaultTheme(self, themeUUID):
        theme = self.application().supportManager.getBundleItem(themeUUID)
        self.treeViewProjects.setPalette(theme.palette())
        self.treeViewProjects.viewport().setPalette(theme.palette())
    
    def __init__(self, **kwargs):
        super(ProjectsDock, self).__init__(**kwargs)
        self.setupUi(self)
        self.projectManager = self.application().projectManager
        self.fileManager = self.application().fileManager
        self.projectTreeProxyModel = self.projectManager.projectTreeProxyModel
    
        self.setupTreeViewProjects()
        
        # Model for selector dialog
        self.selectableProjectFileModel = SelectableProjectFileProxyModel(self.projectManager, self.fileManager, parent = self)
        
        # Bundle Filter Dialog
        self.bundleFilterDialog = BundleFilterDialog(self)
        self.bundleFilterDialog.setWindowTitle("Select Related Bundles")
        self.bundleFilterDialog.setModel(self.projectManager.projectMenuProxyModel)
        self.bundleFilterDialog.setHelpVisible(False)
        
    def initialize(self, **kwargs):
        super(ProjectsDock, self).initialize(**kwargs)
        self.newProjectDialog = self.window().findChild(QtWidgets.QDialog, "NewProjectDialog")
        self.templateDialog = self.window().findChild(QtWidgets.QDialog, "TemplateDialog")
        self.bundleEditorDialog = self.window().findChild(QtWidgets.QDialog, "BundleEditorDialog")
        self.propertiesDialog = self.window().findChild(QtWidgets.QDialog, "PropertiesDialog")
        self.setupPropertiesWidgets()

    @classmethod
    def contributeToSettings(cls):
        return [ ]
    
    # Contributes to Main Menu
    @classmethod
    def contributeToMainMenu(cls):
        navigation = [
                {'text': 'Go to project file',
                 'triggered': cls.on_actionGoToProjectFile_triggered,
                 'sequence': ("Projects", "GoToProjectFiles", 'Meta+Ctrl+Shift+F'),
                 },
                {'text': 'Go to project symbol',
                 'triggered': cls.on_actionGoToProjectFile_triggered,
                 'sequence': ("Projects", "GoToProjectFiles", 'Meta+Ctrl+Shift+F'),
                 }
            ]
        return { "navigation": navigation}
    
    # ------------------ Menu Actions
    def on_actionGoToProjectFile_triggered(self):
        filePath = self.window().selectorDialog.select(self.selectableProjectFileModel, title=_("Select Project File"))
        if filePath is not None:
            index = self.projectTreeProxyModel.indexForPath(filePath)
            self.treeViewProjects.setCurrentIndex(index)
            self.application().openFile(filePath)

    def addFileSystemNodeFormater(self, formater):
        self.projectTreeProxyModel.addNodeFormater(formater)
    
    def componentState(self):
        expandedIndexes = [index for index in self.projectTreeProxyModel.persistentIndexList() if self.treeViewProjects.isExpanded(index)]
        expandedPaths = [self.projectTreeProxyModel.node(index).path() for index in expandedIndexes]
        return { "expanded": expandedPaths }

    def setComponentState(self, state):
        #Expanded Nodes
        list(map(lambda index: index.isValid() and self.treeViewProjects.setExpanded(index, True), 
            [self.projectTreeProxyModel.indexForPath(path) for path in state["expanded"]]))

    def environmentVariables(self):
        environment = PrymatexDock.environmentVariables(self)
        indexes = self.treeViewProjects.selectedIndexes()
        if indexes:
            node = self.currentNode()
            paths = [self.application().fileManager.normcase(node.path()) for node in [ self.projectTreeProxyModel.node(index) for index in indexes ]]
            environment.update({
                'TM_SELECTED_FILE': node.path(), 
                'TM_SELECTED_FILES': " ".join(["'%s'" % path for path in paths ])
            })
        return environment
    
    def setupPropertiesWidgets(self):
        from prymatex.gui.properties.project import ProjectPropertiesWidget
        from prymatex.gui.properties.environment import EnvironmentPropertiesWidget
        from prymatex.gui.properties.resource import ResoucePropertiesWidget
        
        for propertyClass in [ProjectPropertiesWidget, EnvironmentPropertiesWidget, ResoucePropertiesWidget]:
            self.application().populateComponentClass(propertyClass)
            self.application().projectManager.registerPropertyWidget(propertyClass(parent = self.propertiesDialog))

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
        
        self.projectOptionsMenu, objects = create_menu(self, optionsMenu)
        self.toolButtonOptions.setMenu(self.projectOptionsMenu)

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
        self.treeViewProjects.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
    
    #================================================
    # Build Menus
    #================================================
    def buildContextMenu(self, index):    
        contextMenu = { 
            "text": "Context",
            "items": [
                {   "text": "New",
                    "items": [
                        self.actionNewFolder, 
                        self.actionNewFile, 
                        "-", 
                        self.actionNewFromTemplate, 
                        self.actionNewProject,
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
        contextMenu, objects = create_menu(self, contextMenu, separatorName=True)
        
        contextMenu.aboutToShow.connect(self.on_contextMenu_aboutToShow)
        contextMenu.aboutToHide.connect(self.on_contextMenu_aboutToHide)
        contextMenu.triggered.connect(self.on_contextMenu_triggered)
        return contextMenu
        
    def on_contextMenu_aboutToShow(self):      
        # TODO Quiza un metodo que haga esto en el manager  
        self.application().supportManager.setEditorAvailable(False)
        self.application().supportManager.blockSignals(True)
                
    def on_contextMenu_aboutToHide(self):
        self.application().supportManager.setEditorAvailable(True)
        def restore_supportManager_signals():
            self.application().supportManager.blockSignals(False)
        # TODO No estoy muy contento con esto pero que le vamos a hacer
        QtCore.QTimer.singleShot(0, restore_supportManager_signals)

    def on_contextMenu_triggered(self, action):
        if hasattr(action, "bundleTreeNode"):
            node = self.currentNode()
            env =   {   
                'TM_FILEPATH': node.path(),
                'TM_FILENAME': node.nodeName(),
                'TM_DIRECTORY': node.nodeParent().path() 
            } if node.isfile else {
                'TM_DIRECTORY': node.path()
            }
            
            env.update(node.project().environmentVariables())
            self.window().insertBundleItem(action.bundleTreeNode, environment = env)
    
    def extendFileSystemItemMenu(self, menu, node):
        extend_menu_section(menu, ["--open", self.actionOpenSystemEditor, "--handlepaths", self.actionDelete, self.actionRename])
        #extend_menu_section(menu, ["--interact", self.actionSetInTerminal ], section = -1)
        # TODO Quiza sea mejor ponerle un type y controlar contra una cadena
        if isinstance(node, ProjectTreeNode):
            extend_menu_section(menu,
                [self.actionPaste, self.actionRemove], 
                section="handlepaths", position=0)
            #extend_menu_section(menu, [self.actionBashInit], section = "interact")
            extend_menu_section(menu, 
                [self.actionProjectBundles, self.actionSelectRelatedBundles], 
                section="bundles")
        else:
            extend_menu_section(menu, 
                [self.actionCut, self.actionCopy, self.actionPaste],
                section = "handlepaths", position = 0)
        if node.isfile:
            extend_menu_section(menu,
                self.actionOpen, section="open", position = 0)
        if node.isdir or isinstance(node, ProjectTreeNode):
            extend_menu_section(menu, [self.actionGoDown], section="refresh")
            
        #El final
        extend_menu_section(menu, 
            ["--properties", self.actionProperties], section=-1)

    def extendAddonsItemMenu(self, menu, node):
        #Menu de los addons
        addonMenues = [ "-" ]
        for component in self.components():
            addonMenues.extend(component.contributeToContextMenu(node))
        if len(addonMenues) > 1:
            extend_menu_section(menu, addonMenues, section='properties')
        
    def extendProjectBundleItemMenu(self, menu, node):
        #Menu de los bundles relacionados al proyecto
        #Try get all bundles for project bundle definition
        bundles = [self.application().supportManager.getManagedObject(uuid) for uuid in node.project().bundleMenu or []]
        #Filter None bundles
        bundles = [bundle for bundle in bundles if bundle is not None]
        #Sort by name
        bundles = sorted(bundles, key=lambda bundle: bundle.name)
        if bundles:
            bundleMenues = [self.application().supportManager.menuForBundle(bundle) for bundle in bundles]
            extend_menu_section(menu, bundleMenues, section="bundles", position=0)

    #================================================
    # Tree View Project
    #================================================
    def showProjectTreeViewContextMenu(self, point):
        index = self.treeViewProjects.indexAt(point)
        if index.isValid():
            self.treeViewProjects.setCurrentIndex(index)
            self.buildContextMenu(index).popup(self.treeViewProjects.mapToGlobal(point))
    
    def on_treeViewProjects_doubleClicked(self, index):
        self.on_actionOpen_triggered()

    def currentPath(self):
        return self.projectTreeProxyModel.filePath(self.treeViewProjects.currentIndex())

    def currentNode(self):
        return self.projectTreeProxyModel.node(self.treeViewProjects.currentIndex())
        
    def currentDirectory(self):
        return self.application().fileManager.directory(self.currentPath())
    
    #================================================
    # Actions Create, Delete, Rename objects
    #================================================      
    @QtCore.Slot()
    def on_actionNewFile_triggered(self):
        currentDirectory = self.currentDirectory()
        filePath = self.createFile(currentDirectory)
        if filePath is not None:
            self.application().openFile(filePath)
            #TODO: si esta en auto update ver como hacer los refresh
            self.projectTreeProxyModel.refreshPath(currentDirectory)
    
    @QtCore.Slot()
    def on_actionNewFromTemplate_triggered(self):
        currentDirectory = self.currentDirectory()
        filePath = self.templateDialog.createFile(fileDirectory = self.currentDirectory())
        if filePath is not None:
            self.application().openFile(filePath)
            #TODO: si esta en auto update ver como hacer los refresh
            self.projectTreeProxyModel.refreshPath(currentDirectory)
    
    @QtCore.Slot()
    def on_actionNewFolder_triggered(self):
        currentDirectory = self.currentDirectory()
        dirPath = self.createDirectory(currentDirectory)
        if dirPath is not None:
            #TODO: si esta en auto update ver como hacer los refresh
            self.projectTreeProxyModel.refreshPath(currentDirectory)

    @QtCore.Slot()
    def on_actionNewProject_triggered(self):
        self.newProjectDialog.createProject()

    @QtCore.Slot()
    def on_actionDelete_triggered(self):
        indexes = self.treeViewProjects.selectedIndexes()
        projects = []
        paths = []

        for index in indexes:
            node = self.projectTreeProxyModel.node(index)
            if node.isproject:
                #Es proyecto
                question = CheckableMessageBox.questionFactory(self,
                    "Delete project",
                    "Are you sure you want to delete project '%s' from the workspace?" % node.name,
                    "Delete project contents on disk (cannot be undone)",
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel,
                    QtWidgets.QMessageBox.Yes
                )
                question.setDetailedText("Project location:\n%s" % node.path())
                ret = question.exec_()
                if ret == QtWidgets.QMessageBox.Yes:
                    projects.append((node, question.isChecked()))
                elif ret == QtWidgets.QMessageBox.Cancel:
                    return
            else:
                paths.append(node)
        
        # TODO Que pasa con los proyectos y si un path es subpath de otro?
        for node in paths:
            self.deletePath(node.path())
        for index in indexes:
            self.projectTreeProxyModel.refresh(index.parent())

    @QtCore.Slot()
    def on_actionRemove_triggered(self):
        node = self.currentNode()
        if node.isproject:
            ret = QtWidgets.QMessageBox.question(self,
                "Remove project",
                "Are you sure you want to remove project '%s' from the workspace?" % node.name,
                QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel,
                QtWidgets.QMessageBox.Ok
            )
            if ret == QtWidgets.QMessageBox.Ok:
                self.application().projectManager.removeProject(node)

    @QtCore.Slot()
    def on_actionRename_triggered(self):
        self.renamePath(self.currentPath())
        self.projectTreeProxyModel.refresh(self.treeViewProjects.currentIndex())

    @QtCore.Slot()
    def on_actionCloseProject_triggered(self):
        treeNode = self.currentNode()
        if treeNode.isproject:
            self.application().projectManager.closeProject(treeNode)
    
    @QtCore.Slot()
    def on_actionOpenProject_triggered(self):
        treeNode = self.currentNode()
        if treeNode.isproject:
            self.application().projectManager.openProject(treeNode)
    
    @QtCore.Slot()
    def on_actionProperties_triggered(self):
        self.propertiesDialog.setModel(self.application().projectManager.propertiesProxyModel)
        self.propertiesDialog.exec_(self.currentNode())

    @QtCore.Slot()
    def on_actionRefresh_triggered(self):
        indexes = self.treeViewProjects.selectedIndexes()
        for index in indexes:
            self.projectTreeProxyModel.refresh(index)

    @QtCore.Slot()
    def on_actionOpen_triggered(self):
        node = self.currentNode()
        if node.isfile:
            self.application().openFile(node.path())
        
    @QtCore.Slot()
    def on_actionOpenSystemEditor_triggered(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("file://%s" % self.currentPath(), QtCore.QUrl.TolerantMode))
    
    @QtCore.Slot()
    def on_pushButtonCollapseAll_pressed(self):
        self.treeViewProjects.collapseAll()

    @QtCore.Slot(bool)
    def on_pushButtonSync_toggled(self, checked):
        if checked:
            #Conectar señal
            self.window().editorChanged.connect(self.on_window_editorChanged)
            self.on_window_editorChanged(self.window().currentEditor())
        else:
            #Desconectar señal
            self.window().editorChanged.disconnect(self.on_window_editorChanged)
    
    def on_window_editorChanged(self, editor):
        if editor is not None and editor.hasFile():
            index = self.projectTreeProxyModel.indexForPath(editor.filePath())
            self.treeViewProjects.setCurrentIndex(index)

    @QtCore.Slot()
    def on_actionProjectBundles_triggered(self):
        self.bundleEditorDialog.execEditor(namespaceFilter = self.currentNode().namespaceName)
    
    @QtCore.Slot()
    def on_actionSelectRelatedBundles_triggered(self):
        project = self.currentNode()
        self.projectManager.projectMenuProxyModel.setCurrentProject(project)
        self.bundleFilterDialog.exec_()
        
    @QtCore.Slot()
    def on_actionCopy_triggered(self):
        mimeData = self.projectTreeProxyModel.mimeData( self.treeViewProjects.selectedIndexes() )
        self.application().clipboard().setMimeData(mimeData)
        
    @QtCore.Slot()
    def on_actionCut_triggered(self):
        mimeData = self.projectTreeProxyModel.mimeData( self.treeViewProjects.selectedIndexes() )
        self.application().clipboard().setMimeData(mimeData)
        
    @QtCore.Slot()
    def on_actionPaste_triggered(self):
        parentPath = self.currentPath()
        mimeData = self.application().clipboard().mimeData()
        if mimeData.hasUrls() and os.path.isdir(parentPath):
            for url in mimeData.urls():
                srcPath = url.toLocalFile()
                basename = self.application().fileManager.basename(srcPath)
                dstPath = os.path.join(parentPath, basename)
                while self.application().fileManager.exists(dstPath):
                    basename, ret = ReplaceRenameInputDialog.getText(self, _("Already exists"), 
                        _("Destiny already exists\nReplace or or replace?"), text = basename, )
                    if ret == ReplaceRenameInputDialog.Cancel: return
                    if ret == ReplaceRenameInputDialog.Replace: break
                    dstPath = os.path.join(parentPath, basename)
                if os.path.isdir(srcPath):
                    self.application().fileManager.copytree(srcPath, dstPath)
                else:
                    self.application().fileManager.copy(srcPath, dstPath)
            self.projectTreeProxyModel.refresh(self.treeViewProjects.currentIndex())

    @QtCore.Slot()
    def on_actionGoDown_triggered(self):
        self.treeViewProjects.setRootIndex(self.treeViewProjects.currentIndex())
    
    #================================================
    # Navigation
    #================================================
    @QtCore.Slot()
    def on_pushButtonGoUp_pressed(self):
        index = self.projectTreeProxyModel.parent(
            self.treeViewProjects.rootIndex()
        )
        self.treeViewProjects.setRootIndex(index)
    
    #================================================
    # Custom filters
    #================================================
    @QtCore.Slot()
    def on_pushButtonCustomFilters_pressed(self):
        filters, accepted = QtWidgets.QInputDialog.getText(self, _("Custom Filter"), 
                                _("Enter the filters (separated by comma)\nOnly * and ? may be used for custom matching"), 
                                text = self.customFilters)
        if accepted:
            #Save and set filters
            self._settings.setValue('customFilters', filters)
            self.projectTreeProxyModel.setFilterRegExp(filters)
            
    #================================================
    # Sort and order Actions
    #================================================      
    @QtCore.Slot()
    def on_actionOrderByName_triggered(self):
        self.projectTreeProxyModel.sortBy("name", self.actionOrderFoldersFirst.isChecked(), self.actionOrderDescending.isChecked())
    
    @QtCore.Slot()
    def on_actionOrderBySize_triggered(self):
        self.projectTreeProxyModel.sortBy("size", self.actionOrderFoldersFirst.isChecked(), self.actionOrderDescending.isChecked())
    
    @QtCore.Slot()
    def on_actionOrderByDate_triggered(self):
        self.projectTreeProxyModel.sortBy("date", self.actionOrderFoldersFirst.isChecked(), self.actionOrderDescending.isChecked())
    
    @QtCore.Slot()
    def on_actionOrderByType_triggered(self):
        self.projectTreeProxyModel.sortBy("type", self.actionOrderFoldersFirst.isChecked(), self.actionOrderDescending.isChecked())
    
    @QtCore.Slot()
    def on_actionOrderDescending_triggered(self):
        self.projectTreeProxyModel.sortBy(self.projectTreeProxyModel.orderBy, self.actionOrderFoldersFirst.isChecked(), self.actionOrderDescending.isChecked())
    
    @QtCore.Slot()
    def on_actionOrderFoldersFirst_triggered(self):
        self.projectTreeProxyModel.sortBy(self.projectTreeProxyModel.orderBy, self.actionOrderFoldersFirst.isChecked(), self.actionOrderDescending.isChecked())

    #================================================
    # Helper actions
    #================================================
    def refresh(self):
        self.on_actionRefresh_triggered()
        
    def copy(self, checked=False):
        self.on_actionCopy_triggered()
        
    def paste(self, checked=False):
        self.on_actionPaste_triggered()
        
    def cut(self, checked=False):
        self.on_actionCut_triggereda()

    def delete(self, checked=False):
        self.on_actionDelete_triggered()
        
    def rename(self):
        self.on_actionRefresh_triggered()
