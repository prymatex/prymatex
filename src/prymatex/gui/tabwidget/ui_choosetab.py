# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/choosetab.ui'
#
# Created: Tue Jan  4 16:55:08 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ChooseTab(object):
    def setupUi(self, ChooseTab):
        ChooseTab.setObjectName("ChooseTab")
        ChooseTab.resize(310, 170)
        self.verticalLayout = QtGui.QVBoxLayout(ChooseTab)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEdit = QtGui.QLineEdit(ChooseTab)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.listView = QtGui.QListView(ChooseTab)
        self.listView.setObjectName("listView")
        self.verticalLayout.addWidget(self.listView)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushOpen = QtGui.QPushButton(ChooseTab)
        self.pushOpen.setDefault(True)
        self.pushOpen.setObjectName("pushOpen")
        self.horizontalLayout.addWidget(self.pushOpen)
        self.pushCancel = QtGui.QPushButton(ChooseTab)
        self.pushCancel.setObjectName("pushCancel")
        self.horizontalLayout.addWidget(self.pushCancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ChooseTab)
        QtCore.QMetaObject.connectSlotsByName(ChooseTab)

    def retranslateUi(self, ChooseTab):
        ChooseTab.setWindowTitle(QtGui.QApplication.translate("ChooseTab", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.pushOpen.setText(QtGui.QApplication.translate("ChooseTab", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.pushCancel.setText(QtGui.QApplication.translate("ChooseTab", "Cancel", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ChooseTab = QtGui.QDialog()
    ui = Ui_ChooseTab()
    ui.setupUi(ChooseTab)
    ChooseTab.show()
    sys.exit(app.exec_())

