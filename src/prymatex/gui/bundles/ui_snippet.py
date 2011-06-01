# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/snippet.ui'
#
# Created: Tue May 31 18:51:25 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Snippet(object):
    def setupUi(self, Snippet):
        Snippet.setObjectName(_fromUtf8("Snippet"))
        Snippet.resize(274, 210)
        self.verticalLayout = QtGui.QVBoxLayout(Snippet)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.plainTextEdit = QtGui.QPlainTextEdit(Snippet)
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.verticalLayout.addWidget(self.plainTextEdit)

        self.retranslateUi(Snippet)
        QtCore.QMetaObject.connectSlotsByName(Snippet)

    def retranslateUi(self, Snippet):
        Snippet.setWindowTitle(QtGui.QApplication.translate("Snippet", "Form", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Snippet = QtGui.QWidget()
    ui = Ui_Snippet()
    ui.setupUi(Snippet)
    Snippet.show()
    sys.exit(app.exec_())

