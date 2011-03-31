# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/multiclose.ui'
#
# Created: Thu Mar 31 09:44:48 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_SaveMultipleDialog(object):
    def setupUi(self, SaveMultipleDialog):
        SaveMultipleDialog.setObjectName("SaveMultipleDialog")
        SaveMultipleDialog.resize(400, 186)
        self.verticalLayout = QtGui.QVBoxLayout(SaveMultipleDialog)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(SaveMultipleDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.tableView = QtGui.QTableView(SaveMultipleDialog)
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushSaveSelected = QtGui.QPushButton(SaveMultipleDialog)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/actions/resources/actions/document-save-all.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushSaveSelected.setIcon(icon)
        self.pushSaveSelected.setObjectName("pushSaveSelected")
        self.horizontalLayout.addWidget(self.pushSaveSelected)
        self.pushDontSave = QtGui.QPushButton(SaveMultipleDialog)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/actions/resources/actions/edit-delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushDontSave.setIcon(icon1)
        self.pushDontSave.setObjectName("pushDontSave")
        self.horizontalLayout.addWidget(self.pushDontSave)
        self.pushCancel = QtGui.QPushButton(SaveMultipleDialog)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/actions/resources/actions/process-stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushCancel.setIcon(icon2)
        self.pushCancel.setObjectName("pushCancel")
        self.horizontalLayout.addWidget(self.pushCancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(SaveMultipleDialog)
        QtCore.QObject.connect(self.pushCancel, QtCore.SIGNAL("clicked()"), SaveMultipleDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SaveMultipleDialog)

    def retranslateUi(self, SaveMultipleDialog):
        SaveMultipleDialog.setWindowTitle(QtGui.QApplication.translate("SaveMultipleDialog", "Close Multiple Files", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("SaveMultipleDialog", "Some files have been altered since they were opened. \n"
"Do you want to save them?", None, QtGui.QApplication.UnicodeUTF8))
        self.pushSaveSelected.setText(QtGui.QApplication.translate("SaveMultipleDialog", "Save &Selected", None, QtGui.QApplication.UnicodeUTF8))
        self.pushDontSave.setText(QtGui.QApplication.translate("SaveMultipleDialog", "Do &not save", None, QtGui.QApplication.UnicodeUTF8))
        self.pushCancel.setText(QtGui.QApplication.translate("SaveMultipleDialog", "&Cancel", None, QtGui.QApplication.UnicodeUTF8))

import res_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    SaveMultipleDialog = QtGui.QDialog()
    ui = Ui_SaveMultipleDialog()
    ui.setupUi(SaveMultipleDialog)
    SaveMultipleDialog.show()
    sys.exit(app.exec_())

