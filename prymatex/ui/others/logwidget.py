# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/sda5/Projects/Prymatex/prymatex/resources/ui/others/logwidget.ui'
#
# Created: Tue Dec  9 16:01:55 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LogWidget(object):
    def setupUi(self, LogWidget):
        LogWidget.setObjectName("LogWidget")
        LogWidget.resize(666, 133)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/actions/resources/actions/document-preview.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        LogWidget.setWindowIcon(icon)
        LogWidget.setFloating(True)
        LogWidget.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea|QtCore.Qt.RightDockWidgetArea|QtCore.Qt.TopDockWidgetArea)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Clear = QtWidgets.QPushButton(self.dockWidgetContents)
        self.Clear.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/actions/view-refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Clear.setIcon(icon1)
        self.Clear.setObjectName("Clear")
        self.horizontalLayout.addWidget(self.Clear)
        self.pushDebugLevel = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushDebugLevel.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/actions/view-filter.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushDebugLevel.setIcon(icon2)
        self.pushDebugLevel.setObjectName("pushDebugLevel")
        self.horizontalLayout.addWidget(self.pushDebugLevel)
        self.lineEdit = QtWidgets.QLineEdit(self.dockWidgetContents)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.textLog = QtWidgets.QTextEdit(self.dockWidgetContents)
        self.textLog.setEnabled(False)
        self.textLog.setReadOnly(True)
        self.textLog.setObjectName("textLog")
        self.verticalLayout.addWidget(self.textLog)
        LogWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(LogWidget)
        self.Clear.clicked.connect(self.textLog.clear)
        QtCore.QMetaObject.connectSlotsByName(LogWidget)

    def retranslateUi(self, LogWidget):
        _translate = QtCore.QCoreApplication.translate
        LogWidget.setWindowTitle(_translate("LogWidget", "Log"))
        self.lineEdit.setToolTip(_translate("LogWidget", "Filter debugging output"))

import resources_rc
