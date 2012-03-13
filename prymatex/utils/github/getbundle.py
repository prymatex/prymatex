
from PyQt4 import QtGui, QtCore
import sys
from ui_githubclient import Ui_GithubClient
import requests
import json
from operator import itemgetter

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
    term = None
    REQUEST_URL = 'http://github.com/api/v2/json/repos/search/%s+tmbundle'
    def run(self):
        if self.term:
            r = requests.request('GET', self.REQUEST_URL % self.term)
            data = json.loads(r.text)
            self.recordsFound.emit(data) # Thread safety
    

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
if __name__ == '__main__':
    app = QtGui.QApplication([])
    win = PMXGithubBundlesWidget()
    win.show()
    sys.exit(app.exec_())
