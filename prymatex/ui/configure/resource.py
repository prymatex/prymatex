# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/configure/resource.ui'
#
# Created: Mon Aug 27 13:36:45 2012
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ResouceWidget(object):
    def setupUi(self, ResouceWidget):
        ResouceWidget.setObjectName(_fromUtf8("ResouceWidget"))
        ResouceWidget.resize(314, 221)
        self._2 = QtGui.QVBoxLayout(ResouceWidget)
        self._2.setSpacing(2)
        self._2.setMargin(0)
        self._2.setObjectName(_fromUtf8("_2"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setHorizontalSpacing(2)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.labelPath = QtGui.QLabel(ResouceWidget)
        self.labelPath.setObjectName(_fromUtf8("labelPath"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.labelPath)
        self.labelType = QtGui.QLabel(ResouceWidget)
        self.labelType.setObjectName(_fromUtf8("labelType"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.labelType)
        self.labelLocation = QtGui.QLabel(ResouceWidget)
        self.labelLocation.setObjectName(_fromUtf8("labelLocation"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.labelLocation)
        self.labelLastModified = QtGui.QLabel(ResouceWidget)
        self.labelLastModified.setObjectName(_fromUtf8("labelLastModified"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.labelLastModified)
        self.textLabelPath = QtGui.QLabel(ResouceWidget)
        self.textLabelPath.setText(_fromUtf8(""))
        self.textLabelPath.setObjectName(_fromUtf8("textLabelPath"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.textLabelPath)
        self.textLabelType = QtGui.QLabel(ResouceWidget)
        self.textLabelType.setText(_fromUtf8(""))
        self.textLabelType.setObjectName(_fromUtf8("textLabelType"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.textLabelType)
        self.textLabelLocation = QtGui.QLabel(ResouceWidget)
        self.textLabelLocation.setText(_fromUtf8(""))
        self.textLabelLocation.setObjectName(_fromUtf8("textLabelLocation"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.textLabelLocation)
        self.textLabelLastModified = QtGui.QLabel(ResouceWidget)
        self.textLabelLastModified.setText(_fromUtf8(""))
        self.textLabelLastModified.setObjectName(_fromUtf8("textLabelLastModified"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.textLabelLastModified)
        self._2.addLayout(self.formLayout)

        self.retranslateUi(ResouceWidget)
        QtCore.QMetaObject.connectSlotsByName(ResouceWidget)

    def retranslateUi(self, ResouceWidget):
        ResouceWidget.setWindowTitle(_('Resource'))
        self.labelPath.setText(_('Path:'))
        self.labelType.setText(_('Type:'))
        self.labelLocation.setText(_('Location:'))
        self.labelLastModified.setText(_('Last modified:'))

