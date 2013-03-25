#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from .webview import WebView

class TabbedWebView(QtGui.QTabWidget):
    currentWebViewChanged = QtCore.pyqtSignal(WebView)
    
    def __init__(self, parent=None):
        super(TabbedWebView, self).__init__(parent)
        self._new_button = QtGui.QPushButton(self)
        self._new_button.setText("New")
        self._new_button.clicked.connect(lambda checked: self.createWebView())
        self.setCornerWidget(self._new_button)
        self.setTabsClosable(True)
        self.setMovable(True)
        self.tabCloseRequested[int].connect(self._on_tabCloseRequested)
        self.currentChanged[int].connect(self._on_currentChanged)
        
    # Signals
    def _on_tabCloseRequested(self, index):
        webView = self.widget(index)
        print "cerrar", webView

    def _on_currentChanged(self, index):
        webView = self.widget(index)
        self.currentWebViewChanged.emit(webView)

    def createWebView(self):
        webView = WebView(self)
        webView.titleChanged.connect(self.on_webView_titleChanged)
        webView.iconChanged.connect(self.on_webView_iconChanged)
        self.addTab(webView, webView.title())
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