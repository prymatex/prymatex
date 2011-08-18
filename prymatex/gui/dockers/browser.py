#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import os
import codecs

from PyQt4 import QtCore
from PyQt4.QtCore import QObject, pyqtSignature, pyqtProperty, QTimer, QVariant, SIGNAL
from PyQt4.QtCore import Qt, QUrl
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt4.QtNetwork import QNetworkProxy
from prymatex.gui.dockers import PaneDockBase
from prymatex.ui.panebrowser import Ui_BrowserPane
from prymatex.core.base import PMXObject
from prymatex.core.config import pmxConfigPorperty
from prymatex.support.utils import ensureShellScript, makeExecutableTempFile, deleteFile, ensureEnvironment
from subprocess import Popen, PIPE, STDOUT
from prymatex.core.config import pmxConfigPorperty

class TmFileReply(QNetworkReply):
    def __init__(self, parent, url, operation):
        super(TmFileReply, self).__init__(parent)
        file = codecs.open(url.path(), 'r', 'utf-8')
        self.content = file.read().encode('utf-8')
        self.offset = 0
        
        self.setHeader(QNetworkRequest.ContentTypeHeader, QVariant("text/html; charset=utf-8"))
        self.setHeader(QNetworkRequest.ContentLengthHeader, QVariant(len(self.content)))
        QTimer.singleShot(0, self, SIGNAL("readyRead()"))
        QTimer.singleShot(0, self, SIGNAL("finished()"))
        self.open(self.ReadOnly | self.Unbuffered)
        self.setUrl(url)
    
    def abort(self):
        pass
    
    def bytesAvailable(self):
        return len(self.content) - self.offset
    
    def isSequential(self):
        return True
    
    def readData(self, maxSize):
        if self.offset < len(self.content):
            end = min(self.offset + maxSize, len(self.content))
            data = self.content[self.offset:end]
            self.offset = end
            return data

class NetworkAccessManager(QNetworkAccessManager, PMXObject):
    def __init__(self, parent, old_manager):
        super(NetworkAccessManager, self).__init__(parent)
        self.old_manager = old_manager
        self.setCache(old_manager.cache())
        self.setCookieJar(old_manager.cookieJar())
        self.setProxy(old_manager.proxy())
        self.setProxyFactory(old_manager.proxyFactory())
    
    def createRequest(self, operation, request, data):
        if request.url().scheme() == "txmt":
            self.mainWindow.openUrl(request.url())
        elif request.url().scheme() == "tm-file" and operation == self.GetOperation:
            reply = TmFileReply(self, request.url(), self.GetOperation)
            return reply
        return QNetworkAccessManager.createRequest(self, operation, request, data)

js = """
TextMate.system = function(command, callback) {
    this._system(command);
    if (callback != null) {
        
    }
    return _systemWrapper;
}
"""

class SystemWrapper(QObject):
    def __init__(self, process, temp_file):
        QObject.__init__(self)
        self.process = process
        self.temp_file = temp_file
    
    @pyqtSignature("write(int)")
    def write(self, flags):
        self.process.stdin.write()
    
    @pyqtSignature("write(int)")
    def read(self, flags):
        self.process.stdin.close()
        text = self.process.stdout.read()
        self.process.stdout.close()
        self.process.wait()
        deleteFile(self.temp_file)
        return text
        
    @pyqtSignature("close()")
    def close(self):
        self.process.stdin.close()
        self.process.stdout.close()
        self.process.wait()
        deleteFile(self.temp_file)

    def outputString(self):
        self.process.stdin.close()
        text = self.process.stdout.read()
        self.process.stdout.close()
        self.process.wait()
        deleteFile(self.temp_file)
        return text
    outputString = QtCore.pyqtProperty(str, outputString)
    
class TextMate(QObject):
    def __init__(self, mainFrame, bundleItem = None):
        QObject.__init__(self)
        self.mainFrame = mainFrame
        self.bundleItem = bundleItem
        
    @QtCore.pyqtSlot(str)
    def _system(self, command):
        environment = self.bundleItem != None and self.bundleItem.buildEnvironment() or {}
        command = ensureShellScript(unicode(command))
        temp_file = makeExecutableTempFile(command)
        process = Popen([temp_file], stdout=PIPE, stdin=PIPE, stderr=STDOUT, env = ensureEnvironment(environment))
        self.mainFrame.addToJavaScriptWindowObject("_systemWrapper", SystemWrapper(process, temp_file))
    
    def isBusy(self):
        return True
    isBusy = pyqtProperty("bool", isBusy)
    
class PMXBrowserPaneDock(PaneDockBase, Ui_BrowserPane, PMXObject):
    class Meta:
        settings = 'browser'
        
    def __init__(self, parent):
        PaneDockBase.__init__(self, parent)
        self.setupUi(self)
        #New manager
        old_manager = self.webView.page().networkAccessManager()
        new_manager = NetworkAccessManager(self, old_manager)
        self.webView.page().setNetworkAccessManager(new_manager)
        self.webView.loadFinished[bool].connect(self.prepareJavaScript)
        self.bundleItem = None
        title = unicode(self.trUtf8("%s (press Esc to close)")) % self.windowTitle()
        self.setWindowTitle(title)
        self.configure()
        
    def prepareJavaScript(self, ready):
        if not ready:
            return
        self.webView.page().mainFrame().addToJavaScriptWindowObject("TextMate", TextMate(self.webView.page().mainFrame(), self.bundleItem))
        self.webView.page().mainFrame().evaluateJavaScript(js)
    
    def setHtml(self, string, bundleItem):
        self.bundleItem = bundleItem
        self.webView.setHtml(string)
    
    def keyPressEvent(self, key_event):
        if key_event.key() == Qt.Key_Escape:
            self.hide()
    
    ENVIROMENT_PROXY = '__ENVIROMENT_PROXY__'
    
    @property
    def env_proxy(self):
        return os.environ.get('http_proxy', '')
    
    @pmxConfigPorperty(default = os.environ.get('http_proxy', ''))
    def proxy(self, value):
        '''
        System wide proxy
        '''
        if value == self.ENVIROMENT_PROXY:
            value = self.env_proxy
        
        proxy_url = QUrl(value)    
        if not value:
            network_proxy = QNetworkProxy(QNetworkProxy.NoProxy)
        else:
            protocol = QNetworkProxy.NoProxy
            if unicode(proxy_url.scheme()).startswith('http'):
                protocol = QNetworkProxy.HttpProxy
            else:
                protocol = QNetworkProxy.Socks5Proxy
                
            network_proxy = QNetworkProxy(
                                        protocol,
                                        proxy_url.host(),
                                        proxy_url.port(),
                                        proxy_url.userName(),
                                        proxy_url.password()
                                        )
                          
        QNetworkProxy.setApplicationProxy( network_proxy )
                                          