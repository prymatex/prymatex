# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/panebrowser.ui'
#
# Created: Mon Aug 29 18:12:50 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_BrowserPane(object):
    def setupUi(self, BrowserPane):
        BrowserPane.setObjectName(_fromUtf8("BrowserPane"))
        BrowserPane.resize(400, 300)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.webView = QtWebKit.QWebView(self.dockWidgetContents)
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.verticalLayout.addWidget(self.webView)
        BrowserPane.setWidget(self.dockWidgetContents)

        self.retranslateUi(BrowserPane)
        QtCore.QMetaObject.connectSlotsByName(BrowserPane)

    def retranslateUi(self, BrowserPane):
        BrowserPane.setWindowTitle(_('Web Browser'))

from PyQt4 import QtWebKit
