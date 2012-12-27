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
class SelectableProjectFileModel(QtCore.QAbstractTableModel, SelectableModelMixin):
    def __init__(self, manager, parent = None): 
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.manager = manager
        self.projectFileTask = self.manager.application.scheduler.idleTask()
        self.data = []
        
    def rowCount (self, parent = None):
        return len(self.data)

    def columnCount(self, parent = None):
        return 1

    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        item = self.data[index.row()]
        if role in [ QtCore.Qt.DisplayRole, QtCore.Qt.ToolTipRole ]:
            return item
        elif role == QtCore.Qt.DecorationRole:
            return resources.getIcon(item)
        
    def mapToSourceRow(self, index):
        return self.data[index.row()]

    def setFilterRegExp(self, regexp):
        if self.projectFileTask.isRunning():
            self.projectFileTask.cancel()
            self.data = []
            self.layoutChanged.emit()
        self.projectFileTask = self.manager.application.scheduler.newTask(self.__run_file_search(regexp.pattern()))

    def __run_file_search(self, pattern):
        # TODO: sub tareas
        for project in self.manager.getAllProjects():
            for root, dirnames, filenames in os.walk(project.path()):
                for filename in fnmatch.filter(filenames, pattern):
                    count = len(self.data)
                    self.beginInsertRows(QtCore.QModelIndex(), count, count + 1)
                    self.data.append(os.path.join(root, filename))
                    self.endInsertRows()
                    yield
                yield
            yield
