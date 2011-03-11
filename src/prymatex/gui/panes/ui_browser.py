# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/browser.ui'
#
# Created: Fri Mar 11 16:23:36 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Browser(object):
    def setupUi(self, Browser):
        Browser.setObjectName(_fromUtf8("Browser"))
        Browser.resize(501, 438)
        self.verticalLayout = QtGui.QVBoxLayout(Browser)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.view = QtWebKit.QWebView(Browser)
        self.view.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.view.setObjectName(_fromUtf8("view"))
        self.verticalLayout.addWidget(self.view)

        self.retranslateUi(Browser)
        QtCore.QMetaObject.connectSlotsByName(Browser)

    def retranslateUi(self, Browser):
        Browser.setWindowTitle(QtGui.QApplication.translate("Browser", "Form", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import QtWebKit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Browser = QtGui.QWidget()
    ui = Ui_Browser()
    ui.setupUi(Browser)
    Browser.show()
    sys.exit(app.exec_())

