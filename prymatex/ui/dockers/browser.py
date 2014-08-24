# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/sda5/Projects/Prymatex/prymatex/resources/ui/dockers/browser.ui'
#
# Created: Sun Aug 24 09:22:43 2014
#      by: PyQt4 UI code generator 4.11.1
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

class Ui_BrowserDock(object):
    def setupUi(self, BrowserDock):
        BrowserDock.setObjectName(_fromUtf8("BrowserDock"))
        BrowserDock.resize(520, 54)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButtonGoPrevious = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButtonGoPrevious.setMaximumSize(QtCore.QSize(24, 24))
        self.pushButtonGoPrevious.setText(_fromUtf8(""))
        icon = QtGui.QIcon.fromTheme(_fromUtf8("go-previous"))
        self.pushButtonGoPrevious.setIcon(icon)
        self.pushButtonGoPrevious.setFlat(True)
        self.pushButtonGoPrevious.setObjectName(_fromUtf8("pushButtonGoPrevious"))
        self.horizontalLayout.addWidget(self.pushButtonGoPrevious)
        self.pushButtonGoNext = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButtonGoNext.setEnabled(True)
        self.pushButtonGoNext.setMaximumSize(QtCore.QSize(24, 24))
        self.pushButtonGoNext.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.pushButtonGoNext.setText(_fromUtf8(""))
        icon = QtGui.QIcon.fromTheme(_fromUtf8("go-next"))
        self.pushButtonGoNext.setIcon(icon)
        self.pushButtonGoNext.setFlat(True)
        self.pushButtonGoNext.setObjectName(_fromUtf8("pushButtonGoNext"))
        self.horizontalLayout.addWidget(self.pushButtonGoNext)
        self.pushButtonReload = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButtonReload.setMaximumSize(QtCore.QSize(24, 24))
        self.pushButtonReload.setText(_fromUtf8(""))
        icon = QtGui.QIcon.fromTheme(_fromUtf8("reload"))
        self.pushButtonReload.setIcon(icon)
        self.pushButtonReload.setFlat(True)
        self.pushButtonReload.setObjectName(_fromUtf8("pushButtonReload"))
        self.horizontalLayout.addWidget(self.pushButtonReload)
        self.lineUrl = QtGui.QLineEdit(self.dockWidgetContents)
        self.lineUrl.setObjectName(_fromUtf8("lineUrl"))
        self.horizontalLayout.addWidget(self.lineUrl)
        self.pushButtonStop = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButtonStop.setMaximumSize(QtCore.QSize(24, 24))
        self.pushButtonStop.setText(_fromUtf8(""))
        icon = QtGui.QIcon.fromTheme(_fromUtf8("stop"))
        self.pushButtonStop.setIcon(icon)
        self.pushButtonStop.setFlat(True)
        self.pushButtonStop.setObjectName(_fromUtf8("pushButtonStop"))
        self.horizontalLayout.addWidget(self.pushButtonStop)
        self.line = QtGui.QFrame(self.dockWidgetContents)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.horizontalLayout.addWidget(self.line)
        self.toolButtonOptions = QtGui.QToolButton(self.dockWidgetContents)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("options"))
        self.toolButtonOptions.setIcon(icon)
        self.toolButtonOptions.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.toolButtonOptions.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.toolButtonOptions.setAutoRaise(True)
        self.toolButtonOptions.setArrowType(QtCore.Qt.NoArrow)
        self.toolButtonOptions.setObjectName(_fromUtf8("toolButtonOptions"))
        self.horizontalLayout.addWidget(self.toolButtonOptions)
        self.verticalLayout.addLayout(self.horizontalLayout)
        BrowserDock.setWidget(self.dockWidgetContents)
        self.actionSyncEditor = QtGui.QAction(BrowserDock)
        self.actionSyncEditor.setCheckable(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/system-switch-user.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSyncEditor.setIcon(icon)
        self.actionSyncEditor.setObjectName(_fromUtf8("actionSyncEditor"))
        self.actionConnectEditor = QtGui.QAction(BrowserDock)
        self.actionConnectEditor.setCheckable(True)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/network-connect.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionConnectEditor.setIcon(icon1)
        self.actionConnectEditor.setObjectName(_fromUtf8("actionConnectEditor"))

        self.retranslateUi(BrowserDock)
        QtCore.QMetaObject.connectSlotsByName(BrowserDock)

    def retranslateUi(self, BrowserDock):
        BrowserDock.setWindowTitle(_translate("BrowserDock", "Web Browser", None))
        self.pushButtonGoPrevious.setToolTip(_translate("BrowserDock", "Back", None))
        self.pushButtonGoNext.setToolTip(_translate("BrowserDock", "Next", None))
        self.pushButtonReload.setToolTip(_translate("BrowserDock", "Reload", None))
        self.pushButtonStop.setToolTip(_translate("BrowserDock", "Stop", None))
        self.actionSyncEditor.setText(_translate("BrowserDock", "Sync Editor", None))
        self.actionSyncEditor.setToolTip(_translate("BrowserDock", "Sync browser with current editor content", None))
        self.actionConnectEditor.setText(_translate("BrowserDock", "Connect Editor", None))
        self.actionConnectEditor.setToolTip(_translate("BrowserDock", "Connect browser with current editor", None))

