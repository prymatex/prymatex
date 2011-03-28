# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/general.ui'
#
# Created: Mon Mar 28 14:11:23 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_General(object):
    def setupUi(self, General):
        General.setObjectName("General")
        General.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(General)
        self.verticalLayout.setObjectName("verticalLayout")
        self.checkBox = QtGui.QCheckBox(General)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout.addWidget(self.checkBox)
        self.checkBox_2 = QtGui.QCheckBox(General)
        self.checkBox_2.setObjectName("checkBox_2")
        self.verticalLayout.addWidget(self.checkBox_2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(General)
        QtCore.QMetaObject.connectSlotsByName(General)

    def retranslateUi(self, General):
        General.setWindowTitle(QtGui.QApplication.translate("General", "General", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("General", "Highlight curent line", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_2.setText(QtGui.QApplication.translate("General", "Show right margin indicator", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    General = QtGui.QWidget()
    ui = Ui_General()
    ui.setupUi(General)
    General.show()
    sys.exit(app.exec_())

