# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'prymatex\resources\ui\logwidget.ui'
#
# Created: Fri Jul 01 12:35:45 2011
#      by: PyQt4 UI code generator 4.8.2
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.translation import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

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
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/resources/actions/edit-delete.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Clear.setIcon(icon1)
        self.Clear.setObjectName(_fromUtf8("Clear"))
        self.horizontalLayout.addWidget(self.Clear)
        self.pushDebugLevel = QtGui.QPushButton(self.dockWidgetContents)
        self.pushDebugLevel.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/actions/resources/actions/view-filter.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
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
        LogWidget.setWindowTitle(_('Log'))
        self.lineEdit.setToolTip(_('Filter debugging output'))

from prymatex import res_rc
