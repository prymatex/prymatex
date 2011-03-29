from PyQt4.QtCore import QTimer, QVariant, SIGNAL
from PyQt4.QtGui import *
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt4.QtWebKit import QWebView

from prymatex.gui.panes import PaneDockBase
from prymatex.gui.panes.ui_browser import Ui_BrowserPane

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

js = """
TextMate.system = fundtion(command) {
    var ok = this._system(command);
    if (ok) return _systemWrapper;
}
"""

class NetworkAccessManager(QNetworkAccessManager):
    def __init__(self, old_manager):
        QNetworkAccessManager.__init__(self)
        self.old_manager = old_manager
        self.setCache(old_manager.cache())
        self.setCookieJar(old_manager.cookieJar())
        self.setProxy(old_manager.proxy())
        self.setProxyFactory(old_manager.proxyFactory())
    
    def createRequest(self, operation, request, data):
        #txmt://open?«arguments»
            #url — the actual file to open (i.e. a file://… URL), if you leave out this argument, the frontmost document is implied.
            #line — line number to go to (one based).
            #column — column number to go to (one based).
        if request.url().scheme() == "txmt":
            print "txmt"
        return QNetworkAccessManager.createRequest(self, operation, request, data)

class SystemWrapper(QObject):
    def __init__(self, process):
        QObject.__init__(self)
        self.process = process
    
    @pyqtSignature("open(int)")
    def open(self, flags):
        pass
    
    @pyqtSignature("close()")
    def close(self):
        pass

class TextMate(QObject):
    def __init__(self, mainFrame):
        QObject.__init__(self)
        self.mainFrame = mainFrame
    
    @pyqtSignature("system(QString)")
    def _system(self, command):
        self.mainFrame.addToJavaScriptWindowObject("_systemWrapper", SystemWrapper(path))
        return True
    
    def isBusy(self):
        return False
    readAll = pyqtProperty("bool", isBusy)
    
class PMXBrowserPaneDock(PaneDockBase, Ui_BrowserPane):
    def __init__(self, parent):
        PaneDockBase.__init__(self, parent)
        self.setupUi(self)
        #New manager
        old_manager = self.webView.page().networkAccessManager()
        new_manager = NetworkAccessManager(old_manager)
        self.webView.page().setNetworkAccessManager(new_manager)
        self.webView.loadFinished[bool].connect(self.prepareJavaScript)
    
    def prepareJavaScript(self, ready):
        if not ready:
            return
        self.webView.page().mainFrame().addToJavaScriptWindowObject("TextMate", TextMate(self.webView.page().mainFrame()))
        self.webView.page().mainFrame().evaluateJavaScript(js)
    
    def setHtml(self, string):
        self.webView.setHtml(string)

