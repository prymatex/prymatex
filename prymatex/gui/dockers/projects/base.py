#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import codecs

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.qt.helpers import create_menu
from prymatex.qt.extensions import CheckableMessageBox, ReplaceRenameInputDialog

from prymatex.core import PrymatexDock
from prymatex.core.settings import ConfigurableItem, ConfigurableHook

from prymatex.utils.i18n import ugettext as _
from prymatex.gui.dialogs.bundles.filter import BundleFilterDialog

from prymatex.models.trees import TreeNodeBase
from prymatex.models.projects.lists import SelectableProjectFileProxyModel

from prymatex.ui.dockers.projects import Ui_ProjectsDock

from .actions import ProjectsDockActionsMixin

class ProjectsDock(PrymatexDock, Ui_ProjectsDock, ProjectsDockActionsMixin, QtWidgets.QDockWidget):
    SEQUENCE = ("Docks", "ProjectsDock", "Alt+X")
    ICON = "dock-projects"
    PREFERED_AREA = QtCore.Qt.LeftDockWidgetArea

    # -------------- Settings
    @ConfigurableHook("code_editor.default_theme")
    def default_theme(self, theme_uuid):
        theme = self.application().supportManager.getBundleItem(theme_uuid)
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

    def setupTreeViewProjects(self):
        self.treeViewProjects.setModel(self.projectTreeProxyModel)
        
        self.treeViewProjects.setHeaderHidden(True)
        self.treeViewProjects.setUniformRowHeights(False)
        
        self.setupMenues()

        # Drag and Drop (see the proxy model)
        self.treeViewProjects.setDragEnabled(True)
        self.treeViewProjects.setAcceptDrops(True)
        self.treeViewProjects.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.treeViewProjects.setDropIndicatorShown(True)

        self.treeViewProjects.setAlternatingRowColors(True)
        self.treeViewProjects.setAnimated(True)
        
        # Selection Mode
        self.treeViewProjects.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

    # ---------- OVERRIDE: QWidget.setWindowTitle
    def setWindowTitle(self, node_or_str):
        if isinstance(node_or_str, TreeNodeBase):
            if node_or_str.isRootNode():
                node_or_str = "Projects"
            else:
                node_or_str = "%s (%s)" % (
                    node_or_str.nodeName(), 
                    node_or_str.project().nodeName()
                )
        super(ProjectsDock, self).setWindowTitle(node_or_str)
        
    def on_treeViewProjects_doubleClicked(self, index):
        node = self.projectTreeProxyModel.node(index)
        if node.isFile():
            self.application().openFile(node.path())

    def currentPath(self):
        return self.projectTreeProxyModel.filePath(self.treeViewProjects.currentIndex())

    def currentNode(self):
        return self.projectTreeProxyModel.node(self.treeViewProjects.currentIndex())
        
    def currentDirectory(self):
        return self.application().fileManager.directory(self.currentPath())

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

    def on_window_editorChanged(self, editor):
        if editor.hasFile():
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
 
    # # ---------- SIGNAL: pushButtonGoUp.pressed
    @QtCore.Slot()
    def on_pushButtonGoUp_pressed(self):
        index = self.projectTreeProxyModel.parent(self.treeViewProjects.rootIndex())
        self.treeViewProjects.setRootIndex(index)
        node = self.projectTreeProxyModel.node(index)
        self.setWindowTitle(node)
    
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

