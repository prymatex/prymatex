# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/template.ui'
#
# Created: Thu Jun  2 22:28:21 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Template(object):
    def setupUi(self, Template):
        Template.setObjectName(_fromUtf8("Template"))
        Template.resize(361, 237)
        self.formLayout_2 = QtGui.QFormLayout(Template)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout_2.setMargin(0)
        self.formLayout_2.setSpacing(2)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label = QtGui.QLabel(Template)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lineEditExtension = QtGui.QLineEdit(Template)
        self.lineEditExtension.setObjectName(_fromUtf8("lineEditExtension"))
        self.horizontalLayout_2.addWidget(self.lineEditExtension)
        self.formLayout_2.setLayout(0, QtGui.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.label_2 = QtGui.QLabel(Template)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.command = QtGui.QPlainTextEdit(Template)
        self.command.setObjectName(_fromUtf8("command"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.command)
        self.label_4 = QtGui.QLabel(Template)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_4)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.comboBoxOutput = QtGui.QComboBox(Template)
        self.comboBoxOutput.setObjectName(_fromUtf8("comboBoxOutput"))
        self.horizontalLayout_3.addWidget(self.comboBoxOutput)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.formLayout_2.setLayout(2, QtGui.QFormLayout.FieldRole, self.horizontalLayout_3)

        self.retranslateUi(Template)
        QtCore.QMetaObject.connectSlotsByName(Template)

    def retranslateUi(self, Template):
        Template.setWindowTitle(QtGui.QApplication.translate("Template", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Template", "Extension:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Template", "Command(s):", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Template", "Output:", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Template = QtGui.QWidget()
    ui = Ui_Template()
    ui.setupUi(Template)
    Template.show()
    sys.exit(app.exec_())
