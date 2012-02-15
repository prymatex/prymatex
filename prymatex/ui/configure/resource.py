# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/configure/resource.ui'
#
# Created: Tue Feb 14 15:51:26 2012
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.labelPath = QtGui.QLabel(Form)
        self.labelPath.setObjectName(_fromUtf8("labelPath"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.labelPath)
        self.labelType = QtGui.QLabel(Form)
        self.labelType.setObjectName(_fromUtf8("labelType"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.labelType)
        self.labelLocation = QtGui.QLabel(Form)
        self.labelLocation.setObjectName(_fromUtf8("labelLocation"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.labelLocation)
        self.labelLastModified = QtGui.QLabel(Form)
        self.labelLastModified.setObjectName(_fromUtf8("labelLastModified"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.labelLastModified)
        self.textLabelPath = QtGui.QLabel(Form)
        self.textLabelPath.setText(_fromUtf8(""))
        self.textLabelPath.setObjectName(_fromUtf8("textLabelPath"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.textLabelPath)
        self.textLabelType = QtGui.QLabel(Form)
        self.textLabelType.setText(_fromUtf8(""))
        self.textLabelType.setObjectName(_fromUtf8("textLabelType"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.textLabelType)
        self.textLabelLocation = QtGui.QLabel(Form)
        self.textLabelLocation.setText(_fromUtf8(""))
        self.textLabelLocation.setObjectName(_fromUtf8("textLabelLocation"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.textLabelLocation)
        self.textLabelLastModified = QtGui.QLabel(Form)
        self.textLabelLastModified.setText(_fromUtf8(""))
        self.textLabelLastModified.setObjectName(_fromUtf8("textLabelLastModified"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.textLabelLastModified)
        self.verticalLayout.addLayout(self.formLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_('Form'))
        self.labelPath.setText(_('Path:'))
        self.labelType.setText(_('Type:'))
        self.labelLocation.setText(_('Location:'))
        self.labelLastModified.setText(_('Last modified:'))

