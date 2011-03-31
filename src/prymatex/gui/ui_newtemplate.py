# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/newtemplate.ui'
#
# Created: Thu Mar 31 09:44:49 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_NewFromTemplateDialog(object):
    def setupUi(self, NewFromTemplateDialog):
        NewFromTemplateDialog.setObjectName("NewFromTemplateDialog")
        NewFromTemplateDialog.setWindowModality(QtCore.Qt.WindowModal)
        NewFromTemplateDialog.resize(450, 115)
        self.verticalLayout = QtGui.QVBoxLayout(NewFromTemplateDialog)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_3 = QtGui.QLabel(NewFromTemplateDialog)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.label_2 = QtGui.QLabel(NewFromTemplateDialog)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.lineLocation = QtGui.QLineEdit(NewFromTemplateDialog)
        self.lineLocation.setObjectName("lineLocation")
        self.horizontalLayout_5.addWidget(self.lineLocation)
        self.buttonChoose = QtGui.QPushButton(NewFromTemplateDialog)
        self.buttonChoose.setObjectName("buttonChoose")
        self.horizontalLayout_5.addWidget(self.buttonChoose)
        self.formLayout_2.setLayout(1, QtGui.QFormLayout.FieldRole, self.horizontalLayout_5)
        self.label = QtGui.QLabel(NewFromTemplateDialog)
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.lineFileName = QtGui.QLineEdit(NewFromTemplateDialog)
        self.lineFileName.setObjectName("lineFileName")
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineFileName)
        self.comboTemplates = QtGui.QComboBox(NewFromTemplateDialog)
        self.comboTemplates.setObjectName("comboTemplates")
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.comboTemplates)
        self.verticalLayout.addLayout(self.formLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.buttonCancel = QtGui.QPushButton(NewFromTemplateDialog)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/actions/resources/actions/process-stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonCancel.setIcon(icon)
        self.buttonCancel.setObjectName("buttonCancel")
        self.horizontalLayout.addWidget(self.buttonCancel)
        self.buttonCreate = QtGui.QPushButton(NewFromTemplateDialog)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/actions/resources/actions/document-new.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonCreate.setIcon(icon1)
        self.buttonCreate.setObjectName("buttonCreate")
        self.horizontalLayout.addWidget(self.buttonCreate)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(NewFromTemplateDialog)
        QtCore.QObject.connect(self.buttonCancel, QtCore.SIGNAL("clicked()"), NewFromTemplateDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewFromTemplateDialog)
        NewFromTemplateDialog.setTabOrder(self.lineFileName, self.lineLocation)
        NewFromTemplateDialog.setTabOrder(self.lineLocation, self.comboTemplates)
        NewFromTemplateDialog.setTabOrder(self.comboTemplates, self.buttonChoose)
        NewFromTemplateDialog.setTabOrder(self.buttonChoose, self.buttonCreate)
        NewFromTemplateDialog.setTabOrder(self.buttonCreate, self.buttonCancel)

    def retranslateUi(self, NewFromTemplateDialog):
        NewFromTemplateDialog.setWindowTitle(QtGui.QApplication.translate("NewFromTemplateDialog", "New From Template", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("NewFromTemplateDialog", "Template:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("NewFromTemplateDialog", "Location:", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonChoose.setText(QtGui.QApplication.translate("NewFromTemplateDialog", "Ch&oose", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("NewFromTemplateDialog", "File Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonCancel.setText(QtGui.QApplication.translate("NewFromTemplateDialog", "C&ancel", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonCreate.setText(QtGui.QApplication.translate("NewFromTemplateDialog", "&Create", None, QtGui.QApplication.UnicodeUTF8))

import res_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    NewFromTemplateDialog = QtGui.QDialog()
    ui = Ui_NewFromTemplateDialog()
    ui.setupUi(NewFromTemplateDialog)
    NewFromTemplateDialog.show()
    sys.exit(app.exec_())

