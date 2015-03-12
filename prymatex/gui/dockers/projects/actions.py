#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.qt.helpers import create_menu
from prymatex.qt.compat import getExistingDirectory

class ProjectsDockActionsMixin(object):
    def setupMenues(self):
        #Setup Context Menu
        def order_by(attr):
            def _order_by(checked):
                self.projectTreeProxyModel.sortBy(
                    attr, 
                    self.actionFoldersFirst.isChecked(),
                    self.actionDescending.isChecked()
                )
            return _order_by
        def sync_editor(checked):
            if checked:
                #Conectar señal
                self.window().editorChanged.connect(self.on_window_editorChanged)
                self.on_window_editorChanged(self.window().currentEditor())
            else:
                #Desconectar señal
                self.window().editorChanged.disconnect(self.on_window_editorChanged)
        menu_options = {
            "text": "Project Options",
            "items": [
                {
                    'text': "Sync with current editor",
                    'checkable': True,
                    'triggered': sync_editor
                },
                {
                    'text': "Collapse all",
                    'triggered': lambda checked=False: self.treeViewProjects.collapseAll()
                },
                {   "text": "Order",
                    "items": [
                        tuple([{
                            'text': "By %s" % attr,
                            'checkable': True,
                            'triggered': order_by(attr)
                        } for attr in ["name", "size", "date", "type"]
                        ]), "-",
                        {
                            'text': "Descending",
                            'checkable': True,
                            'triggered': order_by(self.projectTreeProxyModel.orderBy)
                        },
                        {
                            'text': "Folders first",
                            'checkable': True,
                            'triggered': order_by(self.projectTreeProxyModel.orderBy)
                        }
                    ]
                }
            ]
        }
        
        self.projectOptionsMenu, objects = create_menu(self, menu_options)
        self.actionByName = [obj for obj in objects if obj.objectName() == 'actionByName'].pop()
        self.actionDescending = [obj for obj in objects if obj.objectName() == 'actionDescending'].pop()
        self.actionFoldersFirst = [obj for obj in objects if obj.objectName() == 'actionFoldersFirst'].pop()
        self.actionByName.setChecked(True)
        self.actionFoldersFirst.trigger()
        self.toolButtonOptions.setMenu(self.projectOptionsMenu)

        #Connect context menu
        self.treeViewProjects.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeViewProjects.customContextMenuRequested.connect(
            self.on_treeViewProjects_customContextMenuRequested)
        
    # -------------- Build context menu
    def _not_index_context_menu(self):
        action_new_project = self.window().findChild(
            QtWidgets.QAction, "actionNewProject"
        )
        action_open_project = self.window().findChild(
            QtWidgets.QAction, "actionOpenProject"
        )
        contextMenu = { 
            'text': "Not index context",
            'items': [ action_new_project, action_open_project ]
        }
        contextMenu, objects = create_menu(self, contextMenu)
        return contextMenu
        
    def _index_context_menu(self, index):
        node = self.projectTreeProxyModel.node(index)
        items = []
        if node.isProject():
            items.extend(self._project_menu_items([ index ]))
        elif node.isDirectory():
            if node.isSourceFolder():
                items.extend(self._source_folder_menu_items([ index ]))
            items.extend(self._directory_menu_items([ index ]))
        elif node.isFile():
            items.extend(self._file_menu_items([ index ]))
        if node.isDirectory() or node.isFile() and not node.isSourceFolder():
            items.extend(self._path_menu_items([ index ]))
        if node.childCount() > 0:
            items.extend(self._has_children_menu_items(node, [ index ]))
        items.extend(self._bundles_menu_items(node, [ index ]))
        items.extend([{
            'text': "Properties"
        }])
        contextMenu = { 
            'text': "Index context",
            'items': items
        }
        contextMenu, objects = create_menu(self, contextMenu)
        return contextMenu

    def _indexes_context_menu(self, indexes):
        indexed_nodes = [(index, self.projectTreeProxyModel.node(index)) \
            for index in indexes]
        items = []
        items.extend(self._project_menu_items(indexed_nodes))
        items.extend(self._source_folder_menu_items(indexed_nodes))
        items.extend(self._directory_menu_items(indexed_nodes))
        items.extend(self._file_menu_items(indexed_nodes))
        items.extend(self._path_menu_items(indexed_nodes))
        items.extend(self._has_children_menu_items(indexed_nodes))
        items.extend(self._bundles_menu_items(indexed_nodes))
        items.extend([{
            'text': "Properties"
        }])
        contextMenu = { 
            'text': "Index context",
            'items': items
        }
        contextMenu, objects = create_menu(self, contextMenu)
        return contextMenu

    def _project_menu_items(self, indexed_nodes):
        items = []
        projects = [ indexed_node for indexed_node in indexed_nodes if \
            indexed_node[1].isProject()]
        if projects:
            items.extend([
                {
                    'text': "Add Source Folder",
                    'triggered': lambda checked=False, values=projects: [ self.addSourceFolder(*value) for value in values ]
                }, {
                    'text': "Project Bundles",
                    'triggered': lambda checked=False, values=projects: [ self.projectBundles(*value) for value in values ]
                }, {
                    'text': "Select Related Bundles ",
                    'triggered': lambda checked=False, values=projects: [ self.selectRelatedBundles(*value) for value in values ]
                }, "-"
            ])
        return items
    
    def _source_folder_menu_items(self, indexed_nodes):
        items = []
        sources = [ indexed_node for indexed_node in indexed_nodes if \
            indexed_node[1].isSourceFolder()]
        if sources:
            items.extend([
                {
                    'text': "Remove Source Folder",
                    'triggered': lambda checked=False, values=sources: [ self.removeSourceFolder(*value) for value in values ]
                }, "-"
            ])
        return items
            
    def _directory_menu_items(self, indexed_nodes):
        items = []
        directories = [ indexed_node for indexed_node in indexed_nodes if \
            indexed_node[1].isDirectory()]
        if directories:
            items.extend([
                {
                    'text': "New Folder",
                    'triggered': lambda checked=False, values=directories: [ self.newFolder(*value) for value in values ]
                },
                {
                    'text': "New File",
                    'triggered': lambda checked=False, values=directories: [ self.newFile(*value) for value in values ]
                },
                {
                     'text': "New From Template",
                     'triggered': lambda checked=False, values=directories: [ self.newFromTemplate(*value) for value in values ]
                }, "-",
                {
                     'text': "Open Folder",
                     'triggered': lambda checked=False, values=directories: [ self.openFolder(*value) for value in values ]
                },
                {
                     'text': "Open System Editor",
                     'triggered': lambda checked=False, values=directories: [ self.openSystemEditor(*value) for value in values ]
                }, "-"
            ])
        return items
    
    def _file_menu_items(self, indexed_nodes):
        items = []
        files = [ indexed_node for indexed_node in indexed_nodes if \
            indexed_node[1].isFile()]
        if files:
            items.extend([
                {
                     'text': "Open File",
                     'triggered': lambda checked=False, values=files: [ self.openFile(*value) for value in values ]
                },
                {
                     'text': "Open System Editor",
                     'triggered': lambda checked=False, values=files: [ self.openSystemEditor(*value) for value in values ]
                }, "-"
            ])
        return items

    def _path_menu_items(self, indexed_nodes):
        items = []
        paths = [ indexed_node for indexed_node in indexed_nodes if \
            indexed_node[1].isDirectory() or indexed_node[1].isFile() and not indexed_node[1].isSourceFolder()]
        if paths:
            items.extend([
                {
                    'text': "Cut",
                    'triggered': lambda checked=False, values=paths: self.cut(values)
                },
                {
                    'text': "Copy",
                    'triggered': lambda checked=False, values=paths: self.copy(values)
                },
                {
                    'text': "Paste",
                    'triggered': lambda checked=False, values=paths: self.paste(values)
                },
                {
                    'text': "Delete",
                    'triggered': lambda checked=False, values=paths: self.delete(values)
                },
                {
                    'text': "Rename",
                    'triggered': lambda checked=False, values=paths: self.rename(values)
                }, "-"
            ])
        return items

    def _has_children_menu_items(self, indexed_nodes):
        items = []
        parents = [ indexed_node for indexed_node in indexed_nodes if \
            indexed_node[1].hasChildren()]
        if parents:
            items.extend([
                {
                     'text': "Go Down",
                     'triggered': lambda checked=False, values=parents: [self.goDown(*value) for value in values]
                },
                {
                     'text': "Refresh",
                     'triggered': lambda checked=False, values=parents: [self.projectTreeProxyModel.refresh(*value) for value in values]
                }, "-"
            ])
        return items

    def _addons_menu_item(self, indexed_nodes):
        # Menu de addons
        addon_menues = [component.contributeToContextMenu(indexed_nodes) for \
            component in self.components()]
        if addon_menues:
            addon_menues.append("-")
        return addon_menues
        
    def _bundles_menu_items(self, indexed_nodes):
        # Menu de bundles relacionados al proyecto
        indexes, nodes = zip(*indexed_nodes)
        bundles = [self.application().supportManager.getManagedObject(uuid) for \
            uuid in nodes[0].project().bundles ]
        #Filter None bundles
        bundles = sorted(filter(lambda bundle: bundle is not None, bundles), 
            key=lambda bundle: bundle.name
        )
        bundle_menues = [self.application().supportManager.menuForBundle(bundle) for \
            bundle in bundles]
        if bundle_menues:
            bundle_menues.append("-")
        return bundle_menues

    # ---------- SIGNAL: treeViewProjects.customContextMenuRequested
    QtCore.Slot(QtCore.QPoint)
    def on_treeViewProjects_customContextMenuRequested(self, point):
        # Aca vamos, esto puede tener multiple seleccion o estar apuntando
        # a un nuevo lugar, hay que identificar el o los indices involucrados
        point_index = self.treeViewProjects.indexAt(point)
        index = point_index.isValid() and point_index or self.treeViewProjects.rootIndex()
        indexes = self.treeViewProjects.selectedIndexes()
        if index.isValid():
            contex_menu = self._indexes_context_menu(indexes)
        else:
            self.treeViewProjects.clearSelection()
            contex_menu = self._not_index_context_menu()

        def about_to_show(app):
            def _about_to_show():
                app.supportManager.setEditorAvailable(False)
                app.supportManager.blockSignals(True)
            return _about_to_show
        contex_menu.aboutToShow.connect(about_to_show(self.application()))

        def about_to_hide(app):
            def _about_to_hide():
                app.supportManager.setEditorAvailable(True)
                def restore_supportManager_signals():
                    app.supportManager.blockSignals(False)
                # TODO No estoy muy contento con esto pero que le vamos a hacer
                QtCore.QTimer.singleShot(0, restore_supportManager_signals)
            return _about_to_hide
        contex_menu.aboutToHide.connect(about_to_hide(self.application()))

        def triggered(window, model, indexes):
            def _triggered(action):
                if hasattr(action, "bundleTreeNode"):
                    for index in indexes:
                        node = model.node(index)
                        env = {   
                            'TM_FILEPATH': node.path(),
                            'TM_FILENAME': node.nodeName(),
                            'TM_DIRECTORY': node.nodeParent().path() 
                        } if node.isFile() else {
                            'TM_DIRECTORY': node.path()
                        }
            
                        env.update(node.project().environmentVariables())
                        window.insertBundleItem(action.bundleTreeNode, environment = env)
            return _triggered
        contex_menu.triggered.connect(triggered(self.window(), self.projectTreeProxyModel, indexes))
        contex_menu.popup(self.treeViewProjects.mapToGlobal(point))

    # --------- Remove and add source Folders
    def removeSourceFolder(self, index, node=None):
        node = node or self.projectTreeProxyModel.node(index)
        project = node.project()
        project.removeSourceFolder(node.path())
        self.projectTreeProxyModel.refresh(index.parent())

    def addSourceFolder(self, index, node=None):
        node = node or self.projectTreeProxyModel.node(index)
        source_folder_path = getExistingDirectory(self, caption="Add Source Folder to %s" % node.nodeName())
        if source_folder_path:
            node.addSourceFolder(source_folder_path)
            self.projectTreeProxyModel.refresh(index)

    # -------------- Project Bundles
    def selectRelatedBundles(self, index, node=None):
        pass
        
    def projectBundles(self, index, node=None):
        pass

    # -------------- Open indexes, files or directories
    def openFolder(self, index, node=None):
        node = node or self.projectTreeProxyModel.node(index)
        self.application().openDirectory(node.path())

    def openFile(self, index, node=None):
        node = node or self.projectTreeProxyModel.node(index)
        self.application().openFile(node.path())

    def openSystemEditor(self, index, node=None):
        node = node or self.projectTreeProxyModel.node(index)
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("file://%s" % node.path(), QtCore.QUrl.TolerantMode))

    def newFile(self, index, node=None):
        node = node or self.projectTreeProxyModel.node(index)
        file_path = self.fileManager.createFileDialog(node.path())
        if file_path is not None:
            self.application().openFile(file_path)
            #TODO: si esta en auto update ver como hacer los refresh
            self.projectTreeProxyModel.refresh(index)
    
    def newFromTemplate(self, index, node=None):
        node = node or self.projectTreeProxyModel.node(index)
        file_path = self.templateDialog.createFile(fileDirectory = node.path())
        if file_path is not None:
            self.application().openFile(file_path)
            #TODO: si esta en auto update ver como hacer los refresh
            self.projectTreeProxyModel.refresh(index)
    
    def newFolder(self, index, node=None):
        node = node or self.projectTreeProxyModel.node(index)
        directory_path = self.fileManager.createDirectoryDialog(node.path())
        if directory_path is not None:
            #TODO: si esta en auto update ver como hacer los refresh
            self.projectTreeProxyModel.refresh(index)

    def goDown(self, index, node=None):
        node = node or self.projectTreeProxyModel.node(index)
        self.setWindowTitle(node)
        self.treeViewProjects.setRootIndex(index)
