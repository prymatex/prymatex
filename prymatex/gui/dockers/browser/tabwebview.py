#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from .webview import WebView

class TabbedWebView(QtGui.QTabWidget):
    currentWebViewChanged = QtCore.pyqtSignal(WebView)
    empty = QtCore.pyqtSignal()
    
    def __init__(self, parent=None):
        QtGui.QTabWidget.__init__(self, parent)

        # Corner widget
        self.buttonNew = QtGui.QPushButton(self)
        self.buttonNew.setText("")
        self.buttonNew.setIcon(QtGui.QIcon.fromTheme("tab-new-background"))
        self.buttonNew.setMaximumSize(QtCore.QSize(28, 28))
        self.buttonNew.clicked.connect(lambda checked: self.createWebView())
        self.setCornerWidget(self.buttonNew)
        
        self.setTabsClosable(True)
        self.setMovable(True)
        self.tabCloseRequested[int].connect(self.removeTab)
        self.currentChanged[int].connect(self._on_currentChanged)
    
    def _on_currentChanged(self, index):
        webView = self.widget(index)
        if webView is not None:
            self.currentWebViewChanged.emit(webView)
        elif self.count() == 0:
            self.empty.emit()

    def createWebView(self):
        webView = WebView(self)
        webView.titleChanged.connect(self.on_webView_titleChanged)
        webView.iconChanged.connect(self.on_webView_iconChanged)
        index = self.addTab(webView, "New")
        return webView

    def currentWebView(self):
        return self.currentWidget()

    # Signals
    def on_webView_titleChanged(self, title):
        webView = self.sender()
        index = self.indexOf(webView)
        self.setTabText(index, webView.title())
        
    def on_webView_iconChanged(self):
        webView = self.sender()
        index = self.indexOf(webView)
        self.setTabIcon(index, webView.icon())