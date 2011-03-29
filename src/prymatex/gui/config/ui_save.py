# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/save.ui'
#
# Created: Mon Mar 28 19:14:21 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Save(object):
    def setupUi(self, Save):
        Save.setObjectName("Save")
        Save.resize(400, 300)
        self.checkBox = QtGui.QCheckBox(Save)
        self.checkBox.setGeometry(QtCore.QRect(40, 30, 87, 21))
        self.checkBox.setObjectName("checkBox")

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

