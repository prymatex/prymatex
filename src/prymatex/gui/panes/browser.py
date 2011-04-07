import codecs

from PyQt4.QtCore import QObject, pyqtSignature, pyqtProperty, QTimer, QVariant, SIGNAL
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

from prymatex.gui.panes import PaneDockBase
from prymatex.gui.panes.ui_browser import Ui_BrowserPane
from prymatex.core.base import PMXObject
from prymatex.core.config import pmxConfigPorperty
from prymatex.bundles.utils import ensureShellScript, makeExecutableTempFile, deleteFile, ensureEnvironment
from subprocess import Popen, PIPE, STDOUT

#http://diotavelli.net/PyQtWiki/SampleCode
'''
if 'http_proxy' in os.environ:
    proxy_url = QtCore.QUrl(os.environ['http_proxy'])
    if unicode(proxy_url.scheme()).starstswith('http'):
        protocol = QtNetwork.QNetworkProxy.HttpProxy
    else:
        protocol = QtNetwork.QNetworkProxy.Socks5Proxy
    QtNetwork.QNetworkProxy.setApplicationProxy(
        QtNetwork.QNetworkProxy(
            protocol,
            proxy_url.host(),
            proxy_url.port(),
            proxy_url.userName(),
            proxy_url.password()))
            '''

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
            self.mainwindow.openUrl(request.url())
        elif request.url().scheme() == "tm-file" and operation == self.GetOperation:
            reply = TmFileReply(self, request.url(), self.GetOperation)
            return reply
        return QNetworkAccessManager.createRequest(self, operation, request, data)

js = """
TextMate.system = function(command, callback) {
    this._system(command);
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
        pass
    
    @pyqtSignature("close()")
    def close(self):
        pass

    def outputString(self):
        self.process.stdin.close()
        text = self.process.stdout.read()
        self.process.stdout.close()
        exit_code = self.process.wait()
        deleteFile(self.temp_file)
        return text
    outputString = pyqtProperty("QString", outputString)
    
class TextMate(QObject):
    def __init__(self, mainFrame, bundleItem = None):
        QObject.__init__(self)
        self.mainFrame = mainFrame
        self.bundleItem = bundleItem
        
    @pyqtSignature("_system(QString)")
    def _system(self, command):
        environment = self.bundleItem != None and self.bundleItem.buildEnvironment() or {}
        command = ensureShellScript(unicode(command))
        temp_file = makeExecutableTempFile(command)
        process = Popen([temp_file], stdout=PIPE, stdin=PIPE, stderr=STDOUT, env = ensureEnvironment(environment))
        self.mainFrame.addToJavaScriptWindowObject("_systemWrapper", SystemWrapper(process, temp_file))
    
    def isBusy(self):
        return True
    isBusy = pyqtProperty("bool", isBusy)
    
class PMXBrowserPaneDock(PaneDockBase, Ui_BrowserPane):
    def __init__(self, parent):
        PaneDockBase.__init__(self, parent)
        self.setupUi(self)
        #New manager
        old_manager = self.webView.page().networkAccessManager()
        new_manager = NetworkAccessManager(self, old_manager)
        self.webView.page().setNetworkAccessManager(new_manager)
        self.webView.loadFinished[bool].connect(self.prepareJavaScript)
        self.bundleItem = None
            
    def prepareJavaScript(self, ready):
        if not ready:
            return
        self.webView.page().mainFrame().addToJavaScriptWindowObject("TextMate", TextMate(self.webView.page().mainFrame(), self.bundleItem))
        self.webView.page().mainFrame().evaluateJavaScript(js)
    
    def setHtml(self, string, bundleItem):
        self.bundleItem = bundleItem
        self.webView.setHtml(string)