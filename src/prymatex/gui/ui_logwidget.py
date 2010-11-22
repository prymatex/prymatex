# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/logwidget.ui'
#
# Created: Mon Nov 22 17:01:34 2010
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_LogWidget(object):
    def setupUi(self, LogWidget):
        LogWidget.setObjectName("LogWidget")
        LogWidget.resize(666, 131)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/actions/resources/actions/document-preview.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        LogWidget.setWindowIcon(icon)
        LogWidget.setFloating(True)
        LogWidget.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea|QtCore.Qt.RightDockWidgetArea|QtCore.Qt.TopDockWidgetArea)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Clear = QtGui.QPushButton(self.dockWidgetContents)
        self.Clear.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/actions/resources/actions/edit-delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Clear.setIcon(icon1)
        self.Clear.setObjectName("Clear")
        self.horizontalLayout.addWidget(self.Clear)
        self.pushDebugLevel = QtGui.QPushButton(self.dockWidgetContents)
        self.pushDebugLevel.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/actions/resources/actions/view-filter.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushDebugLevel.setIcon(icon2)
        self.pushDebugLevel.setObjectName("pushDebugLevel")
        self.horizontalLayout.addWidget(self.pushDebugLevel)
        self.lineEdit = QtGui.QLineEdit(self.dockWidgetContents)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.textLog = QtGui.QTextEdit(self.dockWidgetContents)
        self.textLog.setEnabled(False)
        self.textLog.setReadOnly(True)
        self.textLog.setObjectName("textLog")
        self.verticalLayout.addWidget(self.textLog)
        LogWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(LogWidget)
        QtCore.QObject.connect(self.Clear, QtCore.SIGNAL("clicked()"), self.textLog.clear)
        QtCore.QMetaObject.connectSlotsByName(LogWidget)

    def retranslateUi(self, LogWidget):
        LogWidget.setWindowTitle(QtGui.QApplication.translate("LogWidget", "Log", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit.setToolTip(QtGui.QApplication.translate("LogWidget", "Filter debugging output", None, QtGui.QApplication.UnicodeUTF8))

import res_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    LogWidget = QtGui.QDockWidget()
    ui = Ui_LogWidget()
    ui.setupUi(LogWidget)
    LogWidget.show()
    sys.exit(app.exec_())

