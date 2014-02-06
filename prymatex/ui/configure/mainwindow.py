# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/likewise-open/SUPTRIB/dvanhaaster/Workspace/prymatex/resources/ui/configure/mainwindow.ui'
#
# Created: Thu Feb  6 11:09:58 2014
#      by: PyQt4 UI code generator 4.10.3
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(451, 333)
        self.verticalLayout = QtGui.QVBoxLayout(MainWindow)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox_2 = QtGui.QGroupBox(MainWindow)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.formLayout_2 = QtGui.QFormLayout(self.groupBox_2)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_2.setMargin(6)
        self.formLayout_2.setSpacing(2)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.comboBoxTabTemplate = QtGui.QComboBox(self.groupBox_2)
        self.comboBoxTabTemplate.setEditable(True)
        self.comboBoxTabTemplate.setObjectName(_fromUtf8("comboBoxTabTemplate"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.comboBoxTabTemplate)
        self.labelTabVisibility = QtGui.QLabel(self.groupBox_2)
        self.labelTabVisibility.setObjectName(_fromUtf8("labelTabVisibility"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.labelTabVisibility)
        self.comboBoxTabVisibility = QtGui.QComboBox(self.groupBox_2)
        self.comboBoxTabVisibility.setObjectName(_fromUtf8("comboBoxTabVisibility"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.comboBoxTabVisibility)
        self.verticalLayout.addWidget(self.groupBox_2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "General", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "Interface", None))
        self.label_2.setText(_translate("MainWindow", "Title template:", None))
        self.labelTabVisibility.setText(_translate("MainWindow", "Tab visibilty:", None))

