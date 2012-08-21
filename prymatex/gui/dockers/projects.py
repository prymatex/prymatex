#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import codecs

from PyQt4 import QtCore, QtGui

from prymatex import resources
from prymatex.core.plugin.dock import PMXBaseDock
from prymatex.utils.i18n import ugettext as _
from prymatex.gui.project.models import PMXProjectTreeModel
from prymatex.core.settings import pmxConfigPorperty
from prymatex.gui import utils

from prymatex.gui.dialogs.template import PMXNewFromTemplateDialog
from prymatex.gui.dialogs.project import PMXNewProjectDialog
from prymatex.gui.dialogs.messages import CheckableMessageBox

from prymatex.ui.dockers.projects import Ui_ProjectsDock
from prymatex.gui.dockers.fstasks import PMXFileSystemTasks
from prymatex.gui.project.base import PMXProject


class PMXProjectDock(QtGui.QDockWidget, Ui_ProjectsDock, PMXFileSystemTasks, PMXBaseDock):
    SHORTCUT = "F8"
    ICON = resources.getIcon("project")
    PREFERED_AREA = QtCore.Qt.LeftDockWidgetArea

    #=======================================================================
    # Settings
    #=======================================================================
    SETTINGS_GROUP = 'Projects'
    @pmxConfigPorperty(default = '')
    def customFilters(self, filters):
        self.projectTreeProxyModel.setFilterRegExp(filters)
    
    def __init__(self, parent):
        QtGui.QDockWidget.__init__(self, parent)
        PMXBaseDock.__init__(self)
        self.setupUi(self)
        self.projectManager = self.application.projectManager
        self.projectTreeProxyModel = self.projectManager.projectTreeProxyModel
    
        self.setupPropertiesDialog()
        self.setupTreeViewProjects()
        
    def initialize(self, mainWindow):
        PMXBaseDock.initialize(self, mainWindow)
        #TODO: ver el tema de proveer servicios esta instalacion en la main window es pedorra
        mainWindow.projects = self
    
    def addFileSystemNodeFormater(self, formater):
        self.projectTreeProxyModel.addNodeFormater(formater)
    
    def saveState(self):
        expandedIndexes = filter(lambda index: self.treeViewProjects.isExpanded(index), self.projectTreeProxyModel.persistentIndexList())
        expandedPaths = map(lambda index: self.projectTreeProxyModel.node(index).path, expandedIndexes)
        return { "expanded": expandedPaths }

    def restoreState(self, state):
        #Expanded Nodes
        map(lambda index: index.isValid() and self.treeViewProjects.setExpanded(index, True), 
            map(lambda path: self.projectTreeProxyModel.indexForPath(path), state["expanded"]))

    def keyPressEvent(self, event):
        return QtGui.QDockWidget.keyPressEvent(self, event) 
        
    def setupPropertiesDialog(self):
        from prymatex.gui.dialogs.properties import PMXPropertiesDialog
        from prymatex.gui.project.environment import EnvironmentWidget
        from prymatex.gui.project.resource import PMXResouceWidget
        self.application.populateComponent(PMXPropertiesDialog)
        self.propertiesDialog = PMXPropertiesDialog(self)
        self.application.extendComponent(EnvironmentWidget)
        self.application.extendComponent(PMXResouceWidget)
        self.propertiesDialog.register(EnvironmentWidget(self))
        self.propertiesDialog.register(PMXResouceWidget(self))
        #TODO: Para cada add-on registrar los correspondientes properties

    def setupTreeViewProjects(self):
        self.treeViewProjects.setModel(self.projectTreeProxyModel)
        
        self.treeViewProjects.setHeaderHidden(True)
        self.treeViewProjects.setUniformRowHeights(False)
        
        #Setup Context Menu
        optionsMenu = { 
            "title": "Project Options",
            "items": [
                {   "title": "Order",
                    "items": [
                        (self.actionOrderByName, self.actionOrderBySize, self.actionOrderByDate, self.actionOrderByType),
                        "-", self.actionOrderDescending, self.actionOrderFoldersFirst
                    ]
                }
            ]
        }

        self.actionOrderFoldersFirst.setChecked(True)
        self.actionOrderByName.trigger()
        
        self.projectOptionsMenu, _ = utils.createQMenu(optionsMenu, self)
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

    #================================================
    # Build Menus
    #================================================
    def buildContextMenu(self, index):    
        contextMenu = { 
            "title": "Context",
            "items": [
                {   "title": "New",
                    "items": [
                        self.actionNewFolder, self.actionNewFile, self.actionNewFromTemplate, "-", self.actionNewProject,
                    ]
                },
                "--refresh",
                self.actionRefresh,
            ]
        }
        if index.isValid():
            node = self.projectTreeProxyModel.node(index)
            self.extendFileSystemItemMenu(contextMenu, node)
        # contextMenu, contextMenuActions = utils.createQMenu(contextMenu, self, useSeparatorName = True)
        contextMenu, contextMenuActions = utils.createQMenu(contextMenu, self)
        
        for action in contextMenuActions:
            if hasattr(action, "callback"):
                action.triggered.connect(action.callback)
                
        return contextMenu

    def extendFileSystemItemMenu(self, menu, node):
        utils.extendMenuSection(menu, ["--open", self.actionOpenSystemEditor, "--handlepaths", self.actionDelete, self.actionRename])
        utils.extendMenuSection(menu, ["--interact", self.actionSetInTerminal ], section = -1)
        if isinstance(node, PMXProject):
            utils.extendMenuSection(menu, [self.actionPaste, self.actionRemove], section = "handlepaths", position = 0)
            utils.extendMenuSection(menu, [self.actionCloseProject, self.actionOpenProject], section = "refresh")
            utils.extendMenuSection(menu, [self.actionBashInit, self.actionBundleEditor], section = "interact")
        else:
            utils.extendMenuSection(menu, [self.actionCut, self.actionCopy, self.actionPaste], section = "handlepaths", position = 0)
        if node.isfile:
            utils.extendMenuSection(menu, self.actionOpen, section = "open", position = 0)
            
        #Ahora los addons
        addonMenues = [ "-" ]
        for addon in self.addons:
            addonMenues.extend(addon.contributeToContextMenu(node))
        if len(addonMenues) > 1:
            utils.extendMenuSection(menu, addonMenues, section = -1)
        
        #El final
        utils.extendMenuSection(menu, ["--properties", self.actionProperties], section = -1)

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
        
    #================================================
    # Actions Create, Delete, Rename objects
    #================================================      
    @QtCore.pyqtSlot()
    def on_actionNewFile_triggered(self):
        basePath = self.currentPath()
        self.createFile(basePath)
        #TODO: si esta en auto update ver como hacer los refresh
        self.projectTreeProxyModel.refresh(self.treeViewProjects.currentIndex())
    
    @QtCore.pyqtSlot()
    def on_actionNewFromTemplate_triggered(self):
        basePath = self.currentPath()
        self.createFileFromTemplate(basePath)
        #TODO: si esta en auto update ver como hacer los refresh
        self.projectTreeProxyModel.refresh(self.treeViewProjects.currentIndex())
    
    @QtCore.pyqtSlot()
    def on_actionNewFolder_triggered(self):
        basePath = self.currentPath()
        self.createDirectory(basePath)
        #TODO: si esta en auto update ver como hacer los refresh
        self.projectTreeProxyModel.refresh(self.treeViewProjects.currentIndex())

    @QtCore.pyqtSlot()
    def on_actionNewProject_triggered(self):
        PMXNewProjectDialog.getNewProject(self)
        self.projectTreeProxyModel.refresh(self.treeViewProjects.currentIndex())

    @QtCore.pyqtSlot()
    def on_actionDelete_triggered(self):
        currentIndex = self.treeViewProjects.currentIndex()
        treeNode = self.projectTreeProxyModel.node(currentIndex)
        if treeNode.isproject:
            #Es proyecto
            question = CheckableMessageBox.questionFactory(self,
                "Delete project",
                "Are you sure you want to delete project '%s' from the workspace?" % treeNode.name,
                "Delete project contents on disk (cannot be undone)",
                QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel,
                QtGui.QMessageBox.Ok
            )
            question.setDetailedText("Project location:\n%s" % treeNode.path)
            ret = question.exec_()
            if ret == QtGui.QMessageBox.Ok:
                self.application.projectManager.deleteProject(treeNode, removeFiles = question.isChecked())
        else:
            #Es un path
            self.deletePath(treeNode.path)
        self.projectTreeProxyModel.refresh(currentIndex.parent())

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
        basePath = self.currentPath()
        self.renamePath(basePath)

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
        index = self.treeViewProjects.currentIndex()
        if index.isValid():
            self.projectTreeProxyModel.refresh(index)
        else:
            pass
            #
    
    @QtCore.pyqtSlot()
    def on_actionOpen_triggered(self):
        node = self.currentNode()
        if node.isfile:
            self.application.openFile(node.path)
        
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
    def on_actionSetInTerminal_triggered(self):
        path = self.currentPath()
        directory = self.application.fileManager.getDirectory(path)
        self.mainWindow.terminal.chdir(directory)
        project = self.application.projectManager.findProjectForPath(path)
        if project and project.hasSupport():
            self.mainWindow.terminal.runCommand("source %s" % project.bashInit())
    
    @QtCore.pyqtSlot()
    def on_actionBashInit_triggered(self):
        project = self.currentNode()
        self.application.openFile(project.bashInit())

    @QtCore.pyqtSlot()
    def on_actionBundleEditor_triggered(self):
        project = self.currentNode()
        if project.namespace is None:
            self.application.supportManager.addProjectNamespace(project)
        self.projectManager.projectMenuProxyModel.setCurrentProject(project)
        self.application.bundleEditor.execEditor(namespaceFilter = project.namespace, filterText = "Menu", filterModel = self.projectManager.projectMenuProxyModel)
    
    def on_actionCopy_triggered(self):
        mimeData = self.projectTreeProxyModel.mimeData( [ self.treeViewProjects.currentIndex() ] )
        self.application.clipboard().setMimeData(mimeData)
    
    def on_actionPaste_triggered(self):
        parentPath = self.currentPath()
        mimeData = self.application.clipboard().mimeData()
        if mimeData.hasUrls() and os.path.isdir(parentPath):
            for url in mimeData.urls():
                srcPath = url.toLocalFile()
                dstPath = os.path.join(parentPath, self.application.fileManager.basename(srcPath))
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
