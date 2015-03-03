#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.qt.helpers import create_menu

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
        menu_options = {
            "text": "Project Options",
            "items": [
                {
                    'text': "Sync with current editor",
                    'checkable': True
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
        elif node.isSourceFolder():
            items.extend(self._source_folder_menu_items([ index ]))
        elif node.isDirectory():
            items.extend(self._directory_menu_items([ index ]))
        elif node.isFile():
            items.extend(self._file_menu_items([ index ]))
        if node.isDirectory() or node.isFile() and not node.isSourceFolder():
            items.extend(["-"] + self._path_menu_items([ index ]))
        if node.childCount() > 0:
            items.extend(["-"] + self._has_children_menu_items(node, [ index ]))
        items.extend(["-"] + self._bundles_menu_items(node, [ index ]))
        items.extend([ "-", {
            'text': "Properties"
        }])
        contextMenu = { 
            'text': "Index context",
            'items': items
        }
        contextMenu, objects = create_menu(self, contextMenu)
        return contextMenu

    def _indexes_context_menu(self, indexes):
        if len(indexes) == 1:
            return self._index_context_menu(indexes[0])

        contextMenu = { 
            'text': "Indexes context",
            'items': [
                {   
                    'text': "Copy"
                },
                {   
                    'text': "Paste"
                }
            ]
        }
        contextMenu, objects = create_menu(self, contextMenu)
        return contextMenu
    
    def _project_menu_items(self, indexes):
        return []
    
    def _source_folder_menu_items(self, indexes):
        return []
            
    def _directory_menu_items(self, indexes):
        return [
            {
                'text': "New Folder",
                'triggered': lambda checked=False, indexes=indexes: [ self.newFolder(index) for index in indexes ]
            },
            {
                'text': "New File",
                'triggered': lambda checked=False, indexes=indexes: [ self.newFile(index) for index in indexes ]
            },
            {
                 'text': "New From Template",
                 'triggered': lambda checked=False, indexes=indexes: [ self.newFromTemplate(index) for index in indexes ]
            }, "-",
            {
                 'text': "Open Folder",
                 'triggered': lambda checked=False, indexes=indexes: [ self.openFolder(index) for index in indexes ]
            },
            {
                 'text': "Open System Editor",
                 'triggered': lambda checked=False, indexes=indexes: [ self.openSystemEditor(index) for index in indexes ]
            }
        ]
    
    def _file_menu_items(self, indexes):
        return [
            {
                 'text': "Open File",
                 'triggered': lambda checked=False, indexes=indexes: [ self.openFile(index) for index in indexes ]
            },
            {
                 'text': "Open System Editor",
                 'triggered': lambda checked=False, indexes=indexes: [ self.openSystemEditor(index) for index in indexes ]
            }
        ]

    def _path_menu_items(self, indexes):
        return [
            {
                'text': "Cut" 
            },
            {
                'text': "Copy" 
            },
            {
                'text': "Paste" 
            },
            {
                'text': "Delete" 
            },
            {
                'text': "Rename" 
            },
        ]

    def _has_children_menu_items(self, node, indexes):
        return [
            {
                 'text': "Go Down",
                 'triggered': lambda checked=False, indexes=indexes: [self.treeViewProjects.setRootIndex(index) for index in indexes]
            },
            {
                 'text': "Refresh",
                 'triggered': lambda checked=False, indexes=indexes: [self.projectTreeProxyModel.refresh(index) for index in indexes]
            }
        ]

    def _addons_menu_item(self, node, indexes):
        #Menu de los addons
        addon_menues = [ "-" ]
        for component in self.components():
            addon_menues.extend(component.contributeToContextMenu(node))
        if len(addon_menues) > 1:
            return addon_menues
        
    def _bundles_menu_items(self, node, indexes):
        #Menu de los bundles relacionados al proyecto
        #Try get all bundles for project bundle definition
        bundles = [self.application().supportManager.getManagedObject(uuid) for uuid in node.project().bundles or []]
        #Filter None bundles
        bundles = [bundle for bundle in bundles if bundle is not None]
        return [
            self.application().supportManager.menuForBundle(bundle) \
            for bundle in sorted(bundles, key=lambda bundle: bundle.name) ]

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

    # Open indexes, files or directories
    def openFolder(self, index):
        node = self.projectTreeProxyModel.node(index)
        self.application().openDirectory(node.path())

    def openFile(self, index):
        node = self.projectTreeProxyModel.node(index)
        self.application().openFile(node.path())

    def openSystemEditor(self, index):
        node = self.projectTreeProxyModel.node(index)
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("file://%s" % node.path(), QtCore.QUrl.TolerantMode))

    def newFile(self, index):
        node = self.projectTreeProxyModel.node(index)
        file_path = self.fileManager.createFileDialog(node.path())
        if file_path is not None:
            self.application().openFile(filePath)
            #TODO: si esta en auto update ver como hacer los refresh
            self.projectTreeProxyModel.refreshPath(node.path())
    
    def newFromTemplate(self, index):
        node = self.projectTreeProxyModel.node(index)
        file_path = self.templateDialog.createFile(fileDirectory = node.path())
        if file_path is not None:
            self.application().openFile(file_path)
            #TODO: si esta en auto update ver como hacer los refresh
            self.projectTreeProxyModel.refreshPath(node.path())
    
    def newFolder(self, index):
        node = self.projectTreeProxyModel.node(index)
        directory_path = self.fileManager.createDirectoryDialog(node.path())
        if directory_path is not None:
            #TODO: si esta en auto update ver como hacer los refresh
            self.projectTreeProxyModel.refreshPath(node.path())
            