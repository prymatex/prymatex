# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/sda5/Projects/Prymatex/prymatex/resources/ui/dialogs/template.ui'
#
# Created: Wed Oct 22 18:41:35 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TemplateDialog(object):
    def setupUi(self, TemplateDialog):
        TemplateDialog.setObjectName("TemplateDialog")
        TemplateDialog.setWindowModality(QtCore.Qt.WindowModal)
        TemplateDialog.resize(600, 130)
        TemplateDialog.setMinimumSize(QtCore.QSize(600, 0))
        self.verticalLayout = QtWidgets.QVBoxLayout(TemplateDialog)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout_2.setSpacing(2)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label1 = QtWidgets.QLabel(TemplateDialog)
        self.label1.setObjectName("label1")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label1)
        self.lineFileName = QtWidgets.QLineEdit(TemplateDialog)
        self.lineFileName.setObjectName("lineFileName")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineFileName)
        self.label2 = QtWidgets.QLabel(TemplateDialog)
        self.label2.setObjectName("label2")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.lineLocation = QtWidgets.QLineEdit(TemplateDialog)
        self.lineLocation.setObjectName("lineLocation")
        self.horizontalLayout_5.addWidget(self.lineLocation)
        self.buttonChoose = QtWidgets.QPushButton(TemplateDialog)
        icon = QtGui.QIcon.fromTheme("folder")
        self.buttonChoose.setIcon(icon)
        self.buttonChoose.setObjectName("buttonChoose")
        self.horizontalLayout_5.addWidget(self.buttonChoose)
        self.formLayout_2.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_5)
        self.label3 = QtWidgets.QLabel(TemplateDialog)
        self.label3.setObjectName("label3")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label3)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.comboTemplates = QtWidgets.QComboBox(TemplateDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboTemplates.sizePolicy().hasHeightForWidth())
        self.comboTemplates.setSizePolicy(sizePolicy)
        self.comboTemplates.setObjectName("comboTemplates")
        self.horizontalLayout_3.addWidget(self.comboTemplates)
        self.buttonEnvironment = QtWidgets.QPushButton(TemplateDialog)
        self.buttonEnvironment.setMaximumSize(QtCore.QSize(32, 16777215))
        self.buttonEnvironment.setText("")
        icon = QtGui.QIcon.fromTheme("code-variable")
        self.buttonEnvironment.setIcon(icon)
        self.buttonEnvironment.setObjectName("buttonEnvironment")
        self.horizontalLayout_3.addWidget(self.buttonEnvironment)
        self.formLayout_2.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.verticalLayout.addLayout(self.formLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.buttonCreate = QtWidgets.QPushButton(TemplateDialog)
        icon = QtGui.QIcon.fromTheme("document-new")
        self.buttonCreate.setIcon(icon)
        self.buttonCreate.setObjectName("buttonCreate")
        self.horizontalLayout.addWidget(self.buttonCreate)
        self.buttonCancel = QtWidgets.QPushButton(TemplateDialog)
        icon = QtGui.QIcon.fromTheme("dialog-cancel")
        self.buttonCancel.setIcon(icon)
        self.buttonCancel.setObjectName("buttonCancel")
        self.horizontalLayout.addWidget(self.buttonCancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(TemplateDialog)
        self.buttonCancel.clicked.connect(TemplateDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TemplateDialog)
        TemplateDialog.setTabOrder(self.lineFileName, self.lineLocation)
        TemplateDialog.setTabOrder(self.lineLocation, self.buttonChoose)
        TemplateDialog.setTabOrder(self.buttonChoose, self.buttonCreate)

    def retranslateUi(self, TemplateDialog):
        _translate = QtCore.QCoreApplication.translate
        self.label1.setText(_translate("TemplateDialog", "File Name:"))
        self.label2.setText(_translate("TemplateDialog", "Location:"))
        self.buttonChoose.setText(_translate("TemplateDialog", "Ch&oose"))
        self.label3.setText(_translate("TemplateDialog", "Template:"))
        self.buttonCreate.setText(_translate("TemplateDialog", "&Create"))
        self.buttonCancel.setText(_translate("TemplateDialog", "C&ancel"))

