# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/emergencytrace.ui'
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

class Ui_TracebackDialog(object):
    def setupUi(self, TracebackDialog):
        TracebackDialog.setObjectName(_fromUtf8("TracebackDialog"))
        TracebackDialog.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(TracebackDialog)
        self.verticalLayout.setContentsMargins(1, 2, 1, 1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.labelTitle = QtGui.QLabel(TracebackDialog)
        self.labelTitle.setObjectName(_fromUtf8("labelTitle"))
        self.verticalLayout.addWidget(self.labelTitle)
        self.textStackTrace = QtGui.QTextEdit(TracebackDialog)
        self.textStackTrace.setObjectName(_fromUtf8("textStackTrace"))
        self.verticalLayout.addWidget(self.textStackTrace)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonKillApp = QtGui.QPushButton(TracebackDialog)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("application-exit"))
        self.pushButtonKillApp.setIcon(icon)
        self.pushButtonKillApp.setObjectName(_fromUtf8("pushButtonKillApp"))
        self.horizontalLayout.addWidget(self.pushButtonKillApp)
        self.pushCopy = QtGui.QPushButton(TracebackDialog)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/edit-copy.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushCopy.setIcon(icon)
        self.pushCopy.setObjectName(_fromUtf8("pushCopy"))
        self.horizontalLayout.addWidget(self.pushCopy)
        self.pushClose = QtGui.QPushButton(TracebackDialog)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("dialog-close"))
        self.pushClose.setIcon(icon)
        self.pushClose.setObjectName(_fromUtf8("pushClose"))
        self.horizontalLayout.addWidget(self.pushClose)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(TracebackDialog)
        QtCore.QObject.connect(self.pushClose, QtCore.SIGNAL(_fromUtf8("clicked()")), TracebackDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TracebackDialog)

    def retranslateUi(self, TracebackDialog):
        TracebackDialog.setWindowTitle(_translate("TracebackDialog", "Traceback", None))
        self.labelTitle.setText(_translate("TracebackDialog", "Exception Text", None))
        self.pushButtonKillApp.setText(_translate("TracebackDialog", "Terminate", None))
        self.pushCopy.setText(_translate("TracebackDialog", "&Copy", None))
        self.pushClose.setText(_translate("TracebackDialog", "&Close", None))

