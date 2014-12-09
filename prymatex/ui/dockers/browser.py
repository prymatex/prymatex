# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/sda5/Projects/Prymatex/prymatex/resources/ui/dockers/browser.ui'
#
# Created: Tue Dec  9 16:01:56 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_BrowserDock(object):
    def setupUi(self, BrowserDock):
        BrowserDock.setObjectName("BrowserDock")
        BrowserDock.resize(520, 61)
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
        icon = QtGui.QIcon.fromTheme("go-previous")
        self.pushButtonGoPrevious.setIcon(icon)
        self.pushButtonGoPrevious.setObjectName("pushButtonGoPrevious")
        self.horizontalLayout.addWidget(self.pushButtonGoPrevious)
        self.pushButtonGoNext = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushButtonGoNext.setEnabled(True)
        self.pushButtonGoNext.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.pushButtonGoNext.setText("")
        icon = QtGui.QIcon.fromTheme("go-next")
        self.pushButtonGoNext.setIcon(icon)
        self.pushButtonGoNext.setObjectName("pushButtonGoNext")
        self.horizontalLayout.addWidget(self.pushButtonGoNext)
        self.pushButtonReload = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushButtonReload.setText("")
        icon = QtGui.QIcon.fromTheme("reload")
        self.pushButtonReload.setIcon(icon)
        self.pushButtonReload.setObjectName("pushButtonReload")
        self.horizontalLayout.addWidget(self.pushButtonReload)
        self.lineUrl = QtWidgets.QLineEdit(self.dockWidgetContents)
        self.lineUrl.setObjectName("lineUrl")
        self.horizontalLayout.addWidget(self.lineUrl)
        self.pushButtonStop = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushButtonStop.setText("")
        icon = QtGui.QIcon.fromTheme("stop")
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
        self.toolButtonOptions.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)
        self.toolButtonOptions.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.toolButtonOptions.setArrowType(QtCore.Qt.NoArrow)
        self.toolButtonOptions.setObjectName("toolButtonOptions")
        self.horizontalLayout.addWidget(self.toolButtonOptions)
        self.verticalLayout.addLayout(self.horizontalLayout)
        BrowserDock.setWidget(self.dockWidgetContents)
        self.actionSyncEditor = QtWidgets.QAction(BrowserDock)
        self.actionSyncEditor.setCheckable(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/actions/system-switch-user.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSyncEditor.setIcon(icon)
        self.actionSyncEditor.setObjectName("actionSyncEditor")
        self.actionConnectEditor = QtWidgets.QAction(BrowserDock)
        self.actionConnectEditor.setCheckable(True)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/actions/network-connect.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionConnectEditor.setIcon(icon1)
        self.actionConnectEditor.setObjectName("actionConnectEditor")

        self.retranslateUi(BrowserDock)
        QtCore.QMetaObject.connectSlotsByName(BrowserDock)

    def retranslateUi(self, BrowserDock):
        _translate = QtCore.QCoreApplication.translate
        BrowserDock.setWindowTitle(_translate("BrowserDock", "Web Browser"))
        self.pushButtonGoPrevious.setToolTip(_translate("BrowserDock", "Back"))
        self.pushButtonGoNext.setToolTip(_translate("BrowserDock", "Next"))
        self.pushButtonReload.setToolTip(_translate("BrowserDock", "Reload"))
        self.pushButtonStop.setToolTip(_translate("BrowserDock", "Stop"))
        self.actionSyncEditor.setText(_translate("BrowserDock", "Sync Editor"))
        self.actionSyncEditor.setToolTip(_translate("BrowserDock", "Sync browser with current editor content"))
        self.actionConnectEditor.setText(_translate("BrowserDock", "Connect Editor"))
        self.actionConnectEditor.setToolTip(_translate("BrowserDock", "Connect browser with current editor"))

