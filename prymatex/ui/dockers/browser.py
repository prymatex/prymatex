# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/dockers/browser.ui'
#
# Created: Tue Aug 21 00:14:54 2012
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_BrowserDock(object):
    def setupUi(self, BrowserDock):
        BrowserDock.setObjectName(_fromUtf8("BrowserDock"))
        BrowserDock.resize(520, 301)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.buttonBack = QtGui.QPushButton(self.dockWidgetContents)
        self.buttonBack.setMaximumSize(QtCore.QSize(24, 24))
        self.buttonBack.setText(_fromUtf8(""))
        icon = QtGui.QIcon.fromTheme(_fromUtf8("go-previous"))
        self.buttonBack.setIcon(icon)
        self.buttonBack.setFlat(True)
        self.buttonBack.setObjectName(_fromUtf8("buttonBack"))
        self.horizontalLayout.addWidget(self.buttonBack)
        self.buttonNext = QtGui.QPushButton(self.dockWidgetContents)
        self.buttonNext.setEnabled(True)
        self.buttonNext.setMaximumSize(QtCore.QSize(24, 24))
        self.buttonNext.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.buttonNext.setText(_fromUtf8(""))
        icon = QtGui.QIcon.fromTheme(_fromUtf8("go-next"))
        self.buttonNext.setIcon(icon)
        self.buttonNext.setFlat(True)
        self.buttonNext.setObjectName(_fromUtf8("buttonNext"))
        self.horizontalLayout.addWidget(self.buttonNext)
        self.buttonReload = QtGui.QPushButton(self.dockWidgetContents)
        self.buttonReload.setMaximumSize(QtCore.QSize(24, 24))
        self.buttonReload.setText(_fromUtf8(""))
        icon = QtGui.QIcon.fromTheme(_fromUtf8("view-refresh"))
        self.buttonReload.setIcon(icon)
        self.buttonReload.setFlat(True)
        self.buttonReload.setObjectName(_fromUtf8("buttonReload"))
        self.horizontalLayout.addWidget(self.buttonReload)
        self.lineUrl = QtGui.QLineEdit(self.dockWidgetContents)
        self.lineUrl.setObjectName(_fromUtf8("lineUrl"))
        self.horizontalLayout.addWidget(self.lineUrl)
        self.buttonStop = QtGui.QPushButton(self.dockWidgetContents)
        self.buttonStop.setMaximumSize(QtCore.QSize(24, 24))
        self.buttonStop.setText(_fromUtf8(""))
        icon = QtGui.QIcon.fromTheme(_fromUtf8("dialog-close"))
        self.buttonStop.setIcon(icon)
        self.buttonStop.setFlat(True)
        self.buttonStop.setObjectName(_fromUtf8("buttonStop"))
        self.horizontalLayout.addWidget(self.buttonStop)
        self.line = QtGui.QFrame(self.dockWidgetContents)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.horizontalLayout.addWidget(self.line)
        self.pushButtonOptions = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButtonOptions.setMaximumSize(QtCore.QSize(45, 24))
        self.pushButtonOptions.setText(_fromUtf8(""))
        icon = QtGui.QIcon.fromTheme(_fromUtf8("configure"))
        self.pushButtonOptions.setIcon(icon)
        self.pushButtonOptions.setFlat(True)
        self.pushButtonOptions.setObjectName(_fromUtf8("pushButtonOptions"))
        self.horizontalLayout.addWidget(self.pushButtonOptions)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.webView = QtWebKit.QWebView(self.dockWidgetContents)
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.verticalLayout.addWidget(self.webView)
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
        BrowserDock.setWindowTitle(_('Web Browser'))
        self.buttonBack.setToolTip(_('Back'))
        self.buttonNext.setToolTip(_('Next'))
        self.buttonReload.setToolTip(_('Reload'))
        self.buttonStop.setToolTip(_('Stop'))
        self.actionSyncEditor.setText(_('Sync Editor'))
        self.actionSyncEditor.setToolTip(_('Sync browser with current editor content'))
        self.actionConnectEditor.setText(_('Connect Editor'))
        self.actionConnectEditor.setToolTip(_('Connect browser with current editor'))

from PyQt4 import QtWebKit
from prymatex import resources_rc
