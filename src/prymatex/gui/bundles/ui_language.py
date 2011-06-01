# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/language.ui'
#
# Created: Tue May 31 18:51:24 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Language(object):
    def setupUi(self, Language):
        Language.setObjectName(_fromUtf8("Language"))
        Language.resize(274, 210)
        self.verticalLayout = QtGui.QVBoxLayout(Language)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.plainTextEdit = QtGui.QPlainTextEdit(Language)
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.verticalLayout.addWidget(self.plainTextEdit)

        self.retranslateUi(Language)
        QtCore.QMetaObject.connectSlotsByName(Language)

    def retranslateUi(self, Language):
        Language.setWindowTitle(QtGui.QApplication.translate("Language", "Form", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Language = QtGui.QWidget()
    ui = Ui_Language()
    ui.setupUi(Language)
    Language.show()
    sys.exit(app.exec_())

