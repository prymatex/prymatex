# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/dragcommand.ui'
#
# Created: Tue May 31 18:51:24 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DragCommand(object):
    def setupUi(self, DragCommand):
        DragCommand.setObjectName(_fromUtf8("DragCommand"))
        DragCommand.resize(361, 237)
        self.formLayout_2 = QtGui.QFormLayout(DragCommand)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout_2.setMargin(0)
        self.formLayout_2.setSpacing(2)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label = QtGui.QLabel(DragCommand)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.formLayout_2.setLayout(0, QtGui.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.label_2 = QtGui.QLabel(DragCommand)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.plainTextEdit = QtGui.QPlainTextEdit(DragCommand)
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.plainTextEdit)
        self.label_4 = QtGui.QLabel(DragCommand)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_4)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.comboBox_4 = QtGui.QComboBox(DragCommand)
        self.comboBox_4.setObjectName(_fromUtf8("comboBox_4"))
        self.comboBox_4.addItem(_fromUtf8(""))
        self.horizontalLayout_3.addWidget(self.comboBox_4)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.formLayout_2.setLayout(2, QtGui.QFormLayout.FieldRole, self.horizontalLayout_3)

        self.retranslateUi(DragCommand)
        QtCore.QMetaObject.connectSlotsByName(DragCommand)

    def retranslateUi(self, DragCommand):
        DragCommand.setWindowTitle(QtGui.QApplication.translate("DragCommand", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DragCommand", "File Types:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("DragCommand", "Command(s):", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("DragCommand", "Output:", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_4.setItemText(0, QtGui.QApplication.translate("DragCommand", "Insert as Snippet", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    DragCommand = QtGui.QWidget()
    ui = Ui_DragCommand()
    ui.setupUi(DragCommand)
    DragCommand.show()
    sys.exit(app.exec_())

