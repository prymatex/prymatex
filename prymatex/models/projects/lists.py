#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import fnmatch
import os

from prymatex.qt import QtCore, QtGui
from prymatex import resources

from prymatex.models.selectable import SelectableModelMixin

#====================================================
# Go to file
#====================================================
class SelectableProjectFileModel(QtCore.QAbstractListModel, SelectableModelMixin):
    def __init__(self, projectManager, fileManager, parent = None): 
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.fileManager = fileManager
        self.projectManager = projectManager
        self.projectFileTask = self.projectManager.application.scheduler.idleTask()
        self.__files = []
        self.__baseFilters = []


    def initialize(self, selector):
        SelectableModelMixin.initialize(self, selector)
        selector.finished.connect(self.on_selector_finished)


    def setBaseFilters(self, baseFilters):
        self.__baseFilters = baseFilters
        
    def isFiltered(self):
        return True


    def on_selector_finished(self, result):
        print "se temino", result
        self.projectFileTask.cancel()
        self.selector.finished.disconnect(self.on_selector_finished)


    def rowCount(self, parent = None):
        return len(self.__files)


    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        item = self.__files[index.row()]
        if role in [ QtCore.Qt.DisplayRole, QtCore.Qt.ToolTipRole ]:
            print item["name"]
            return item["name"]
        elif role == QtCore.Qt.DecorationRole:
            return resources.getIcon(item["path"])

    def item(self, index):
        return self.__files[index.row()]

    def setFilterString(self, string):
        self.projectFileTask.cancel()
        self.__files = []
        self.layoutChanged.emit()
        self.projectFileTask = self.projectManager.application.scheduler.newTask(self.__run_project_search(string))

    def __run_file_filter(self, rootDirectory, filenames, pattern):
        for filename in filenames:
            if not self.fileManager.fnmatchany(filename, self.__baseFilters):
                count = len(self.__files)
                self.beginInsertRows(QtCore.QModelIndex(), count, count + 1)
                self.__files.append(
                    dict(name = filename,
                      path = os.path.join(rootDirectory, filename) ) )
                self.endInsertRows()
            yield

    def __run_file_search(self, path, pattern):
        for root, dirnames, filenames in os.walk(path):
            yield self.__run_file_filter(root, filenames, pattern)
        
    def __run_project_search(self, pattern):
        for project in self.projectManager.getAllProjects():
            yield self.__run_file_search(project.path(), pattern)
