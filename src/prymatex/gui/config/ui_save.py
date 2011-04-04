# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/save.ui'
#
# Created: Thu Mar 31 09:45:11 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Save(object):
    def setupUi(self, Save):
        Save.setObjectName("Save")
        Save.resize(400, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/actions/resources/actions/document-save-all.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Save.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(Save)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.checkBox_2 = QtGui.QCheckBox(Save)
        self.checkBox_2.setObjectName("checkBox_2")
        self.horizontalLayout_2.addWidget(self.checkBox_2)
        self.spinBox = QtGui.QSpinBox(Save)
        self.spinBox.setEnabled(False)
        self.spinBox.setMaximum(120)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout_2.addWidget(self.spinBox)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(Save)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtGui.QLineEdit(Save)
        self.lineEdit.setEnabled(False)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.label_2 = QtGui.QLabel(Save)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEdit_2 = QtGui.QLineEdit(Save)
        self.lineEdit_2.setEnabled(False)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout.addWidget(self.lineEdit_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem1 = QtGui.QSpacerItem(20, 193, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(Save)
        QtCore.QObject.connect(self.checkBox_2, QtCore.SIGNAL("toggled(bool)"), self.spinBox.setEnabled)
        QtCore.QObject.connect(self.checkBox_2, QtCore.SIGNAL("toggled(bool)"), self.lineEdit.setEnabled)
        QtCore.QObject.connect(self.checkBox_2, QtCore.SIGNAL("toggled(bool)"), self.lineEdit_2.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(Save)

    def retranslateUi(self, Save):
        Save.setWindowTitle(QtGui.QApplication.translate("Save", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_2.setText(QtGui.QApplication.translate("Save", "Save files automatically every", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBox.setSuffix(QtGui.QApplication.translate("Save", " mins", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Save", "Backup prefix", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit.setText(QtGui.QApplication.translate("Save", ".", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Save", "Backup postfix", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_2.setText(QtGui.QApplication.translate("Save", "~", None, QtGui.QApplication.UnicodeUTF8))

import res_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Save = QtGui.QWidget()
    ui = Ui_Save()
    ui.setupUi(Save)
    Save.show()
    sys.exit(app.exec_())

