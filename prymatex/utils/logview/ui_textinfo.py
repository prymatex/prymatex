# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'textinfo.ui'
#
# Created: Sun Feb  6 14:39:53 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from qt import QtCore, QtGui

class Ui_TextInfoDialog(object):
    def setupUi(self, TextInfoDialog):
        TextInfoDialog.setObjectName("TextInfoDialog")
        TextInfoDialog.resize(400, 300)
        TextInfoDialog.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(TextInfoDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.text = QtGui.QPlainTextEdit(TextInfoDialog)
        self.text.setReadOnly(True)
        self.text.setPlainText("None")
        self.text.setObjectName("text")
        self.verticalLayout.addWidget(self.text)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.selectAll = QtGui.QPushButton(TextInfoDialog)
        self.selectAll.setObjectName("selectAll")
        self.horizontalLayout.addWidget(self.selectAll)
        self.copy = QtGui.QPushButton(TextInfoDialog)
        self.copy.setObjectName("copy")
        self.horizontalLayout.addWidget(self.copy)
        self.buttonBox = QtGui.QDialogButtonBox(TextInfoDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(TextInfoDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), TextInfoDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), TextInfoDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TextInfoDialog)

    def retranslateUi(self, TextInfoDialog):
        TextInfoDialog.setWindowTitle(QtGui.QApplication.translate("TextInfoDialog", "Additional Information", None, QtGui.QApplication.UnicodeUTF8))
        self.selectAll.setText(QtGui.QApplication.translate("TextInfoDialog", "Select &All", None, QtGui.QApplication.UnicodeUTF8))
        self.copy.setText(QtGui.QApplication.translate("TextInfoDialog", "&Copy", None, QtGui.QApplication.UnicodeUTF8))

