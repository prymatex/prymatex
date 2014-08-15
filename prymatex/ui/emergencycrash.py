# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/emergencycrash.ui'
#
# Created: Fri Aug 15 10:26:58 2014
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

class Ui_CrashDialog(object):
    def setupUi(self, CrashDialog):
        CrashDialog.setObjectName(_fromUtf8("CrashDialog"))
        CrashDialog.resize(579, 411)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/prymatex/logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        CrashDialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(CrashDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(CrashDialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtGui.QLabel(CrashDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_3 = QtGui.QLabel(CrashDialog)
        self.label_3.setText(_fromUtf8(""))
        self.label_3.setPixmap(QtGui.QPixmap(_fromUtf8(":/icons/resources/icons/Prymatex_Logo.png")))
        self.label_3.setScaledContents(False)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.textEdit = QtGui.QTextEdit(CrashDialog)
        self.textEdit.setEnabled(True)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.horizontalLayout.addWidget(self.textEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushSendTraceback = QtGui.QPushButton(CrashDialog)
        self.pushSendTraceback.setEnabled(False)
        self.pushSendTraceback.setObjectName(_fromUtf8("pushSendTraceback"))
        self.horizontalLayout_2.addWidget(self.pushSendTraceback)
        self.pushCopyTraceback = QtGui.QPushButton(CrashDialog)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/edit-copy.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushCopyTraceback.setIcon(icon1)
        self.pushCopyTraceback.setObjectName(_fromUtf8("pushCopyTraceback"))
        self.horizontalLayout_2.addWidget(self.pushCopyTraceback)
        self.pushClose = QtGui.QPushButton(CrashDialog)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/application-exit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushClose.setIcon(icon2)
        self.pushClose.setObjectName(_fromUtf8("pushClose"))
        self.horizontalLayout_2.addWidget(self.pushClose)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(CrashDialog)
        QtCore.QObject.connect(self.pushClose, QtCore.SIGNAL(_fromUtf8("clicked()")), CrashDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CrashDialog)

    def retranslateUi(self, CrashDialog):
        CrashDialog.setWindowTitle(_translate("CrashDialog", "Prymatex Crash", None))
        self.label.setText(_translate("CrashDialog", "Prymatex Has Crashed", None))
        self.label_2.setText(_translate("CrashDialog", "Prymatex has crashed, an uncattched exception has been risen somewhere.\n"
"If you\'re a developer you could dig into the code and send a path if appopiate.\n"
"Full detail about the exception has been pasted below.", None))
        self.label_3.setToolTip(_translate("CrashDialog", "No monkeys have been hurt in the process", None))
        self.pushSendTraceback.setText(_translate("CrashDialog", "Send", None))
        self.pushCopyTraceback.setText(_translate("CrashDialog", "Copy", None))
        self.pushClose.setText(_translate("CrashDialog", "Close", None))

