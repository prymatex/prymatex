# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/browser.ui'
#
# Created: Tue Mar 15 18:52:36 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

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
        BrowserPane.setWindowTitle(QtGui.QApplication.translate("BrowserPane", "Browser Panel", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import QtWebKit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    BrowserPane = QtGui.QDockWidget()
    ui = Ui_BrowserPane()
    ui.setupUi(BrowserPane)
    BrowserPane.show()
    sys.exit(app.exec_())

