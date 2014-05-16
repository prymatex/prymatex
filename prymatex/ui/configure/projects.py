# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/datos/workspace/Prymatex/prymatex/resources/ui/configure/projects.ui'
#
# Created: Fri May 16 17:31:45 2014
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

class Ui_Projects(object):
    def setupUi(self, Projects):
        Projects.setObjectName(_fromUtf8("Projects"))
        Projects.resize(272, 281)
        self.verticalLayout = QtGui.QVBoxLayout(Projects)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox_3 = QtGui.QGroupBox(Projects)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.formLayout_3 = QtGui.QFormLayout(self.groupBox_3)
        self.formLayout_3.setMargin(6)
        self.formLayout_3.setSpacing(2)
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.label = QtGui.QLabel(self.groupBox_3)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.lineLocation_2 = QtGui.QLineEdit(self.groupBox_3)
        self.lineLocation_2.setEnabled(False)
        self.lineLocation_2.setObjectName(_fromUtf8("lineLocation_2"))
        self.horizontalLayout_6.addWidget(self.lineLocation_2)
        self.buttonChoose_2 = QtGui.QPushButton(self.groupBox_3)
        self.buttonChoose_2.setEnabled(False)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("folder"))
        self.buttonChoose_2.setIcon(icon)
        self.buttonChoose_2.setObjectName(_fromUtf8("buttonChoose_2"))
        self.horizontalLayout_6.addWidget(self.buttonChoose_2)
        self.formLayout_3.setLayout(0, QtGui.QFormLayout.FieldRole, self.horizontalLayout_6)
        self.label_3 = QtGui.QLabel(self.groupBox_3)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_3)
        self.comboBoxLicence = QtGui.QComboBox(self.groupBox_3)
        self.comboBoxLicence.setObjectName(_fromUtf8("comboBoxLicence"))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.FieldRole, self.comboBoxLicence)
        self.verticalLayout.addWidget(self.groupBox_3)
        spacerItem = QtGui.QSpacerItem(20, 4, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Projects)
        QtCore.QMetaObject.connectSlotsByName(Projects)

    def retranslateUi(self, Projects):
        Projects.setWindowTitle(_translate("Projects", "Projects", None))
        self.groupBox_3.setTitle(_translate("Projects", "Defaults", None))
        self.label.setText(_translate("Projects", "Location:", None))
        self.buttonChoose_2.setText(_translate("Projects", "Ch&oose", None))
        self.label_3.setText(_translate("Projects", "Licence:", None))

