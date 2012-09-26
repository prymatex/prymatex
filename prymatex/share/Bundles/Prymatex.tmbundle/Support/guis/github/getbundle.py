#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os, json, sys
import urllib2, httplib2
from urlparse import urlsplit

# Third parties
from PyQt4 import QtGui, QtCore

from prymatex.core.plugin.dialog import PMXBaseDialog

# UI
from ui_githubclient import Ui_GitHubClientDialog

GITHUB_API_SEARCH_URL = 'https://api.github.com/legacy/repos/search/%s+tmbundle'
GITHUB_CLONE_URL = 'https://github.com/{username}/{name}.git'

class RepositoryTableModel(QtCore.QAbstractTableModel):
    HEADER_NAMES = ["Name", "User", "Watchers"]
    def __init__(self, parent = None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.repositories = []
        
    def rowCount(self, parent = None):
        return len(self.repositories)
    
    def columnCount(self, parent = None):
        return len(self.HEADER_NAMES)
        
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.HEADER_NAMES[section]
    
    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid(): 
            return None
        repository = self.repositories[ index.row() ]
        
        if role == QtCore.Qt.CheckStateRole and index.column() == 0:
            return QtCore.Qt.Checked if repository['checked'] else QtCore.Qt.Unchecked
        elif role in [ QtCore.Qt.DisplayRole, QtCore.Qt.EditRole ]:
            if index.column() == 0:
                return repository['name']
            elif index.column() == 1:
                return repository['username']
            elif index.column() == 2:
                return repository['watchers']

    def setData(self, index, value, role):
        """Retornar verdadero si se puedo hacer el cambio, falso en caso contrario"""

        if not index.isValid(): return False
        repository = self.repositories[ index.row() ]
        
        if role == QtCore.Qt.CheckStateRole:
            repository['checked'] = value
            self.dataChanged.emit(index, index)
            return True
        return False
    
    def hasSelected(self):
        return bool(self.allSelected())
        
    def allSelected(self):
        return filter(lambda repo: repo["checked"], self.repositories)
        
    def clearUnselected(self):
        self.repositories = filter(lambda repo: repo["checked"], self.repositories)
        self.layoutChanged.emit()
        
    def addRepositories(self, repositories):
        for repo in repositories:
            repo['checked'] = False
            if repo["name"].endswith(".tmbundle") or repo["name"].endswith("-tmbundle"):
                basename = "%s.tmbundle" % repo["name"][0:-9]
            else:
                basename = "%s.tmbundle" % repo["name"]
            repo['folder'] = basename
            repo.setdefault('destiny', '')
            repo.setdefault('homepage', '')
            repo.setdefault('url', '')
        self.repositories += repositories
        self.layoutChanged.emit()
    
    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable
        
class GitHubSearchBundleThread(QtCore.QThread):
    recordsFound = QtCore.pyqtSignal(object)
    requestError = QtCore.pyqtSignal(str)
    term = None
    
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
            proxy = httplib2.ProxyInfo(proxy_type = httplib2.socks.PROXY_TYPE_HTTP,
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
                headers, response = self.http.request(GITHUB_API_SEARCH_URL % self.term)
                data = json.loads(response)
                self.recordsFound.emit(data) # Thread safety
            except Exception as e:
                print e
                self.requestError.emit(str(e))
    

class GitHubBundlesDialog(QtGui.QDialog, Ui_GitHubClientDialog, PMXBaseDialog):
    
    MINIMUM_QUERY_LENGTH = 1
    
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        PMXBaseDialog.__init__(self)
        self.setupUi(self)
        
        self.currentRepository = None
        self.workerThread = GitHubSearchBundleThread(self)
        self.buttonSearch.setEnabled(False)
        self.buttonOk.setEnabled(False)
        self.widgetInfo.setVisible(False)
        self.model = RepositoryTableModel(self)
        self.proxy = QtGui.QSortFilterProxyModel()
        self.proxy.setSourceModel(self.model)
        
        self.workerThread.recordsFound.connect(self.on_workerThread_recordsFound)
        self.model.dataChanged.connect(self.on_model_dataChanged)
        
        self.tableViewResults.setModel(self.proxy)
        self.tableViewResults.verticalHeader().hide()
        self.tableViewResults.horizontalHeader().setSortIndicatorShown(True)
        self.tableViewResults.horizontalHeader().setClickable(True)
        self.loadComboBoxNamespace()
        
    def loadComboBoxNamespace(self):
        for ns in self.application.supportManager.nsorder:
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
        self.labelDestiny.setText(repo["destiny"])
        self.labelUrl.setText(repo["url"])
        
    # =======================
    # = Señales de busqueda =
    # =======================
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
    
    # ================================
    # = Señales que arman el destiny =
    # ================================
    @QtCore.pyqtSlot(str)
    def on_comboBoxNamespace_activated(self, namespace):
        basePath = self.application.supportManager.basePath("Bundles", namespace)
        self.currentRepository["destiny"] = os.path.join(basePath, self.currentRepository["folder"])
        self.setCurrentRepository(self.currentRepository)
    
    def on_lineEditFolder_editingFinished(self):
        self.currentRepository["folder"] = self.lineEditFolder.text()
        basePath = self.application.supportManager.basePath("Bundles", self.comboBoxNamespace.currentText())
        self.currentRepository["destiny"] = os.path.join(basePath, self.currentRepository["folder"])
        self.setCurrentRepository(self.currentRepository)
    
    # ======================
    # = Señales del modelo =
    # ======================
    def on_model_dataChanged(self, index):
        repo = self.model.repositories[index.row()]
        if repo["checked"]:
            namespace = self.comboBoxNamespace.currentText()
            basePath = self.application.supportManager.basePath("Bundles", namespace)
            repo["url"] = GITHUB_CLONE_URL.format(**repo)
            repo["destiny"] = os.path.join(basePath, repo["folder"])
        else:
            repo["url"] = ""
            repo["destiny"] = ""
        self.buttonOk.setEnabled(self.model.hasSelected())
        self.setCurrentRepository(repo)
        
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
        self.tableViewResults.resizeColumnsToContents()
        self.tableViewResults.resizeRowsToContents()
        self.tableViewResults.setEnabled(True)
    
    def retrivalError(self, reason):
        self.tableViewResults.setEnabled(True)
        QtGui.QMessageBox.critical(self, _("Query Error"), "An error occurred<br><pre>%s</pre>" % reason)
    
    def on_buttonOk_pressed(self):
        repos = self.model.allSelected()
        for repo in repos:
            print repo
            #process = QtCore.QProcess(self)
            #process.setWorkingDirectory(dstPath)
            #process.finished[int].connect(self.on_processClone_finished)
            #process.start("git clone %s %s.tmbundle" % (repoUrl, bundleName), QtCore.QIODevice.ReadOnly)

    def on_buttonCancel_pressed(self):
        self.close()
        
    def on_processClone_finished(self, value):
        def showMessages(text):
            print text
        self.application.supportManager.reloadSupport(showMessages)
        
if __name__ == '__main__':
    app = QtGui.QApplication([])
    win = GitHubBundlesDialog()
    win.show()
    sys.exit(app.exec_())
