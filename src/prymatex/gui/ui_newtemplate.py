# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/newtemplate.ui'
#
# Created: Tue Mar 15 18:51:02 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_NewFromTemplateDialog(object):
    def setupUi(self, NewFromTemplateDialog):
        NewFromTemplateDialog.setObjectName(_fromUtf8("NewFromTemplateDialog"))
        NewFromTemplateDialog.resize(467, 113)
        self.verticalLayout = QtGui.QVBoxLayout(NewFromTemplateDialog)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_3 = QtGui.QLabel(NewFromTemplateDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.label_2 = QtGui.QLabel(NewFromTemplateDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.lineEdit_2 = QtGui.QLineEdit(NewFromTemplateDialog)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.horizontalLayout_5.addWidget(self.lineEdit_2)
        self.buttonChoose = QtGui.QPushButton(NewFromTemplateDialog)
        self.buttonChoose.setObjectName(_fromUtf8("buttonChoose"))
        self.horizontalLayout_5.addWidget(self.buttonChoose)
        self.formLayout_2.setLayout(1, QtGui.QFormLayout.FieldRole, self.horizontalLayout_5)
        self.label = QtGui.QLabel(NewFromTemplateDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.lineEdit = QtGui.QLineEdit(NewFromTemplateDialog)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEdit)
        self.comboBox = QtGui.QComboBox(NewFromTemplateDialog)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.comboBox)
        self.verticalLayout.addLayout(self.formLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.buttonCancel = QtGui.QPushButton(NewFromTemplateDialog)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/resources/actions/process-stop.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonCancel.setIcon(icon)
        self.buttonCancel.setObjectName(_fromUtf8("buttonCancel"))
        self.horizontalLayout.addWidget(self.buttonCancel)
        self.buttonCreate = QtGui.QPushButton(NewFromTemplateDialog)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/resources/actions/edit-delete.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonCreate.setIcon(icon1)
        self.buttonCreate.setObjectName(_fromUtf8("buttonCreate"))
        self.horizontalLayout.addWidget(self.buttonCreate)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(NewFromTemplateDialog)
        QtCore.QObject.connect(self.buttonCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), NewFromTemplateDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewFromTemplateDialog)

    def retranslateUi(self, NewFromTemplateDialog):
        NewFromTemplateDialog.setWindowTitle(QtGui.QApplication.translate("NewFromTemplateDialog", "New From Template", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("NewFromTemplateDialog", "Template:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("NewFromTemplateDialog", "Location:", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonChoose.setText(QtGui.QApplication.translate("NewFromTemplateDialog", "Choose", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("NewFromTemplateDialog", "File Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonCancel.setText(QtGui.QApplication.translate("NewFromTemplateDialog", "&Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonCreate.setText(QtGui.QApplication.translate("NewFromTemplateDialog", "Create", None, QtGui.QApplication.UnicodeUTF8))

import res_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    NewFromTemplateDialog = QtGui.QDialog()
    ui = Ui_NewFromTemplateDialog()
    ui.setupUi(NewFromTemplateDialog)
    NewFromTemplateDialog.show()
    sys.exit(app.exec_())

