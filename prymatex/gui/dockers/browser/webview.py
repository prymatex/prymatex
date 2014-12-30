#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import mimetypes

from prymatex.qt import QtGui, QtCore, QtWebKit, QtWebKitWidgets

from .network import NetworkAccessManager
from .scripts import TextMate, SystemWrapper, WINDOW_JAVASCRIPT

class WebView(QtWebKitWidgets.QWebView):
    def __init__(self, browserDock):
        QtWebKitWidgets.QWebView.__init__(self, browserDock)
        self.browserDock = browserDock
        
        #self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.networkAccessManager = self.buildNetworkAccessManager()
        self.__running_context = None

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
        if self.runningContext() is None:
            return False
        return self.runningContext().isBundleItem(context.bundleItem)

    def setRunningContext(self, context):
        self.__running_context = context
        self.createWebPage(context.outputValue,
            QtCore.QUrl.fromUserInput("about:%s" % context.description()))

    def runningContext(self):
        return self.__running_context

    def createWebPage(self, content, url):
        page = QtWebKitWidgets.QWebPage(self)
        page.setNetworkAccessManager(self.networkAccessManager)
        page.mainFrame().javaScriptWindowObjectCleared.connect(self.on_mainFrame_javaScriptWindowObjectCleared)
        page.setForwardUnsupportedContent(True)
        page.unsupportedContent.connect(self.on_page_unsupportedContent)
        self.setPage(page)
        page.mainFrame().setUrl(url)
        page.mainFrame().setHtml(content)

    # ------------ Override
    def title(self):
        title = QtWebKitWidgets.QWebView.title(self)
        if not title and self.runningContext() is not None:
            return self.runningContext().description()
        return title

    def createWindow(self, windowType):
        return self.browserDock.createWebView(windowType)

    # ------------ Page Signals handlers
    def on_mainFrame_javaScriptWindowObjectCleared(self):
        self.page().mainFrame().addToJavaScriptWindowObject("TextMate", TextMate(self,
            self.browserDock.application().supportManager
        ))
        env = []
        if self.runningContext():
            for key, value in self.runningContext().environment.items():
                env.append('window["{0}"]="{1}"'.format(key, value))
        self.page().mainFrame().evaluateJavaScript(WINDOW_JAVASCRIPT % ";\n".join(env))

    def on_page_unsupportedContent(self, reply):
        url = reply.url()
        QtGui.QDesktopServices.openUrl(url)

    def on_networkAccessManager_commandUrlRequested(self, url):
        self.browserDock.application().openUrl(url)
