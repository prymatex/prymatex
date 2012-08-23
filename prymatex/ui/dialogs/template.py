# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/dialogs/template.ui'
#
# Created: Thu Aug 23 00:38:08 2012
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_NewFromTemplateDialog(object):
    def setupUi(self, NewFromTemplateDialog):
        NewFromTemplateDialog.setObjectName(_fromUtf8("NewFromTemplateDialog"))
        NewFromTemplateDialog.setWindowModality(QtCore.Qt.WindowModal)
        NewFromTemplateDialog.resize(450, 117)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/prymatex/logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        NewFromTemplateDialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(NewFromTemplateDialog)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label1 = QtGui.QLabel(NewFromTemplateDialog)
        self.label1.setObjectName(_fromUtf8("label1"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label1)
        self.lineFileName = QtGui.QLineEdit(NewFromTemplateDialog)
        self.lineFileName.setObjectName(_fromUtf8("lineFileName"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineFileName)
        self.label2 = QtGui.QLabel(NewFromTemplateDialog)
        self.label2.setObjectName(_fromUtf8("label2"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label2)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.lineLocation = QtGui.QLineEdit(NewFromTemplateDialog)
        self.lineLocation.setObjectName(_fromUtf8("lineLocation"))
        self.horizontalLayout_5.addWidget(self.lineLocation)
        self.buttonChoose = QtGui.QPushButton(NewFromTemplateDialog)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("folder"))
        self.buttonChoose.setIcon(icon)
        self.buttonChoose.setObjectName(_fromUtf8("buttonChoose"))
        self.horizontalLayout_5.addWidget(self.buttonChoose)
        self.formLayout_2.setLayout(1, QtGui.QFormLayout.FieldRole, self.horizontalLayout_5)
        self.label3 = QtGui.QLabel(NewFromTemplateDialog)
        self.label3.setObjectName(_fromUtf8("label3"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label3)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.comboTemplates = QtGui.QComboBox(NewFromTemplateDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboTemplates.sizePolicy().hasHeightForWidth())
        self.comboTemplates.setSizePolicy(sizePolicy)
        self.comboTemplates.setObjectName(_fromUtf8("comboTemplates"))
        self.horizontalLayout_3.addWidget(self.comboTemplates)
        self.buttonEnvironment = QtGui.QPushButton(NewFromTemplateDialog)
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
        self.buttonCreate = QtGui.QPushButton(NewFromTemplateDialog)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("document-new"))
        self.buttonCreate.setIcon(icon)
        self.buttonCreate.setObjectName(_fromUtf8("buttonCreate"))
        self.horizontalLayout.addWidget(self.buttonCreate)
        self.buttonCancel = QtGui.QPushButton(NewFromTemplateDialog)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("dialog-cancel"))
        self.buttonCancel.setIcon(icon)
        self.buttonCancel.setObjectName(_fromUtf8("buttonCancel"))
        self.horizontalLayout.addWidget(self.buttonCancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(NewFromTemplateDialog)
        QtCore.QObject.connect(self.buttonCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), NewFromTemplateDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewFromTemplateDialog)
        NewFromTemplateDialog.setTabOrder(self.lineFileName, self.lineLocation)
        NewFromTemplateDialog.setTabOrder(self.lineLocation, self.buttonChoose)
        NewFromTemplateDialog.setTabOrder(self.buttonChoose, self.buttonCreate)

    def retranslateUi(self, NewFromTemplateDialog):
        NewFromTemplateDialog.setWindowTitle(_('New From Template'))
        self.label1.setText(_('File Name:'))
        self.label2.setText(_('Location:'))
        self.buttonChoose.setText(_('Ch&oose'))
        self.label3.setText(_('Template:'))
        self.buttonCreate.setText(_('&Create'))
        self.buttonCancel.setText(_('C&ancel'))

from prymatex import resources_rc
