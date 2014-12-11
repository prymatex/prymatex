# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/sda5/Projects/Prymatex/prymatex/resources/ui/emergencycrash.ui'
#
# Created: Wed Dec 10 16:51:28 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CrashDialog(object):
    def setupUi(self, CrashDialog):
        CrashDialog.setObjectName("CrashDialog")
        CrashDialog.resize(579, 411)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/prymatex/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        CrashDialog.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(CrashDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(CrashDialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(CrashDialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(CrashDialog)
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap(":/icons/resources/icons/Prymatex_Logo.png"))
        self.label_3.setScaledContents(False)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.textEdit = QtWidgets.QTextEdit(CrashDialog)
        self.textEdit.setEnabled(True)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout.addWidget(self.textEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushSendTraceback = QtWidgets.QPushButton(CrashDialog)
        self.pushSendTraceback.setEnabled(False)
        self.pushSendTraceback.setObjectName("pushSendTraceback")
        self.horizontalLayout_2.addWidget(self.pushSendTraceback)
        self.pushCopyTraceback = QtWidgets.QPushButton(CrashDialog)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/actions/edit-copy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushCopyTraceback.setIcon(icon1)
        self.pushCopyTraceback.setObjectName("pushCopyTraceback")
        self.horizontalLayout_2.addWidget(self.pushCopyTraceback)
        self.pushClose = QtWidgets.QPushButton(CrashDialog)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/actions/application-exit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushClose.setIcon(icon2)
        self.pushClose.setObjectName("pushClose")
        self.horizontalLayout_2.addWidget(self.pushClose)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(CrashDialog)
        self.pushClose.clicked.connect(CrashDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CrashDialog)

    def retranslateUi(self, CrashDialog):
        _translate = QtCore.QCoreApplication.translate
        CrashDialog.setWindowTitle(_translate("CrashDialog", "Prymatex Crash"))
        self.label.setText(_translate("CrashDialog", "Prymatex Has Crashed"))
        self.label_2.setText(_translate("CrashDialog", "Prymatex has crashed, an uncattched exception has been risen somewhere.\n"
"If you\'re a developer you could dig into the code and send a path if appopiate.\n"
"Full detail about the exception has been pasted below."))
        self.label_3.setToolTip(_translate("CrashDialog", "No monkeys have been hurt in the process"))
        self.pushSendTraceback.setText(_translate("CrashDialog", "Send"))
        self.pushCopyTraceback.setText(_translate("CrashDialog", "Copy"))
        self.pushClose.setText(_translate("CrashDialog", "Close"))

