#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import os
import codecs
from subprocess import Popen, PIPE, STDOUT

from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt4.QtNetwork import QNetworkProxy

from prymatex import resources
from prymatex.gui.utils import createQMenu
from prymatex.ui.dockers.browser import Ui_BrowserDock
from prymatex.core.settings import pmxConfigPorperty
from prymatex.support.utils import prepareShellScript, deleteFile
from prymatex.core.plugin.dock import PMXBaseDock

class TmFileReply(QNetworkReply):
    def __init__(self, parent, url, operation):
        super(TmFileReply, self).__init__(parent)
        file = codecs.open(url.path(), 'r', 'utf-8')
        self.content = file.read().encode('utf-8')
        self.offset = 0
        
        self.setHeader(QNetworkRequest.ContentTypeHeader, "text/html; charset=utf-8")
        self.setHeader(QNetworkRequest.ContentLengthHeader, len(self.content))
        QtCore.QTimer.singleShot(0, self, QtCore.SIGNAL("readyRead()"))
        QtCore.QTimer.singleShot(0, self, QtCore.SIGNAL("finished()"))
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

class NetworkAccessManager(QNetworkAccessManager):
    commandUrlRequested = QtCore.pyqtSignal(QtCore.QUrl)
    
    def __init__(self, parent, old_manager):
        super(NetworkAccessManager, self).__init__(parent)
        self.old_manager = old_manager
        self.setCache(old_manager.cache())
        self.setCookieJar(old_manager.cookieJar())
        self.setProxy(old_manager.proxy())
        self.setProxyFactory(old_manager.proxyFactory())
    
    def createRequest(self, operation, request, data):
        if request.url().scheme() == "txmt":
            self.commandUrlRequested.emit(request.url())
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

class SystemWrapper(QtCore.QObject):
    def __init__(self, process, file):
        QtCore.QObject.__init__(self)
        self.process = process
        self.file = file
    
    @QtCore.pyqtSlot(str)
    def write(self, data):
        self.process.stdin.write(data)
    
    @QtCore.pyqtSlot()
    def read(self):
        self.process.stdin.close()
        text = self.process.stdout.read()
        self.process.stdout.close()
        self.process.wait()
        deleteFile(self.file)
        return text
        
    @QtCore.pyqtSlot()
    def close(self):
        self.process.stdin.close()
        self.process.stdout.close()
        self.process.wait()
        deleteFile(self.file)

    def outputString(self):
        self.process.stdin.close()
        text = self.process.stdout.read()
        self.process.stdout.close()
        self.process.wait()
        deleteFile(self.file)
        return text
    outputString = QtCore.pyqtProperty(str, outputString)
    
class TextMate(QtCore.QObject):
    def __init__(self, mainFrame, bundleItem = None):
        QtCore.QObject.__init__(self)
        self.mainFrame = mainFrame
        self.bundleItem = bundleItem
        
    @QtCore.pyqtSlot(str)
    def _system(self, command):
        environment = self.bundleItem != None and self.bundleItem.buildEnvironment() or {}
        with prepareShellScript(unicode(command), environment) as (tempFile, environment):
            process = Popen([ tempFile ], stdout=PIPE, stdin=PIPE, stderr=STDOUT, env = environment)
            self.mainFrame.addToJavaScriptWindowObject("_systemWrapper", SystemWrapper(process, tempFile))

    def isBusy(self):
        return True
    isBusy = QtCore.pyqtProperty("bool", isBusy)
    
class PMXBrowserDock(QtGui.QDockWidget, Ui_BrowserDock, PMXBaseDock):
    SHORTCUT = "F9"
    ICON = resources.getIcon("browser")
    PREFERED_AREA = QtCore.Qt.BottomDockWidgetArea
    
    SETTINGS_GROUP = "Browser"
    
    updateInterval = pmxConfigPorperty(default = 3000)
    homePage = pmxConfigPorperty(default = "http://www.prymatex.org")
    @pmxConfigPorperty(default = os.environ.get('http_proxy', ''))
    def proxy(self, value):
        """System wide proxy
        """
        proxy_url = QtCore.QUrl(value)
        #TODO: Una regexp para filtar basura y quitar el try except
        if not value:
            network_proxy = QNetworkProxy(QNetworkProxy.NoProxy)
        else:
            try:
                protocol = QNetworkProxy.NoProxy
                if proxy_url.scheme().startswith('http'):
                    protocol = QNetworkProxy.HttpProxy
                else:
                    protocol = QNetworkProxy.Socks5Proxy
                network_proxy = QNetworkProxy(protocol, proxy_url.host(), proxy_url.port(), proxy_url.userName(), proxy_url.password())
            except:
                network_proxy = QNetworkProxy(QNetworkProxy.NoProxy)
        QNetworkProxy.setApplicationProxy( network_proxy )
    
    @classmethod
    def contributeToSettings(cls):
        from prymatex.gui.settings.browser import PMXNetworkWidget
        return [ PMXNetworkWidget ]
        
    def __init__(self, parent):
        QtGui.QDockWidget.__init__(self, parent)
        PMXBaseDock.__init__(self)
        self.setupUi(self)
        self.setupToolBar()

        #Developers, developers, developers!!! Extras
        QtWebKit.QWebSettings.globalSettings().setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)
        QtWebKit.QWebSettings.globalSettings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled, True)
        
        #New manager
        self.networkAccessManager = NetworkAccessManager(self, self.webView.page().networkAccessManager())
        self.webView.page().setNetworkAccessManager(self.networkAccessManager)
        self.networkAccessManager.commandUrlRequested.connect(self.on_manager_commandUrlRequested)

        # Set the default home page
        self.lineUrl.setText(self.homePage)
        self.webView.setUrl(QtCore.QUrl(self.homePage))
        
        self.scrollValues = (False, 0, 0)   #(<restore scroll values>, <horizontalValue>, <verticalValue>)

        # history buttons:
        self.buttonBack.setEnabled(False)
        self.buttonNext.setEnabled(False)
        
        #Capturar editor, bundleitem
        self.currentEditor = None
        self.bundleItem = None
        
        #Sync Timer
        self.updateTimer = QtCore.QTimer()
        self.updateTimer.timeout.connect(self.updateHtmlCurrentEditorContent)
        
    def setupToolBar(self):
        #Setup Context Menu
        optionsMenu = { 
            "title": "Browser Options",
            "items": [ self.actionSyncEditor, self.actionConnectEditor ]
        }

        self.browserOptionsMenu, _ = createQMenu(optionsMenu, self)
        self.pushButtonOptions.setMenu(self.browserOptionsMenu)

    def on_manager_commandUrlRequested(self, url):
        self.application.handleUrlCommand(url)
        
    def initialize(self, mainWindow):
        PMXBaseDock.initialize(self, mainWindow)
        mainWindow.browser = self
        
    def showEvent(self, event):
        self.setFocus()
    
    def event(self, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Escape:
                self.close()
                self.mainWindow.currentEditor().setFocus()
                return True
            elif event.key() == QtCore.Qt.Key_L and event.modifiers() == QtCore.Qt.ControlModifier:
                self.lineUrl.setFocus()
                self.lineUrl.selectAll()
                return True
        return QtGui.QDockWidget.event(self, event)
    
    
    def setHtml(self, string, bundleItem = None):
        if not self.isVisible():
            self.show()
        self.raise_()
        self.bundleItem = bundleItem
        url = QtCore.QUrl.fromUserInput("about:%s" % bundleItem.name)
        self.lineUrl.setText(url.toString())
        self.webView.setHtml(string, url)
    
    def on_lineUrl_returnPressed(self):
        """Url have been changed by user"""

        page = self.webView.page()
        history = page.history()
        self.buttonBack.setEnabled(history.canGoBack())
        self.buttonNext.setEnabled(history.canGoForward())
        
        url = QtCore.QUrl.fromUserInput(self.lineUrl.text())
        self.webView.setUrl(url)

    def on_buttonStop_clicked(self):
        """Stop loading the page"""
        self.webView.stop()

    def on_buttonReload_clicked(self):
        """Reload the web page"""
        url = QtCore.QUrl.fromUserInput(self.lineUrl.text())
        self.webView.setUrl(url)

    #=============================
    # QWebView Signals
    #=============================
    def on_webView_iconChanged(self):
        # print "iconChanged"
        pass

    def on_webView_linkClicked(self, link):
        #Terminar el timer y navegar hasta esa Url
        #TODO: validar que el link este bien
        self.stopTimer()
        map(lambda action: action.setChecked(False), [ self.actionSyncEditor, self.actionConnectEditor ])
        self.webView.load(link)

    def on_webView_loadFinished(self, ready):
        if not ready:
            return
        self.webView.page().mainFrame().addToJavaScriptWindowObject("TextMate", TextMate(self.webView.page().mainFrame(), self.bundleItem))
        self.webView.page().mainFrame().evaluateJavaScript(js)
        
        #Restore scroll
        if self.scrollValues[0]:
            self.webView.page().mainFrame().setScrollBarValue(QtCore.Qt.Horizontal, self.scrollValues[1])
            self.webView.page().mainFrame().setScrollBarValue(QtCore.Qt.Vertical, self.scrollValues[2])

    def on_webView_urlChanged(self, url):
        """Update the URL if a link on a web page is clicked"""
        #History
        page = self.webView.page()
        history = page.history()
        self.buttonBack.setEnabled(history.canGoBack())
        self.buttonNext.setEnabled(history.canGoForward())
        
        #Scroll Values
        self.scrollValues = (url.toString() == self.webView.url().toString(), self.scrollValues[1], self.scrollValues[2])

        #Line Location
        self.lineUrl.setText(url.toString())

    def on_webView_loadStarted(self):
        self.scrollValues = ( False,    self.webView.page().mainFrame().scrollBarValue(QtCore.Qt.Horizontal),
                                               self.webView.page().mainFrame().scrollBarValue(QtCore.Qt.Vertical))
        
    def on_webView_loadProgress(self, load):
        """Page load progress"""
        self.buttonStop.setEnabled(load != 100)
    
    def on_webView_selectionChanged(self):
        # print "selectionChanged"
        pass

    def on_webView_statusBarMessage(self, message):
        # print "statusBarMessage", message
        pass
        
    def on_webView_titleChanged(self, title):
        """Web page title changed - change the tab name"""
        #print "titleChanged", title
        #self.setWindowTitle(title)
        pass
    
    def on_buttonBack_clicked(self):
        """Back button clicked, go one page back"""
        page = self.webView.page()
        history = page.history()
        history.back()
        self.buttonBack.setEnabled(history.canGoBack())
    
    def on_buttonNext_clicked(self):
        """Next button clicked, go to next page"""
        page = self.webView.page()
        history = page.history()
        history.forward()
        self.buttonNext.setEnabled(history.canGoForward())
        
    def updateHtmlCurrentEditorContent(self):
        # TODO Resolver url, asegurar que sea html para no hacer cochinadas
        editor = self.currentEditor if self.currentEditor is not None else self.mainWindow.currentEditor()
        content = editor.toPlainText()
        url = QtCore.QUrl.fromUserInput(editor.filePath)
        
        self.webView.settings().clearMemoryCaches()
        
        self.webView.setHtml(content, url)
    
    def stopTimer(self):
        self.updateTimer.stop()
        self.webView.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DontDelegateLinks)

    def startTimer(self):
        self.updateTimer.start(self.updateInterval)
        self.webView.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)

    def connectCurrentEditor(self):
        self.currentEditor = self.mainWindow.currentEditor()
        self.connect(self.currentEditor, QtCore.SIGNAL("close()"), self.disconnectCurrentEditor)
        
    def disconnectCurrentEditor(self):
        if self.currentEditor is not None:
            self.disconnect(self.currentEditor, QtCore.SIGNAL("close()"), self.disconnectCurrentEditor)
            self.currentEditor = None

    @QtCore.pyqtSlot(bool)
    def on_actionSyncEditor_toggled(self, checked):
        if checked:
            #Quitar otro check
            self.actionConnectEditor.setChecked(False)
            #Desconectar editor
            self.disconnectCurrentEditor()
            self.startTimer()
        else:
            self.stopTimer()

    @QtCore.pyqtSlot(bool)
    def on_actionConnectEditor_toggled(self, checked):
        # TODO Capturar el current editor y usarlo para el update
        if checked:
            #Quitar otro check
            self.actionSyncEditor.setChecked(False)
            #Capturar editor
            self.connectCurrentEditor()
            self.startTimer()
        else:
            self.stopTimer()
            self.disconnectCurrentEditor()
