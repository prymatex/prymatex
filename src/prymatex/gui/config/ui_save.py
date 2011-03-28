# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/save.ui'
#
# Created: Mon Mar 28 18:45:09 2011
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Save(object):
    def setupUi(self, Save):
        Save.setObjectName(_fromUtf8("Save"))
        Save.resize(400, 300)
        self.checkBox = QtGui.QCheckBox(Save)
        self.checkBox.setGeometry(QtCore.QRect(40, 30, 87, 21))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))

        self.retranslateUi(Save)
        QtCore.QMetaObject.connectSlotsByName(Save)

    def retranslateUi(self, Save):
        Save.setWindowTitle(QtGui.QApplication.translate("Save", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("Save", "Autosave", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Save = QtGui.QWidget()
    ui = Ui_Save()
    ui.setupUi(Save)
    Save.show()
    sys.exit(app.exec_())

