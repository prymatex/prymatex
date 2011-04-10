# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/save.ui'
#
# Created: Sat Apr  9 13:53:21 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Save(object):
    def setupUi(self, Save):
        Save.setObjectName("Save")
        Save.setEnabled(True)
        Save.resize(400, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/actions/resources/actions/document-save-all.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Save.setWindowIcon(icon)
        self.formLayout = QtGui.QFormLayout(Save)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(Save)
        self.label.setObjectName("label")
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label)
        self.lineBackupPrefix = QtGui.QLineEdit(Save)
        self.lineBackupPrefix.setEnabled(False)
        self.lineBackupPrefix.setObjectName("lineBackupPrefix")
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.lineBackupPrefix)
        self.label_2 = QtGui.QLabel(Save)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.label_2)
        self.lineBackupPostfix = QtGui.QLineEdit(Save)
        self.lineBackupPostfix.setEnabled(False)
        self.lineBackupPostfix.setObjectName("lineBackupPostfix")
        self.formLayout.setWidget(7, QtGui.QFormLayout.FieldRole, self.lineBackupPostfix)
        self.label_3 = QtGui.QLabel(Save)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(9, QtGui.QFormLayout.LabelRole, self.label_3)
        self.comboEncodings = QtGui.QComboBox(Save)
        self.comboEncodings.setObjectName("comboEncodings")
        self.formLayout.setWidget(9, QtGui.QFormLayout.FieldRole, self.comboEncodings)
        self.label_4 = QtGui.QLabel(Save)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(11, QtGui.QFormLayout.LabelRole, self.label_4)
        self.comboBox = QtGui.QComboBox(Save)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.formLayout.setWidget(11, QtGui.QFormLayout.FieldRole, self.comboBox)
        self.checkBox = QtGui.QCheckBox(Save)
        self.checkBox.setObjectName("checkBox")
        self.formLayout.setWidget(12, QtGui.QFormLayout.FieldRole, self.checkBox)
        self.checkBox_3 = QtGui.QCheckBox(Save)
        self.checkBox_3.setObjectName("checkBox_3")
        self.formLayout.setWidget(10, QtGui.QFormLayout.FieldRole, self.checkBox_3)
        self.checkAutoSave = QtGui.QCheckBox(Save)
        self.checkAutoSave.setObjectName("checkAutoSave")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.checkAutoSave)
        self.spinSaveInterval = QtGui.QSpinBox(Save)
        self.spinSaveInterval.setEnabled(False)
        self.spinSaveInterval.setMaximum(120)
        self.spinSaveInterval.setObjectName("spinSaveInterval")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.spinSaveInterval)
        self.checkBox_4 = QtGui.QCheckBox(Save)
        self.checkBox_4.setEnabled(True)
        self.checkBox_4.setObjectName("checkBox_4")
        self.formLayout.setWidget(8, QtGui.QFormLayout.FieldRole, self.checkBox_4)

        self.retranslateUi(Save)
        QtCore.QObject.connect(self.checkAutoSave, QtCore.SIGNAL("toggled(bool)"), self.spinSaveInterval.setEnabled)
        QtCore.QObject.connect(self.checkAutoSave, QtCore.SIGNAL("toggled(bool)"), self.lineBackupPrefix.setEnabled)
        QtCore.QObject.connect(self.checkAutoSave, QtCore.SIGNAL("toggled(bool)"), self.lineBackupPostfix.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(Save)

    def retranslateUi(self, Save):
        Save.setWindowTitle(QtGui.QApplication.translate("Save", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Save", "Backup prefix", None, QtGui.QApplication.UnicodeUTF8))
        self.lineBackupPrefix.setText(QtGui.QApplication.translate("Save", ".", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Save", "Backup postfix", None, QtGui.QApplication.UnicodeUTF8))
        self.lineBackupPostfix.setText(QtGui.QApplication.translate("Save", "~", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Save", "Default encoding", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Save", "Line Ending", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(0, QtGui.QApplication.translate("Save", "LF (recommended)", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(1, QtGui.QApplication.translate("Save", "CR + LF", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("Save", "Use for existing files as well", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_3.setText(QtGui.QApplication.translate("Save", "Use for existing files as well", None, QtGui.QApplication.UnicodeUTF8))
        self.checkAutoSave.setText(QtGui.QApplication.translate("Save", "Automaitcally save", None, QtGui.QApplication.UnicodeUTF8))
        self.spinSaveInterval.setSuffix(QtGui.QApplication.translate("Save", " mins", None, QtGui.QApplication.UnicodeUTF8))
        self.spinSaveInterval.setPrefix(QtGui.QApplication.translate("Save", "every ", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_4.setText(QtGui.QApplication.translate("Save", "Save when focus is lost", None, QtGui.QApplication.UnicodeUTF8))

import res_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Save = QtGui.QWidget()
    ui = Ui_Save()
    ui.setupUi(Save)
    Save.show()
    sys.exit(app.exec_())

