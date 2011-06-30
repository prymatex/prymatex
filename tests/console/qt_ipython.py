# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_ipython.ui'
#
# Created: Sun Nov 30 21:03:28 2008
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_IPyForm(object):
    def setupUi(self, IPyForm):
        IPyForm.setObjectName("IPyForm")
        IPyForm.resize(742, 519)
        self.verticalLayout = QtGui.QVBoxLayout(IPyForm)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtGui.QSplitter(IPyForm)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.textEdit = QtGui.QTextEdit(self.splitter)
        self.textEdit.setObjectName("textEdit")
        self.editor = Qsci.QsciScintilla(self.splitter)
        self.editor.setObjectName("editor")
        self.verticalLayout.addWidget(self.splitter)

        self.retranslateUi(IPyForm)
        QtCore.QMetaObject.connectSlotsByName(IPyForm)

    def retranslateUi(self, IPyForm):
        IPyForm.setWindowTitle(QtGui.QApplication.translate("IPyForm", "IPython Qt", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import Qsci
