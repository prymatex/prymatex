# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/dockers/browser.ui'
#
# Created: Sun May 20 12:36:36 2012
#      by: PyQt4 UI code generator 4.8.4
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
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/go-previous.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonBack.setIcon(icon)
        self.buttonBack.setFlat(True)
        self.buttonBack.setObjectName(_fromUtf8("buttonBack"))
        self.horizontalLayout.addWidget(self.buttonBack)
        self.buttonNext = QtGui.QPushButton(self.dockWidgetContents)
        self.buttonNext.setEnabled(True)
        self.buttonNext.setMaximumSize(QtCore.QSize(24, 24))
        self.buttonNext.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.buttonNext.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/go-next.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonNext.setIcon(icon1)
        self.buttonNext.setFlat(True)
        self.buttonNext.setObjectName(_fromUtf8("buttonNext"))
        self.horizontalLayout.addWidget(self.buttonNext)
        self.buttonReload = QtGui.QPushButton(self.dockWidgetContents)
        self.buttonReload.setMaximumSize(QtCore.QSize(24, 24))
        self.buttonReload.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/view-refresh.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonReload.setIcon(icon2)
        self.buttonReload.setFlat(True)
        self.buttonReload.setObjectName(_fromUtf8("buttonReload"))
        self.horizontalLayout.addWidget(self.buttonReload)
        self.lineUrl = QtGui.QLineEdit(self.dockWidgetContents)
        self.lineUrl.setObjectName(_fromUtf8("lineUrl"))
        self.horizontalLayout.addWidget(self.lineUrl)
        self.buttonStop = QtGui.QPushButton(self.dockWidgetContents)
        self.buttonStop.setMaximumSize(QtCore.QSize(24, 24))
        self.buttonStop.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/dialog-close.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonStop.setIcon(icon3)
        self.buttonStop.setFlat(True)
        self.buttonStop.setObjectName(_fromUtf8("buttonStop"))
        self.horizontalLayout.addWidget(self.buttonStop)
        self.line = QtGui.QFrame(self.dockWidgetContents)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.horizontalLayout.addWidget(self.line)
        self.pushButtonSync = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButtonSync.setMaximumSize(QtCore.QSize(24, 24))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/system-switch-user.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonSync.setIcon(icon4)
        self.pushButtonSync.setCheckable(True)
        self.pushButtonSync.setFlat(True)
        self.pushButtonSync.setObjectName(_fromUtf8("pushButtonSync"))
        self.horizontalLayout.addWidget(self.pushButtonSync)
        self.pushButtonOptions = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButtonOptions.setMaximumSize(QtCore.QSize(24, 24))
        self.pushButtonOptions.setText(_fromUtf8(""))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/configure.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonOptions.setIcon(icon5)
        self.pushButtonOptions.setFlat(True)
        self.pushButtonOptions.setObjectName(_fromUtf8("pushButtonOptions"))
        self.horizontalLayout.addWidget(self.pushButtonOptions)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.webView = QtWebKit.QWebView(self.dockWidgetContents)
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.verticalLayout.addWidget(self.webView)
        BrowserDock.setWidget(self.dockWidgetContents)

        self.retranslateUi(BrowserDock)
        QtCore.QMetaObject.connectSlotsByName(BrowserDock)

    def retranslateUi(self, BrowserDock):
        BrowserDock.setWindowTitle(_('Web Browser'))
        self.buttonBack.setToolTip(_('Back'))
        self.buttonNext.setToolTip(_('Next'))
        self.buttonReload.setToolTip(_('Reload'))
        self.buttonStop.setToolTip(_('Stop'))
        self.pushButtonSync.setToolTip(_('Sync folder with current editor file path'))

from PyQt4 import QtWebKit
from prymatex import resources_rc
