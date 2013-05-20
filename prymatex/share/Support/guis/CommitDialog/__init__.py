#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import sys

from prymatex.qt import QtGui, QtCore
from prymatex.qt.helpers.menus import create_menu

from prymatex.core import PMXBaseDialog

from prymatex.core.settings import pmxConfigPorperty

from .ui_commit import Ui_CommitDialog
from .model import FilesTableModel

class CommitDialog(QtGui.QDialog, Ui_CommitDialog, PMXBaseDialog):
    lastCommitSummary = pmxConfigPorperty(default=[])
    
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        PMXBaseDialog.__init__(self)
        self.setupUi(self)
        self.filesTableModel = FilesTableModel(self)
        self.tableViewFiles.setModel(self.filesTableModel)
        self.tableViewFiles.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableViewFiles.customContextMenuRequested.connect(self.showTableViewFilesContextMenu)
        self.tableViewFiles.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableViewFiles.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.Stretch)
        
        #Setup Context Menu
        selectMenu = { 
            "title": "Select Menu",
            "items": [
                {   'text': 'Choose All',
                    'callback': lambda dialog: dialog.chooseAll(),
                },
                {   'text': 'Choose None',
                    'callback': lambda dialog: dialog.chooseNone(),
                },
                {   'text': 'Revert to Default Choices',
                    'callback': lambda dialog: dialog.revertChoices(),
                },
            ]
        }
        
        self.selectMenu, _ = create_menu(self, selectMenu, connectActions = True)
        self.toolButtonSelect.setMenu(self.selectMenu)
        
    def chooseAll(self):
        print("chooseAll")
        
    def chooseNone(self):
        print("chooseNone")
        
    def revertChoices(self):
        print("revertChoices")
        
    def initialize(self, mainWindow):
        self.lastCommitSummary = self.lastCommitSummary[:10]
        self.comboBoxSummary.addItem("Previous Summaries")
        for summary in self.lastCommitSummary:
            self.comboBoxSummary.addItem("%s ..." % " ".join(summary.split()[:8]))

    @QtCore.Slot(int)
    def on_comboBoxSummary_activated(self, index):
        index -= 1
        if index < len(self.lastCommitSummary):
            self.textEditSummary.setPlainText(self.lastCommitSummary[index])
            self.comboBoxSummary.setCurrentIndex(0)
            
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
            self.filesTableModel.setFiles([{'path': f_s[0], 'status': f_s[1], 'checked': f_s[1] != "?"} for f_s in zip(filePaths, fileStatus)])
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
            message = self.textEditSummary.toPlainText()
            args.append("'%s'" % message)
            if message not in self.lastCommitSummary:
                self.lastCommitSummary.insert(0, message)
                self.settings.setValue("lastCommitSummary", self.lastCommitSummary)
            args.append(" ".join(self.filesTableModel.selectedFiles()))
            return " ".join(args)
        return 'cancel'
        
dialogClass = CommitDialog

if __name__ == '__main__':
    app = QtGui.QApplication([])
    win = dialogClass()
    win.setParameters({"title": "Commit", "files": "uno dos tres", "status": "M:?:A"})
    print(win.execModal())
    sys.exit(app.exec_())
