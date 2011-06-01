# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/preference.ui'
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

class Ui_Preference(object):
    def setupUi(self, Preference):
        Preference.setObjectName(_fromUtf8("Preference"))
        Preference.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(Preference)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.plainTextEdit = QtGui.QPlainTextEdit(Preference)
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.verticalLayout.addWidget(self.plainTextEdit)

        self.retranslateUi(Preference)
        QtCore.QMetaObject.connectSlotsByName(Preference)

    def retranslateUi(self, Preference):
        Preference.setWindowTitle(QtGui.QApplication.translate("Preference", "Form", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Preference = QtGui.QWidget()
    ui = Ui_Preference()
    ui.setupUi(Preference)
    Preference.show()
    sys.exit(app.exec_())

