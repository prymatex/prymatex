#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import codecs
import mimetypes
from subprocess import Popen, PIPE, STDOUT

from prymatex.qt import QtCore, QtGui, QtNetwork, QtWebKit
from prymatex.qt.QtNetwork import QNetworkProxy

class FileReply(QtNetwork.QNetworkReply):
    def __init__(self, parent, url, operation):
        super(FileReply, self).__init__(parent)
        fp = open(url.path(), 'r')
        self.content = fp.read()
        self.offset = 0

        mimetype = mimetypes.guess_type(url.path())[0]
        #self.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader, mimetype)
        self.setHeader(QtNetwork.QNetworkRequest.ContentLengthHeader, len(self.content))
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

class NetworkAccessManager(QtNetwork.QNetworkAccessManager):
    commandUrlRequested = QtCore.Signal(QtCore.QUrl)
    
    def createRequest(self, operation, request, data):
        print("createRequest", request.url().scheme())
        if request.url().scheme() == "txmt":
            self.commandUrlRequested.emit(request.url())
        elif request.url().scheme() == "tm-file" and operation == self.GetOperation:
            #TODO: Ava tenemos que trabajar con el mime antes, ver el caso del os pdf
            return FileReply(self, request.url(), self.GetOperation)
        return QtNetwork.QNetworkAccessManager.createRequest(self, operation, request, data)
        
def setGlobalApplicationProxy(proxyAddress = None):
    networkProxy = QtNetwork.QNetworkProxy(QNetworkProxy.NoProxy)
    if proxyAddress is not None:
        proxyUrl = QtCore.QUrl(proxyAddress)
        protocol = QtNetwork.QNetworkProxy.NoProxy
        if proxyUrl.scheme().startswith('http'):
            protocol = QtNetwork.QNetworkProxy.HttpProxy
        else:
            protocol = QtNetwork.QNetworkProxy.Socks5Proxy
        networkProxy = QtNetwork.QNetworkProxy(protocol, proxyUrl.host(), proxyUrl.port(), proxyUrl.userName(), proxyUrl.password())
    QtNetwork.QNetworkProxy.setApplicationProxy( networkProxy )
