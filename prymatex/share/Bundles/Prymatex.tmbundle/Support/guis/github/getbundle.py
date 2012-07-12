#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
from operator import itemgetter
import json
import sys
from urlparse import urlsplit
import urllib2

# Third parties
from PyQt4 import QtGui, QtCore
import httplib2

from prymatex.core.plugin.dialog import PMXBaseDialog

# UI
from ui_githubclient import Ui_GitHubClientDialog

_ = lambda s:s


class PMXGitHubRepoModel(QtGui.QStandardItemModel):
    ROWS = (
            ('name', _('Repo')),
            ('description', _('Description')),
            ('url', _('URL')),
            ('username', _('Username')),
            ('watchers', _('Watchers')),
            ('forks', _('Forks')),
            )
    def __init__(self, parent = None):
        QtGui.QStandardItemModel.__init__(self, 0,len(self.ROWS))
        for n, (name, title) in enumerate(self.ROWS):
            self.setHeaderData(n, QtCore.Qt.Horizontal, title,)
        

class PMXGHSearchBundleThread(QtCore.QThread):
    recordsFound = QtCore.pyqtSignal(object)
    requestError = QtCore.pyqtSignal(str)
    
    term = None
    REQUEST_URL = 'http://github.com/api/v2/json/repos/search/%s+tmbundle'
    
    def __init__(self, parent = None):
        QtCore.QThread.__init__(self, parent)
        self.http = self.buildHttp()
    
    def buildHttp(self):
        ''' Build HTTP instance taking proxy information '''
        # TODO: Use prymatex configuration as first option
        proxy = None
        http_proxy = os.environ.get('http_proxy', os.environ.get('HTTP_PROXY', ''))
        if http_proxy:
            data = urlsplit(http_proxy)
            proxy = httplib2.ProxyInfo(proxy_type=httplib2.socks.PROXY_TYPE_HTTP,
                                       proxy_host = data.hostname,
                                       proxy_port = data.port,
                                       proxy_user = data.username,
                                       proxy_pass = data.password)
        # TODO: Socks
        
        http = httplib2.Http(proxy_info = proxy)
        
        return http
    
    def run(self):
        if self.term:
            try:
                headers, response = self.http.request(self.REQUEST_URL % self.term)
                data = json.loads(response)
                self.recordsFound.emit(data) # Thread safety
            except Exception as e:
                self.requestError.emit(str(e))
    

class GitHubBundlesDialog(QtGui.QDialog, Ui_GitHubClientDialog, PMXBaseDialog):
    
    MINIMUM_QUERY_LENGTH = 1
    
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        PMXBaseDialog.__init__(self)
        self.setupUi(self)
        self.workerThread = PMXGHSearchBundleThread(self)
        self.workerThread.recordsFound.connect(self.updateRecords)
        self.buttonSearch.setEnabled(False)
        self.buttonClone.setEnabled(False)
        self.model = PMXGitHubRepoModel(self)
        self.tableViewResults.setModel(self.model)
        self.tableViewResults.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableViewResults.verticalHeader().hide()
        self.tableViewResults.selectionModel().selectionChanged.connect(self.on_treeView_selectionChanged)
        
    def on_buttonSearch_pressed(self):
        text = self.lineEditQuery.text()
        if len(text) < self.MINIMUM_QUERY_LENGTH or self.workerThread.isRunning():
            return
        self.tableViewResults.setEnabled(False)
        self.workerThread.term = text
        self.workerThread.start()
        
    def on_lineEditQuery_returnPressed(self):
        self.on_buttonSearch_pressed()
        
    def on_lineEditQuery_textChanged(self):    
        self.buttonSearch.setEnabled(len(self.lineEditQuery.text()) >= self.MINIMUM_QUERY_LENGTH)
    
    def on_lineEditBundle_textChanged(self):    
        self.buttonClone.setEnabled(len(self.lineEditQuery.text()) >= self.MINIMUM_QUERY_LENGTH)
    
    def on_treeView_selectionChanged(self, selected, deselected):
        indexes = selected.indexes()
        if indexes:
            index = indexes[0]
            repoName = self.model.item(index.row(), 0).text()
            if repoName.endswith(".tmbundle") or repoName.endswith("-tmbundle"):
                repoName = repoName[0:-9]
            self.lineEditBundle.setText(repoName)
        else:
            self.lineEditBundle.setText("")

    def updateRecords(self, data):
        item_names = map(itemgetter(0), self.model.ROWS)
        self.model.removeRows(0, self.model.rowCount())
        for repo_entry in data.get('repositories', []):
            row = map(lambda name: QtGui.QStandardItem(str(repo_entry.get(name, ''))), item_names)
            self.model.appendRow(row)
        self.tableViewResults.resizeColumnsToContents()
        self.tableViewResults.resizeRowsToContents()
        self.tableViewResults.setEnabled(True)
    
    def retrivalError(self, reason):
        self.tableViewResults.setEnabled(True)
        QtGui.QMessageBox.critical(self, _("Query Error"), "An error occurred<br><pre>%s</pre>" % reason)
    
    def on_buttonClone_pressed(self):
        index = self.tableViewResults.currentIndex()
        if index.isValid():
            dstPath = self.application.supportManager.basePath("Bundles", "user")
            repoUrl = self.model.item(index.row(), 2).text()
            bundleName = self.lineEditBundle.text()
            process = QtCore.QProcess(self)
            process.setWorkingDirectory(dstPath)
            process.finished[int].connect(self.on_processClone_finished)
            process.start("git clone %s %s.tmbundle" % (repoUrl, bundleName), QtCore.QIODevice.ReadOnly)

    def on_processClone_finished(self, value):
        def showMessages(text):
            print text
        self.application.supportManager.reloadSupport(showMessages)
        
if __name__ == '__main__':
    app = QtGui.QApplication([])
    win = PMXGithubBundlesWidget()
    win.show()
    sys.exit(app.exec_())
