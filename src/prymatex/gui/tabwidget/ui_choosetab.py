# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/choosetab.ui'
#
# Created: Mon Jan  3 17:56:04 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(310, 170)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEdit = QtGui.QLineEdit(Dialog)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.listView = QtGui.QListView(Dialog)
        self.listView.setObjectName("listView")
        self.verticalLayout.addWidget(self.listView)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushOpen = QtGui.QPushButton(Dialog)
        self.pushOpen.setDefault(True)
        self.pushOpen.setObjectName("pushOpen")
        self.horizontalLayout.addWidget(self.pushOpen)
        self.pushCancel = QtGui.QPushButton(Dialog)
        self.pushCancel.setObjectName("pushCancel")
        self.horizontalLayout.addWidget(self.pushCancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.pushOpen.setText(QtGui.QApplication.translate("Dialog", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.pushCancel.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

