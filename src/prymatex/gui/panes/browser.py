from PyQt4.QtCore import QObject, pyqtSignature, pyqtProperty
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

from prymatex.gui.panes import PaneDockBase
from prymatex.gui.panes.ui_browser import Ui_BrowserPane
from prymatex.core.base import PMXObject
from prymatex.core.config import Setting

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
TextMate.system = function(command) {
    alert(command);
    var ok = this._system(command);
    if (ok) return _systemWrapper;
}
"""

class NetworkAccessManager(QNetworkAccessManager, PMXObject):
    def __init__(self, parent, old_manager):
        super(NetworkAccessManager, self).__init__(parent)
        self.old_manager = old_manager
        self.setCache(old_manager.cache())
        self.setCookieJar(old_manager.cookieJar())
        self.setProxy(old_manager.proxy())
        self.setProxyFactory(old_manager.proxyFactory())
    
    def createRequest(self, operation, request, data):
        print operation
        print request
        print data
        if request.url().scheme() == "txmt":
            self.mainwindow.openUrl(request.url())
        return QNetworkAccessManager.createRequest(self, operation, request, data)

class SystemWrapper(QObject):
    def __init__(self, process):
        QObject.__init__(self)
        self.process = process
    
    @pyqtSignature("write(int)")
    def write(self, flags):
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
        self.mainFrame.addToJavaScriptWindowObject("_systemWrapper", SystemWrapper(''))
        return True
    
    def isBusy(self):
        return False
    readAll = pyqtProperty("bool", isBusy)
    
class PMXBrowserPaneDock(PaneDockBase, Ui_BrowserPane, PMXObject):
    geometry = Setting()
    
    def __init__(self, parent):
        PaneDockBase.__init__(self, parent)
        self.setupUi(self)
        #New manager
        old_manager = self.webView.page().networkAccessManager()
        new_manager = NetworkAccessManager(self, old_manager)
        self.webView.page().setNetworkAccessManager(new_manager)
        self.webView.loadFinished[bool].connect(self.prepareJavaScript)
        self.configure()

    class Meta():
        settings = 'browser'
            
    def prepareJavaScript(self, ready):
        if not ready:
            return
        self.webView.page().mainFrame().addToJavaScriptWindowObject("TextMate", TextMate(self.webView.page().mainFrame()))
        self.webView.page().mainFrame().evaluateJavaScript(js)
    
    def setHtml(self, string):
        self.webView.setHtml(string)
