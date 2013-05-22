# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/datos/workspace/Prymatex/prymatex/resources/ui/configure/project.ui'
#
# Created: Wed May 22 20:00:29 2013
#      by: PyQt4 UI code generator snapshot-4.10.2-6f54723ef2ba
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
        Project.setWindowTitle(_translate("Project", "Form", None))
        self.label1.setText(_translate("Project", "Name:", None))
        self.label.setText(_translate("Project", "Description:", None))
        self.label3.setText(_translate("Project", "Keywords:", None))
        self.label_3.setText(_translate("Project", "Licence:", None))
        self.label2.setText(_translate("Project", "Location:", None))

