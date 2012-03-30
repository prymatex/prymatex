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
from prymatex.ui.dockers.projects import Ui_ProjectsDock
from prymatex.gui.dialogs.newfromtemplate import PMXNewFromTemplateDialog
from prymatex.gui.dockers.fstasks import PMXFileSystemTasks
from prymatex.gui.project.base import PMXProject
from prymatex.gui.dialogs.newproject import PMXNewProjectDialog

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
        self.projectTreeProxyModel = self.application.projectManager.projectTreeProxyModel
        self.treeViewProjects.setModel(self.projectTreeProxyModel)
        self.setupPropertiesDialog()
        self.setupTreeViewProjects()

    def initialize(self, mainWindow):
        PMXBaseDock.initialize(self, mainWindow)
        #TODO: ver el tema de proveer servicios esta instalacion en la main window es pedorra
        mainWindow.projects = self
    
    def keyPressEvent(self, event):
        print event
        return QtGui.QDockWidget.keyPressEvent(self, event) 
        
    def setupPropertiesDialog(self):
        from prymatex.gui.dialogs.properties import PMXPropertiesDialog
        from prymatex.gui.project.environment import PMXEnvironmentWidget
        from prymatex.gui.project.resource import PMXResouceWidget
        self.application.populateComponent(PMXPropertiesDialog)
        self.propertiesDialog = PMXPropertiesDialog(self)
        self.application.extendComponent(PMXEnvironmentWidget)
        self.application.extendComponent(PMXResouceWidget)
        self.propertiesDialog.register(PMXEnvironmentWidget(self))
        self.propertiesDialog.register(PMXResouceWidget(self))
        #TODO: Para cada add-on registrar los correspondientes properties

    def setupTreeViewProjects(self):
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

        #=======================================================================
        # Drag and Drop (see the proxy model)
        #=======================================================================
        self.treeViewProjects.setDragEnabled(True)
        self.treeViewProjects.setAcceptDrops(True)
        self.treeViewProjects.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.treeViewProjects.setDropIndicatorShown(True)

        #Connect context menu
        self.treeViewProjects.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeViewProjects.customContextMenuRequested.connect(self.showProjectTreeViewContextMenu)
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
        contextMenu, contextMenuActions = utils.createQMenu(contextMenu, self)
        return contextMenu

    def extendFileSystemItemMenu(self, menu, node):
        utils.extendMenuSection(menu, ["--open", self.actionOpenSystemEditor, "--delete", self.actionDelete])
        utils.extendMenuSection(menu, ["--interact", self.actionSetInTerminal, "--properties", self.actionProperties], section = -1)
        if isinstance(node, PMXProject):
            utils.extendMenuSection(menu, self.actionRemove, section = "delete", position = 0)
            utils.extendMenuSection(menu, [self.actionCloseProject, self.actionOpenProject], section = "refresh")
            utils.extendMenuSection(menu, [self.actionBashInit, self.actionBundleEditor], section = "interact")
        elif node.isfile:
            utils.extendMenuSection(menu, self.actionOpen, section = "open", position = 0)
        elif node.isdir:
            pass

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
        treeNode = self.currentNode()
        if not treeNode.isproject:
            self.deletePath(treeNode.path)
            #TODO: si esta en auto update ver como hacer los refresh
            self.projectTreeProxyModel.refresh(self.projectTreeProxyModel.indexForPath(treeNode.parentNode.path))
        else:
            #Test delete removeFiles
            self.application.projectManager.deleteProject(treeNode, removeFiles = False)
    
    @QtCore.pyqtSlot()
    def on_actionRemove_triggered(self):
        treeNode = self.currentNode()
        if treeNode.isproject:
            self.application.projectManager.removeProject(treeNode)

    @QtCore.pyqtSlot()
    def on_actionRename_triggered(self):
        basePath = self.currentPath()
        self.renamePath(basePath)

    @QtCore.pyqtSlot()
    def on_actionCloseProject_triggered(self):
        path = self.currentPath()
        print(path)
    
    @QtCore.pyqtSlot()
    def on_actionOpenProject_triggered(self):
        print (self.currentPath())
    
    @QtCore.pyqtSlot()
    def on_actionProperties_triggered(self):
        treeNode = self.currentNode()
        self.propertiesDialog.exec_(treeNode)

    @QtCore.pyqtSlot()
    def on_actionRefresh_triggered(self):
        self.projectTreeProxyModel.refresh(self.treeViewProjects.currentIndex())
    
    @QtCore.pyqtSlot()
    def on_actionOpen_triggered(self):
        node = self.currentNode()
        if node.isfile:
            self.application.openFile(node.path)
        
    @QtCore.pyqtSlot()
    def on_actionOpenSystemEditor_triggered(self):
        path = self.currentPath()
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("file://%s" % path, QtCore.QUrl.TolerantMode))
    
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
        if project.hasSupport():
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
        self.application.bundleEditor.execEditor(namespaceFilter = project.namespace)
        
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