#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import json
import sys
from logging import getLogger
from urlparse import urlsplit
from prymatex.qt import QtGui, QtCore
from prymatex.core import PMXBaseDialog
from ui_githubclient import Ui_GitHubClientDialog
import requests
from model import RepositoryTableModel, RepositoryProxyTableModel

GITHUB_API_SEARCH_URL = 'https://api.github.com/legacy/repos/search/%s+tmbundle'

logger = getLogger(__name__)

class GithubBundleSearchThread(QtCore.QThread):
    # Signals
    dataUpdate = QtCore.pyqtSignal(object)
    # Term to search for
    term = None
    # Proxy configuration (http://docs.python-requests.org/en/latest/user/advanced/#proxies)
    proxy = {}

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

    def run(self):
        if not self.term or self.term < self.parent().MINIMUM_QUERY_LENGTH:
            return
        response = requests.get(GITHUB_API_SEARCH_URL % self.term)
        data = json.loads(response.content)
        self.dataUpdate.emit(data) # Thread safety


    def search(self, term):
        '''Performs a lookup in Github REST API based on term'''
        if self.isRunning():
            raise RuntimeError("A search is alredy being made")
        self.term = term
        self.start()


class GithubBundlesDialog(QtGui.QDialog, Ui_GitHubClientDialog, PMXBaseDialog):
    MINIMUM_QUERY_LENGTH = 1

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        PMXBaseDialog.__init__(self)
        self.setupUi(self)

        self.currentRepository = None

        self.workerThread = GithubBundleSearchThread(self)
        self.model = RepositoryTableModel(self)
        self.proxy = RepositoryProxyTableModel()
        self.proxy.setSourceModel(self.model)

        self.buttonSearch.setEnabled(False)
        self.buttonOk.setEnabled(False)
        self.widgetInfo.setVisible(False)

        self.workerThread.dataUpdate.connect(self.on_workerThread_recordsFound)
        self.model.dataChanged.connect(self.on_model_dataChanged)

        self.setupTableView()
        self.loadComboBoxNamespace()

    def setupTableView(self):
        self.tableViewResults.setModel(self.proxy)
        self.tableViewResults.verticalHeader().hide()
        self.tableViewResults.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableViewResults.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Stretch)
        self.tableViewResults.horizontalHeader().setSortIndicatorShown(True)
        self.tableViewResults.horizontalHeader().setClickable(True)
        
    def loadComboBoxNamespace(self):
        for ns in self.application.supportManager.safeNamespaces:
            self.comboBoxNamespace.addItem(ns)

    def setCurrentRepository(self, repo):
        self.currentRepository = repo
        self.labelDescription.setText(repo["description"])
        self.labelHomepage.setText(repo["homepage"])
        self.labelCreated.setText(repo["created"])
        self.labelPushed.setText(repo["pushed"])
        self.labelWatchers.setText(unicode(repo["watchers"]))
        self.labelFollowers.setText(unicode(repo["followers"]))
        self.labelForks.setText(unicode(repo["forks"]))
        self.lineEditFolder.setText(repo["folder"])
        if repo["namespace"]:
            namespaceBundlePath, _ = self.application.supportManager.namespaceElementPath(repo["namespace"], "Bundles")
            self.labelDestiny.setText(os.path.join(namespaceBundlePath, repo["folder"]))
        else:
            self.labelDestiny.setText("")
        self.labelUrl.setText(repo["url"])

    def reloadSupport(self):
        def showMessages(text):
            print text
        self.application.supportManager.reloadSupport(showMessages)

    # =======================
    # = Señales de busqueda =
    # =======================
    def on_buttonSearch_pressed(self):
        text = self.lineEditQuery.text()
        try:
            self.workerThread.search(text)
        except RuntimeError as e:
            return
        except ValueError:
            return
        else:
            self.tableViewResults.setEnabled(False)

    def on_lineEditQuery_returnPressed(self):
        self.on_buttonSearch_pressed()

    def on_lineEditQuery_textChanged(self):
        self.buttonSearch.setEnabled(len(self.lineEditQuery.text()) >= self.MINIMUM_QUERY_LENGTH)

    # ================================
    # = Señales que arman el destiny =
    # ================================
    @QtCore.pyqtSlot(str)
    def on_comboBoxNamespace_activated(self, namespace):
        self.currentRepository["namespace"] = namespace
        self.setCurrentRepository(self.currentRepository)

    def on_lineEditFolder_editingFinished(self):
        self.currentRepository["folder"] = self.lineEditFolder.text()
        self.setCurrentRepository(self.currentRepository)

    # ======================
    # = Señales del modelo =
    # ======================
    def on_model_dataChanged(self, index):
        repo = self.model.repositories[index.row()]
        if repo["checked"]:
            repo["namespace"] = self.comboBoxNamespace.currentText()
        else:
            repo["namespace"] = None
        self.buttonOk.setEnabled(self.model.hasSelected())

    def on_tableViewResults_activated(self, index):
        self.widgetInfo.setVisible(True)
        repo = self.model.repositories[index.row()]
        self.setCurrentRepository(repo)

    # ======================
    # = Señales del Thread =
    # ======================
    def on_workerThread_recordsFound(self, data):
        self.model.clearUnselected()
        self.model.addRepositories(data["repositories"])
        self.tableViewResults.resizeRowsToContents()
        self.tableViewResults.setEnabled(True)
        self.proxy.sort(0)

    def retrivalError(self, reason):
        self.tableViewResults.setEnabled(True)
        QtGui.QMessageBox.critical(self, _("Query Error"), "An error occurred<br><pre>%s</pre>" % reason)

    def on_buttonOk_pressed(self):
        repos = self.model.allSelected()
        self._processCount = len(repos)
        for repo in repos:
            namespaceBundlePath, _ = self.application.supportManager.namespaceElementPath(repo["namespace"], "Bundles", create=True)
            process = QtCore.QProcess(self)
            process.setWorkingDirectory(namespaceBundlePath)
            process.finished[int].connect(self.on_processClone_finished)
            process.start("git clone %s %s" % (repo["url"], repo["folder"]), QtCore.QIODevice.ReadOnly)

    def on_buttonCancel_pressed(self):
        self.close()

    def on_processClone_finished(self, value):
        self._processCount -= 1
        if not self._processCount:
            self.reloadSupport()
            self.close()

if __name__ == '__main__':
    app = QtGui.QApplication([])
    win = GithubBundlesDialog()
    win.show()
    sys.exit(app.exec_())
