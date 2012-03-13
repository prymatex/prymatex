# Stdlib
import os
from operator import itemgetter
import json
import sys
from urlparse import urlsplit

# Third parties
from PyQt4 import QtGui, QtCore
import httplib2

# UI
from ui_githubclient import Ui_GithubClient
from M2Crypto import urllib2

_ = lambda s:s


class PMXGitHubRepoModel(QtGui.QStandardItemModel):
    ROWS = (
            ('name', _('Repo')),
            ('username', _('Username')),
            ('description', _('Description')),
            ('url', _('URL')),
            ('forks', 'Fork Count'),
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
    

class PMXGithubBundlesWidget(QtGui.QWidget, Ui_GithubClient):
    
    MINIMUM_QUERY_LENGTH = 1
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.workerThread = PMXGHSearchBundleThread(self)
        self.workerThread.recordsFound.connect(self.updateRecords)
        self.pushButtonSearch.pressed.connect(self.search)
        self.pushButtonSearch.setEnabled(False)
        self.lineEditQuery.textChanged.connect(self.checkText)
        self.lineEditQuery.returnPressed.connect(self.search)
        self.model = PMXGitHubRepoModel(self)
        self.tableViewResults.setModel(self.model)
        self.tableViewResults.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableViewResults.verticalHeader().hide()
        
    def search(self):
        text = self.lineEditQuery.text()
        if len(text) < self.MINIMUM_QUERY_LENGTH or self.workerThread.isRunning():
            return
        self.tableViewResults.setEnabled(False)
        self.workerThread.term = text
        self.workerThread.start()
        
    def checkText(self):    
        self.pushButtonSearch.setEnabled(len(self.lineEditQuery.text()) >= self.MINIMUM_QUERY_LENGTH)
    
    def updateRecords(self, data):
        item_names = map(itemgetter(0), self.model.ROWS)
        self.model.removeRows(0, self.model.rowCount())
        for repo_entry in data.get('repositories', []):
            row = map(lambda name: QtGui.QStandardItem(repo_entry.get(name, '')), item_names)
            self.model.appendRow(row)
        self.tableViewResults.resizeColumnsToContents()
        self.tableViewResults.resizeRowsToContents()
        self.tableViewResults.setEnabled(True)
    
    def retrivalError(self, reason):
        self.tableViewResults.setEnabled(True)
        QtGui.QMessageBox.critical(self, _("Query Error"), "An error occurred<br><pre>%s</pre>" % reason)
    
    
        
if __name__ == '__main__':
    app = QtGui.QApplication([])
    win = PMXGithubBundlesWidget()
    win.show()
    sys.exit(app.exec_())
