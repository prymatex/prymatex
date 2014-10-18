# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/sda5/Projects/Prymatex/prymatex/resources/ui/emergencytrace.ui'
#
# Created: Sat Oct 18 10:31:39 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TracebackDialog(object):
    def setupUi(self, TracebackDialog):
        TracebackDialog.setObjectName("TracebackDialog")
        TracebackDialog.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(TracebackDialog)
        self.verticalLayout.setContentsMargins(1, 2, 1, 1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelTitle = QtWidgets.QLabel(TracebackDialog)
        self.labelTitle.setObjectName("labelTitle")
        self.verticalLayout.addWidget(self.labelTitle)
        self.textStackTrace = QtWidgets.QTextEdit(TracebackDialog)
        self.textStackTrace.setObjectName("textStackTrace")
        self.verticalLayout.addWidget(self.textStackTrace)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonKillApp = QtWidgets.QPushButton(TracebackDialog)
        icon = QtGui.QIcon.fromTheme("application-exit")
        self.pushButtonKillApp.setIcon(icon)
        self.pushButtonKillApp.setObjectName("pushButtonKillApp")
        self.horizontalLayout.addWidget(self.pushButtonKillApp)
        self.pushCopy = QtWidgets.QPushButton(TracebackDialog)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/actions/edit-copy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushCopy.setIcon(icon)
        self.pushCopy.setObjectName("pushCopy")
        self.horizontalLayout.addWidget(self.pushCopy)
        self.pushClose = QtWidgets.QPushButton(TracebackDialog)
        icon = QtGui.QIcon.fromTheme("dialog-close")
        self.pushClose.setIcon(icon)
        self.pushClose.setObjectName("pushClose")
        self.horizontalLayout.addWidget(self.pushClose)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(TracebackDialog)
        self.pushClose.clicked.connect(TracebackDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TracebackDialog)

    def retranslateUi(self, TracebackDialog):
        _translate = QtCore.QCoreApplication.translate
        TracebackDialog.setWindowTitle(_translate("TracebackDialog", "Traceback"))
        self.labelTitle.setText(_translate("TracebackDialog", "Exception Text"))
        self.pushButtonKillApp.setText(_translate("TracebackDialog", "Terminate"))
        self.pushCopy.setText(_translate("TracebackDialog", "&Copy"))
        self.pushClose.setText(_translate("TracebackDialog", "&Close"))

