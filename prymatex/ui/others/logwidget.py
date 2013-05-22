# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/datos/workspace/Prymatex/prymatex/resources/ui/others/logwidget.ui'
#
# Created: Wed May 22 20:00:14 2013
#      by: PyQt4 UI code generator snapshot-4.10.2-6f54723ef2ba
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

class Ui_LogWidget(object):
    def setupUi(self, LogWidget):
        LogWidget.setObjectName(_fromUtf8("LogWidget"))
        LogWidget.resize(666, 133)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/resources/actions/document-preview.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        LogWidget.setWindowIcon(icon)
        LogWidget.setFloating(True)
        LogWidget.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea|QtCore.Qt.RightDockWidgetArea|QtCore.Qt.TopDockWidgetArea)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.Clear = QtGui.QPushButton(self.dockWidgetContents)
        self.Clear.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/view-refresh.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Clear.setIcon(icon1)
        self.Clear.setObjectName(_fromUtf8("Clear"))
        self.horizontalLayout.addWidget(self.Clear)
        self.pushDebugLevel = QtGui.QPushButton(self.dockWidgetContents)
        self.pushDebugLevel.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/view-filter.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushDebugLevel.setIcon(icon2)
        self.pushDebugLevel.setObjectName(_fromUtf8("pushDebugLevel"))
        self.horizontalLayout.addWidget(self.pushDebugLevel)
        self.lineEdit = QtGui.QLineEdit(self.dockWidgetContents)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout.addWidget(self.lineEdit)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.textLog = QtGui.QTextEdit(self.dockWidgetContents)
        self.textLog.setEnabled(False)
        self.textLog.setReadOnly(True)
        self.textLog.setObjectName(_fromUtf8("textLog"))
        self.verticalLayout.addWidget(self.textLog)
        LogWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(LogWidget)
        QtCore.QObject.connect(self.Clear, QtCore.SIGNAL(_fromUtf8("clicked()")), self.textLog.clear)
        QtCore.QMetaObject.connectSlotsByName(LogWidget)

    def retranslateUi(self, LogWidget):
        LogWidget.setWindowTitle(_translate("LogWidget", "Log", None))
        self.lineEdit.setToolTip(_translate("LogWidget", "Filter debugging output", None))

import resources_rc
