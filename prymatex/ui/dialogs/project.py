# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/dialogs/project.ui'
#
# Created: Thu Sep 18 09:56:56 2014
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

class Ui_ProjectDialog(object):
    def setupUi(self, ProjectDialog):
        ProjectDialog.setObjectName(_fromUtf8("ProjectDialog"))
        ProjectDialog.setWindowModality(QtCore.Qt.WindowModal)
        ProjectDialog.resize(600, 443)
        ProjectDialog.setMinimumSize(QtCore.QSize(600, 400))
        self.verticalLayout = QtGui.QVBoxLayout(ProjectDialog)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label1 = QtGui.QLabel(ProjectDialog)
        self.label1.setObjectName(_fromUtf8("label1"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label1)
        self.line_2 = QtGui.QFrame(ProjectDialog)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.SpanningRole, self.line_2)
        self.lineProjectName = QtGui.QLineEdit(ProjectDialog)
        self.lineProjectName.setObjectName(_fromUtf8("lineProjectName"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineProjectName)
        self.checkBoxUseDefaultLocation = QtGui.QCheckBox(ProjectDialog)
        self.checkBoxUseDefaultLocation.setChecked(True)
        self.checkBoxUseDefaultLocation.setObjectName(_fromUtf8("checkBoxUseDefaultLocation"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.SpanningRole, self.checkBoxUseDefaultLocation)
        self.label2 = QtGui.QLabel(ProjectDialog)
        self.label2.setObjectName(_fromUtf8("label2"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label2)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.lineLocation = QtGui.QLineEdit(ProjectDialog)
        self.lineLocation.setEnabled(False)
        self.lineLocation.setObjectName(_fromUtf8("lineLocation"))
        self.horizontalLayout_5.addWidget(self.lineLocation)
        self.buttonChoose = QtGui.QPushButton(ProjectDialog)
        self.buttonChoose.setEnabled(False)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("folder"))
        self.buttonChoose.setIcon(icon)
        self.buttonChoose.setObjectName(_fromUtf8("buttonChoose"))
        self.horizontalLayout_5.addWidget(self.buttonChoose)
        self.formLayout.setLayout(2, QtGui.QFormLayout.FieldRole, self.horizontalLayout_5)
        self.label = QtGui.QLabel(ProjectDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label)
        self.textDescription = QtGui.QTextEdit(ProjectDialog)
        self.textDescription.setObjectName(_fromUtf8("textDescription"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.textDescription)
        self.line = QtGui.QFrame(ProjectDialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.SpanningRole, self.line)
        self.label3 = QtGui.QLabel(ProjectDialog)
        self.label3.setObjectName(_fromUtf8("label3"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label3)
        self.comboBoxKeywords = QtGui.QComboBox(ProjectDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxKeywords.sizePolicy().hasHeightForWidth())
        self.comboBoxKeywords.setSizePolicy(sizePolicy)
        self.comboBoxKeywords.setEditable(True)
        self.comboBoxKeywords.setObjectName(_fromUtf8("comboBoxKeywords"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.comboBoxKeywords)
        self.label_3 = QtGui.QLabel(ProjectDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_3)
        self.comboBoxLicence = QtGui.QComboBox(ProjectDialog)
        self.comboBoxLicence.setObjectName(_fromUtf8("comboBoxLicence"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.comboBoxLicence)
        self.checkBoxUseTemplate = QtGui.QCheckBox(ProjectDialog)
        self.checkBoxUseTemplate.setObjectName(_fromUtf8("checkBoxUseTemplate"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.SpanningRole, self.checkBoxUseTemplate)
        self.label_2 = QtGui.QLabel(ProjectDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(9, QtGui.QFormLayout.LabelRole, self.label_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.comboBoxTemplate = QtGui.QComboBox(ProjectDialog)
        self.comboBoxTemplate.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxTemplate.sizePolicy().hasHeightForWidth())
        self.comboBoxTemplate.setSizePolicy(sizePolicy)
        self.comboBoxTemplate.setObjectName(_fromUtf8("comboBoxTemplate"))
        self.horizontalLayout_3.addWidget(self.comboBoxTemplate)
        self.buttonEnvironment = QtGui.QPushButton(ProjectDialog)
        self.buttonEnvironment.setEnabled(False)
        self.buttonEnvironment.setMaximumSize(QtCore.QSize(32, 16777215))
        self.buttonEnvironment.setText(_fromUtf8(""))
        icon = QtGui.QIcon.fromTheme(_fromUtf8("code-variable"))
        self.buttonEnvironment.setIcon(icon)
        self.buttonEnvironment.setObjectName(_fromUtf8("buttonEnvironment"))
        self.horizontalLayout_3.addWidget(self.buttonEnvironment)
        self.formLayout.setLayout(9, QtGui.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.buttonCreate = QtGui.QPushButton(ProjectDialog)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("project-development-new-template"))
        self.buttonCreate.setIcon(icon)
        self.buttonCreate.setObjectName(_fromUtf8("buttonCreate"))
        self.horizontalLayout.addWidget(self.buttonCreate)
        self.buttonCancel = QtGui.QPushButton(ProjectDialog)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("dialog-cancel"))
        self.buttonCancel.setIcon(icon)
        self.buttonCancel.setObjectName(_fromUtf8("buttonCancel"))
        self.horizontalLayout.addWidget(self.buttonCancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ProjectDialog)
        QtCore.QObject.connect(self.buttonCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), ProjectDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ProjectDialog)
        ProjectDialog.setTabOrder(self.lineLocation, self.buttonChoose)
        ProjectDialog.setTabOrder(self.buttonChoose, self.buttonCreate)

    def retranslateUi(self, ProjectDialog):
        self.label1.setText(_translate("ProjectDialog", "Name:", None))
        self.checkBoxUseDefaultLocation.setText(_translate("ProjectDialog", "Use default location", None))
        self.label2.setText(_translate("ProjectDialog", "Location:", None))
        self.buttonChoose.setText(_translate("ProjectDialog", "Ch&oose", None))
        self.label.setText(_translate("ProjectDialog", "Description:", None))
        self.label3.setText(_translate("ProjectDialog", "Keywords:", None))
        self.label_3.setText(_translate("ProjectDialog", "Licence:", None))
        self.checkBoxUseTemplate.setText(_translate("ProjectDialog", "Use template", None))
        self.label_2.setText(_translate("ProjectDialog", "Template:", None))
        self.buttonCreate.setText(_translate("ProjectDialog", "&Create", None))
        self.buttonCancel.setText(_translate("ProjectDialog", "C&ancel", None))

