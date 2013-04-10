#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import fnmatch
import os

from prymatex.qt import QtCore, QtGui
from prymatex import resources

from prymatex.utils import text as texttools
from prymatex.models.selectable import SelectableModelMixin

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
            return resources.getIcon(item["path"])
        elif role == QtCore.Qt.ToolTipRole:
            return None


    def item(self, index):
        return self.__files[index.row()]["path"]


    def setFilterString(self, string):
        self.projectFileTask.cancel()
        self.__files = []
        self.layoutChanged.emit()
        self.projectFileTask = self.projectManager.application.scheduler.newTask(self.__run_project_search(string))


    def __run_file_filter(self, rootDirectory, filenames, pattern):
        for filename in filenames:
            if not self.fileManager.fnmatchany(filename, self.__baseFilters):
                path = os.path.join(rootDirectory, filename)
                if self.fileManager.fnmatch(filename, "*%s*" % pattern):
                    # TODO Recuperar cuanto es y ponerlo en strong
                    count = len(self.__files)
                    self.beginInsertRows(QtCore.QModelIndex(), count, count + 1)
                    self.__files.append(
                        dict(name = filename,
                          path = path ) )
                    self.endInsertRows()
            yield


    def __run_file_search(self, path, pattern):
        for root, dirnames, filenames in os.walk(path):
            yield self.__run_file_filter(root, filenames, pattern)

        
    def __run_project_search(self, pattern):
        for project in self.projectManager.getAllProjects():
            yield self.__run_file_search(project.path(), pattern)
