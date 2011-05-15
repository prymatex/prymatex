# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/envvars.ui'
#
# Created: Sun May 15 00:37:58 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_EnvVariables(object):
    def setupUi(self, EnvVariables):
        EnvVariables.setObjectName(_fromUtf8("EnvVariables"))
        EnvVariables.resize(400, 449)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/resources/actions/configure.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        EnvVariables.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(EnvVariables)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(EnvVariables)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.tableView = QtGui.QTableView(EnvVariables)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.verticalLayout.addWidget(self.tableView)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushAdd = QtGui.QPushButton(EnvVariables)
        self.pushAdd.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/resources/actions/list-add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushAdd.setIcon(icon1)
        self.pushAdd.setObjectName(_fromUtf8("pushAdd"))
        self.horizontalLayout.addWidget(self.pushAdd)
        self.pushRemove = QtGui.QPushButton(EnvVariables)
        self.pushRemove.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/resources/actions/list-remove.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushRemove.setIcon(icon2)
        self.pushRemove.setObjectName(_fromUtf8("pushRemove"))
        self.horizontalLayout.addWidget(self.pushRemove)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(EnvVariables)
        QtCore.QMetaObject.connectSlotsByName(EnvVariables)

    def retranslateUi(self, EnvVariables):
        EnvVariables.setWindowTitle(QtGui.QApplication.translate("EnvVariables", "Enviroment Variables", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("EnvVariables", "Enviroment Variables", None, QtGui.QApplication.UnicodeUTF8))

import res_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    EnvVariables = QtGui.QWidget()
    ui = Ui_EnvVariables()
    ui.setupUi(EnvVariables)
    EnvVariables.show()
    sys.exit(app.exec_())

