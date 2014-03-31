#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import fnmatch
import os

from prymatex.qt import QtCore, QtGui
from prymatex import resources
from prymatex.utils import text

from prymatex.models.selectable import SelectableProxyModel, SelectableModelMixin

#====================================================
# Go to file
#====================================================
class SelectableProjectFileModel(QtCore.QAbstractListModel, SelectableModelMixin):
    def __init__(self, projectManager, fileManager, parent = None): 
        QtCore.QAbstractListModel.__init__(self, parent)
        self.fileManager = fileManager
        self.projectManager = projectManager
        self.projectFileTask = self.projectManager.application.schedulerManager.idleTask()
        self.__files = []
        self.__baseFilters = []

    def initialize(self, selector):
        SelectableModelMixin.initialize(self, selector)
        selector.finished.connect(self.on_selector_finished)
        self.projectFileTask = self.projectManager.application.schedulerManager.newTask(self.__run_project_search())

    def setBaseFilters(self, baseFilters):
        self.__baseFilters = baseFilters

    def isFilterable(self):
        return True

    def on_selector_finished(self, result):
        self.projectFileTask.cancel()
        self.selector.finished.disconnect(self.on_selector_finished)
        
    def rowCount(self, parent = None):
        return len(self.__files)

    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        item = self.__files[index.row()]
        if role == QtCore.Qt.DisplayRole:
            return "<table><tr><td><h4>%(name)s</h4></td></tr><tr><td><small>%(path)s</small></td></tr></table>" % item
        elif role == QtCore.Qt.DecorationRole:
            return resources.get_icon(item["path"])
        elif role == QtCore.Qt.ToolTipRole:
            return None

    def item(self, index):
        if index < len(self.__files):
            return self.__files[index]["path"]

    # --------- Tasks
    def __run_file_filter(self, rootDirectory, filenames):
        for filename in filenames:
            if not self.fileManager.fnmatchany(filename, self.__baseFilters):
                self.beginInsertRows(QtCore.QModelIndex(), len(self.__files), len(self.__files) + 1)
                self.__files.append({ "name": filename,
                        "path": os.path.join(rootDirectory, filename) })
                self.endInsertRows()
            yield

    def __run_file_search(self, path):
        for root, dirnames, filenames in os.walk(path):
            yield self.__run_file_filter(root, filenames)
        
    def __run_project_search(self):
        for project in self.projectManager.getAllProjects():
            yield self.__run_file_search(project.path())

class SelectableProjectFileProxyModel(SelectableProxyModel):
    def __init__(self, projectManager, fileManager, parent = None):
        SelectableProxyModel.__init__(self, parent)
        self.setSourceModel(SelectableProjectFileModel(projectManager, fileManager, parent))
        self.setFilterFunction(lambda pattern, path: bool(path) and text.fuzzy_match(pattern, path))

    def setBaseFilters(self, baseFilters):
        self.sourceModel().setBaseFilters(baseFilters)
