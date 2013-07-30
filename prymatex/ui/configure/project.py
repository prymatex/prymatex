# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/likewise-open/SUPTRIB/dvanhaaster/Workspace/prymatex/resources/ui/configure/project.ui'
#
# Created: Tue Jul 30 11:11:59 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Project(object):
    def setupUi(self, Project):
        Project.setObjectName(_fromUtf8("Project"))
        Project.resize(400, 300)
        self.formLayout = QtGui.QFormLayout(Project)
        self.formLayout.setMargin(0)
        self.formLayout.setSpacing(2)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label1 = QtGui.QLabel(Project)
        self.label1.setObjectName(_fromUtf8("label1"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label1)
        self.lineProjectName = QtGui.QLineEdit(Project)
        self.lineProjectName.setObjectName(_fromUtf8("lineProjectName"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineProjectName)
        self.label = QtGui.QLabel(Project)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.textDescription = QtGui.QTextEdit(Project)
        self.textDescription.setObjectName(_fromUtf8("textDescription"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.textDescription)
        self.label3 = QtGui.QLabel(Project)
        self.label3.setObjectName(_fromUtf8("label3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label3)
        self.comboBoxKeywords = QtGui.QComboBox(Project)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxKeywords.sizePolicy().hasHeightForWidth())
        self.comboBoxKeywords.setSizePolicy(sizePolicy)
        self.comboBoxKeywords.setEditable(True)
        self.comboBoxKeywords.setObjectName(_fromUtf8("comboBoxKeywords"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.comboBoxKeywords)
        self.label_3 = QtGui.QLabel(Project)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_3)
        self.comboBoxLicence = QtGui.QComboBox(Project)
        self.comboBoxLicence.setObjectName(_fromUtf8("comboBoxLicence"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.comboBoxLicence)
        self.label2 = QtGui.QLabel(Project)
        self.label2.setObjectName(_fromUtf8("label2"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label2)
        self.textLabelLocation = QtGui.QLabel(Project)
        self.textLabelLocation.setText(_fromUtf8(""))
        self.textLabelLocation.setObjectName(_fromUtf8("textLabelLocation"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.textLabelLocation)

        self.retranslateUi(Project)
        QtCore.QMetaObject.connectSlotsByName(Project)

    def retranslateUi(self, Project):
        Project.setWindowTitle(QtGui.QApplication.translate("Project", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label1.setText(QtGui.QApplication.translate("Project", "Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Project", "Description:", None, QtGui.QApplication.UnicodeUTF8))
        self.label3.setText(QtGui.QApplication.translate("Project", "Keywords:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Project", "Licence:", None, QtGui.QApplication.UnicodeUTF8))
        self.label2.setText(QtGui.QApplication.translate("Project", "Location:", None, QtGui.QApplication.UnicodeUTF8))

