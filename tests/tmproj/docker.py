#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import os
import codecs

from PyQt4 import QtCore, QtGui
    
class PMXConsoleDock(QtGui.QDockWidget):
    def __init__(self, parent):
        QtGui.QDockWidget.__init__(self, parent)
        self.setWindowTitle(_("Project"))
        self.setupProjectTree()

    def setupProjectTree(self):
        self.pojectsTreeView = PMXTreeProjectsView()
        self.prjectsTreeModel = PMXProjectsTreeModel()
        self.pojectsTreeView.setModel(self.prjectsTreeModel)
        self.setWidget(self.pojectsTreeView)

class PMXProjectsTreeView(QtGui.QTreeView):
    def __init__(self):
        QtGui.QTreeView.__init__(self)

        self.header().setHidden(True)
        self.setSelectionMode(QTreeWidget.SingleSelection)
        self.setAnimated(True)

        self._actualProject = None
        self._fileWatcher = QtCore.QFileSystemWatcher()