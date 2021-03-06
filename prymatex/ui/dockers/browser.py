# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/dockers/browser.ui'
#
# Created: Wed May 27 08:01:35 2015
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_BrowserDock(object):
    def setupUi(self, BrowserDock):
        BrowserDock.setObjectName("BrowserDock")
        BrowserDock.resize(773, 61)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButtonGoPrevious = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushButtonGoPrevious.setText("")
        icon = QtGui.QIcon.fromTheme("browser-back")
        self.pushButtonGoPrevious.setIcon(icon)
        self.pushButtonGoPrevious.setObjectName("pushButtonGoPrevious")
        self.horizontalLayout.addWidget(self.pushButtonGoPrevious)
        self.pushButtonGoNext = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushButtonGoNext.setEnabled(True)
        self.pushButtonGoNext.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.pushButtonGoNext.setText("")
        icon = QtGui.QIcon.fromTheme("browser-forward")
        self.pushButtonGoNext.setIcon(icon)
        self.pushButtonGoNext.setObjectName("pushButtonGoNext")
        self.horizontalLayout.addWidget(self.pushButtonGoNext)
        self.pushButtonReload = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushButtonReload.setText("")
        icon = QtGui.QIcon.fromTheme("browser-reload")
        self.pushButtonReload.setIcon(icon)
        self.pushButtonReload.setObjectName("pushButtonReload")
        self.horizontalLayout.addWidget(self.pushButtonReload)
        self.comboBoxUrl = QtWidgets.QComboBox(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxUrl.sizePolicy().hasHeightForWidth())
        self.comboBoxUrl.setSizePolicy(sizePolicy)
        self.comboBoxUrl.setEditable(True)
        self.comboBoxUrl.setObjectName("comboBoxUrl")
        self.horizontalLayout.addWidget(self.comboBoxUrl)
        self.pushButtonStop = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushButtonStop.setText("")
        icon = QtGui.QIcon.fromTheme("browser-stop")
        self.pushButtonStop.setIcon(icon)
        self.pushButtonStop.setObjectName("pushButtonStop")
        self.horizontalLayout.addWidget(self.pushButtonStop)
        self.line = QtWidgets.QFrame(self.dockWidgetContents)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.toolButtonOptions = QtWidgets.QToolButton(self.dockWidgetContents)
        icon = QtGui.QIcon.fromTheme("options")
        self.toolButtonOptions.setIcon(icon)
        self.toolButtonOptions.setObjectName("toolButtonOptions")
        self.horizontalLayout.addWidget(self.toolButtonOptions)
        self.verticalLayout.addLayout(self.horizontalLayout)
        BrowserDock.setWidget(self.dockWidgetContents)

        self.retranslateUi(BrowserDock)
        QtCore.QMetaObject.connectSlotsByName(BrowserDock)

    def retranslateUi(self, BrowserDock):
        _translate = QtCore.QCoreApplication.translate
        BrowserDock.setWindowTitle(_translate("BrowserDock", "Browser"))
        self.pushButtonGoPrevious.setToolTip(_translate("BrowserDock", "Back"))
        self.pushButtonGoNext.setToolTip(_translate("BrowserDock", "Next"))
        self.pushButtonReload.setToolTip(_translate("BrowserDock", "Reload"))
        self.pushButtonStop.setToolTip(_translate("BrowserDock", "Stop"))

