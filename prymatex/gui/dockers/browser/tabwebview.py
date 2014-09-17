#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets
from .webview import WebView

class TabbedWebView(QtWidgets.QTabWidget):
    currentWebViewChanged = QtCore.Signal(WebView)
    webViewNewRequested = QtCore.Signal()
    webViewCloseRequested = QtCore.Signal(WebView)
    
    def __init__(self, browserDock):
        QtWidgets.QTabWidget.__init__(self, browserDock)
        self.browserDock = browserDock

        # Corner widget
        self.buttonNew = QtWidgets.QPushButton(self)
        self.buttonNew.setText("")
        self.buttonNew.setIcon(QtGui.QIcon.fromTheme("tab-new"))
        self.buttonNew.setMaximumSize(QtCore.QSize(28, 28))
        self.buttonNew.clicked.connect(lambda checked: self.webViewNewRequested.emit())
        self.setCornerWidget(self.buttonNew)
        
        self.setTabsClosable(True)
        self.setMovable(True)
        self.tabCloseRequested[int].connect(
            lambda index: self.webViewCloseRequested.emit(self.widget(index)))
        self.currentChanged[int].connect(
            lambda index: self.currentWebViewChanged.emit(self.widget(index)))
    
    def addWebView(self, webView):
        webView.titleChanged.connect(self.on_webView_titleChanged)
        webView.iconChanged.connect(self.on_webView_iconChanged)
        index = self.addTab(webView, webView.title())
        self.setTabIcon(index, webView.icon())
        return index
    
    def currentWebView(self):
        return self.currentWidget()

    def removeWebView(self, webView):
        self.removeTab(self.indexOf(webView))

    # Signals
    def on_webView_titleChanged(self, title):
        webView = self.sender()
        index = self.indexOf(webView)
        self.setTabText(index, webView.title())
        
    def on_webView_iconChanged(self):
        webView = self.sender()
        index = self.indexOf(webView)
        self.setTabIcon(index, webView.icon())
