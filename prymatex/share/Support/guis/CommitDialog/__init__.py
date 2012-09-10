#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from prymatex.core.plugin.dialog import PMXBaseDialog

from CommitDialog.ui_commit import Ui_CommitDialog
from CommitDialog.model import FilesTableModel

class CommitDialog(QtGui.QDialog, Ui_CommitDialog, PMXBaseDialog):
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        PMXBaseDialog.__init__(self)
        self.setupUi(self)
        self.filesTableModel = FilesTableModel(self)
        self.tableViewFiles.setModel(self.filesTableModel)
        self.tableViewFiles.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableViewFiles.customContextMenuRequested.connect(self.showTableViewFilesContextMenu)
        self.tableViewFiles.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        
    def showTableViewFilesContextMenu(self, point):
        index = self.tableViewFiles.indexAt(point)
        if index.isValid():
            # TODO Obtener el item y armar el menu
            menu = QtGui.QMenu(self)
            for action in self.actions:
                menu.addAction(action["name"])
            menu.popup(self.tableViewFiles.mapToGlobal(point))
        
    def setParameters(self, parameters):
        filePaths = []
        fileStatus = []
        self.actions = []
        print parameters
        if "title" in parameters:
            self.setWindowTitle(parameters["title"])
        if "files" in parameters:
            filePaths = parameters["files"].split()
        if "status" in parameters:
            fileStatus = parameters["status"].split(":")
        if "diff-cmd" in parameters:
            cmd, args = parameters["diff-cmd"].split(',')
            self.actions.append({ 'name': 'Diff', 'command': cmd, 'args': args, 'status': [] })
        if "action-cmd" in parameters:
            for command in parameters["action-cmd"]:
                status, action = command.split(':')
                name, cmd, args = action.split(',')
                self.actions.append({ 'name': name, 'command': cmd, 'args': args, 'status': status.split(",")})
        if len(filePaths) == len(fileStatus):
            self.filesTableModel.setFiles(map(lambda (f, s): {'path': f, 'status': s, 'checked': s != "?"}, zip(filePaths, fileStatus)))
            self.tableViewFiles.resizeColumnsToContents()
            self.tableViewFiles.resizeRowsToContents()
    
    def on_buttonOk_pressed(self):
        self.accept()

    def on_buttonCancel_pressed(self):
        self.close()
    
    def execModal(self):
        code = self.exec_()
        if code == QtGui.QDialog.Accepted:
            args = [ "dylan" ]
            args.append("'%s'" % self.textEditSummary.toPlainText())
            return " ".join(args)
        return ''
        
dialogClass = CommitDialog