#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import subprocess
import mimetypes

from prymatex.qt import QtGui, QtCore, QtWebKit

from .network import NetworkAccessManager
from .scripts import TextMate, SystemWrapper, WINDOW_JAVASCRIPT

class WebView(QtWebKit.QWebView):
    def __init__(self, browserDock):
        QtWebKit.QWebView.__init__(self, browserDock)
        self.browserDock = browserDock
        
        #self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.networkAccessManager = self.buildNetworkAccessManager()
        self.runningContext = None

    def buildNetworkAccessManager(self):
        defaultManager = self.page().networkAccessManager()
        networkAccessManager = NetworkAccessManager(self)
        networkAccessManager.setCache(defaultManager.cache())
        networkAccessManager.setCookieJar(defaultManager.cookieJar())
        networkAccessManager.setProxy(defaultManager.proxy())
        networkAccessManager.setProxyFactory(defaultManager.proxyFactory())
        networkAccessManager.commandUrlRequested.connect(self.on_networkAccessManager_commandUrlRequested)
        return networkAccessManager

    def isSimilarContext(self, context):
        if self.runningContext is None:
            return False
        return self.runningContext.isBundleItem(context.bundleItem)

    def setRunningContext(self, context):
        self.runningContext = context
        self.createWebPage(context.outputValue,
            QtCore.QUrl.fromUserInput("about:%s" % context.description()))

    def createWebPage(self, content, url):
        page = QtWebKit.QWebPage(self)
        page.setNetworkAccessManager(self.networkAccessManager)
        page.mainFrame().javaScriptWindowObjectCleared.connect(self.on_mainFrame_javaScriptWindowObjectCleared)
        page.setForwardUnsupportedContent(True)
        page.unsupportedContent.connect(self.on_page_unsupportedContent)
        self.setPage(page)
        page.mainFrame().setUrl(url)
        page.mainFrame().setHtml(content)

    # ------------ Override
    def title(self):
        title = QtWebKit.QWebView.title(self)
        if not title and self.runningContext is not None:
            return self.runningContext.description()
        return title

    def createWindow(self, windowType):
        return self.browserDock.createWebView(windowType)

    # ------------ Page Signals handlers
    def on_mainFrame_javaScriptWindowObjectCleared(self):
        self.page().mainFrame().addToJavaScriptWindowObject("TextMate", TextMate(self))
        environment = "\n".join(
            ['window["{0}"]="{1}";'.format(key_value[0], key_value[1]) for key_value in self.runningContext is not None and iter(self.runningContext.environment.items()) or {}]
        )
        self.page().mainFrame().evaluateJavaScript(WINDOW_JAVASCRIPT % environment)

    def on_page_unsupportedContent(self, reply):
        url = reply.url()
        print("UnsupportedContent", url)
        QtGui.QDesktopServices.openUrl(url)

    def on_networkAccessManager_commandUrlRequested(self, url):
        self.browserDock.application.handleUrlCommand(url)

    def runCommand(self, command):
        self.runningContext.removeTempFile()
        self.runningContext.setShellCommand(command)
        with self.runningContext as context:
            context.process = subprocess.Popen(context.shellCommand, 
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, env=context.environment)
            self.page().mainFrame().addToJavaScriptWindowObject("_systemWrapper", 
                SystemWrapper(context.process))