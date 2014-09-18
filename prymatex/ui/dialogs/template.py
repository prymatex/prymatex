# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/dialogs/template.ui'
#
# Created: Thu Sep 18 10:11:59 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_TemplateDialog(object):
    def setupUi(self, TemplateDialog):
        TemplateDialog.setObjectName(_fromUtf8("TemplateDialog"))
        TemplateDialog.setWindowModality(QtCore.Qt.WindowModal)
        TemplateDialog.resize(600, 130)
        TemplateDialog.setMinimumSize(QtCore.QSize(600, 0))
        self.verticalLayout = QtGui.QVBoxLayout(TemplateDialog)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout_2.setSpacing(2)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label1 = QtGui.QLabel(TemplateDialog)
        self.label1.setObjectName(_fromUtf8("label1"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label1)
        self.lineFileName = QtGui.QLineEdit(TemplateDialog)
        self.lineFileName.setObjectName(_fromUtf8("lineFileName"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineFileName)
        self.label2 = QtGui.QLabel(TemplateDialog)
        self.label2.setObjectName(_fromUtf8("label2"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label2)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.lineLocation = QtGui.QLineEdit(TemplateDialog)
        self.lineLocation.setObjectName(_fromUtf8("lineLocation"))
        self.horizontalLayout_5.addWidget(self.lineLocation)
        self.buttonChoose = QtGui.QPushButton(TemplateDialog)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("folder"))
        self.buttonChoose.setIcon(icon)
        self.buttonChoose.setObjectName(_fromUtf8("buttonChoose"))
        self.horizontalLayout_5.addWidget(self.buttonChoose)
        self.formLayout_2.setLayout(1, QtGui.QFormLayout.FieldRole, self.horizontalLayout_5)
        self.label3 = QtGui.QLabel(TemplateDialog)
        self.label3.setObjectName(_fromUtf8("label3"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label3)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.comboTemplates = QtGui.QComboBox(TemplateDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboTemplates.sizePolicy().hasHeightForWidth())
        self.comboTemplates.setSizePolicy(sizePolicy)
        self.comboTemplates.setObjectName(_fromUtf8("comboTemplates"))
        self.horizontalLayout_3.addWidget(self.comboTemplates)
        self.buttonEnvironment = QtGui.QPushButton(TemplateDialog)
        self.buttonEnvironment.setMaximumSize(QtCore.QSize(32, 16777215))
        self.buttonEnvironment.setText(_fromUtf8(""))
        icon = QtGui.QIcon.fromTheme(_fromUtf8("code-variable"))
        self.buttonEnvironment.setIcon(icon)
        self.buttonEnvironment.setObjectName(_fromUtf8("buttonEnvironment"))
        self.horizontalLayout_3.addWidget(self.buttonEnvironment)
        self.formLayout_2.setLayout(2, QtGui.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.verticalLayout.addLayout(self.formLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.buttonCreate = QtGui.QPushButton(TemplateDialog)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("document-new"))
        self.buttonCreate.setIcon(icon)
        self.buttonCreate.setObjectName(_fromUtf8("buttonCreate"))
        self.horizontalLayout.addWidget(self.buttonCreate)
        self.buttonCancel = QtGui.QPushButton(TemplateDialog)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("dialog-cancel"))
        self.buttonCancel.setIcon(icon)
        self.buttonCancel.setObjectName(_fromUtf8("buttonCancel"))
        self.horizontalLayout.addWidget(self.buttonCancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(TemplateDialog)
        QtCore.QObject.connect(self.buttonCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), TemplateDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TemplateDialog)
        TemplateDialog.setTabOrder(self.lineFileName, self.lineLocation)
        TemplateDialog.setTabOrder(self.lineLocation, self.buttonChoose)
        TemplateDialog.setTabOrder(self.buttonChoose, self.buttonCreate)

    def retranslateUi(self, TemplateDialog):
        self.label1.setText(_translate("TemplateDialog", "File Name:", None))
        self.label2.setText(_translate("TemplateDialog", "Location:", None))
        self.buttonChoose.setText(_translate("TemplateDialog", "Ch&oose", None))
        self.label3.setText(_translate("TemplateDialog", "Template:", None))
        self.buttonCreate.setText(_translate("TemplateDialog", "&Create", None))
        self.buttonCancel.setText(_translate("TemplateDialog", "C&ancel", None))

