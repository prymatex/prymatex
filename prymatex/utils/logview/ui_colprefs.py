# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'colprefs.ui'
#
# Created: Sun Feb  6 14:39:53 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from qt import QtCore, QtGui

class Ui_ColPrefsDialog(object):
    def setupUi(self, ColPrefsDialog):
        ColPrefsDialog.setObjectName("ColPrefsDialog")
        ColPrefsDialog.resize(225, 402)
        ColPrefsDialog.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(ColPrefsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(ColPrefsDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.list = QtGui.QListWidget(ColPrefsDialog)
        self.list.setObjectName("list")
        self.verticalLayout.addWidget(self.list)
        self.label_2 = QtGui.QLabel(ColPrefsDialog)
        self.label_2.setTextFormat(QtCore.Qt.PlainText)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.buttonBox = QtGui.QDialogButtonBox(ColPrefsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.label.setBuddy(self.list)

        self.retranslateUi(ColPrefsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), ColPrefsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), ColPrefsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ColPrefsDialog)

    def retranslateUi(self, ColPrefsDialog):
        ColPrefsDialog.setWindowTitle(QtGui.QApplication.translate("ColPrefsDialog", "Column Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ColPrefsDialog", "C&olumns:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ColPrefsDialog", "Tick the columns you want to see. Drag and drop in the list to reorder.", None, QtGui.QApplication.UnicodeUTF8))

