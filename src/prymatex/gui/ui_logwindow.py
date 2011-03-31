# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/logwindow.ui'
#
# Created: Thu Mar 31 09:44:47 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_LogWidget(object):
    def setupUi(self, LogWidget):
        LogWidget.setObjectName("LogWidget")
        LogWidget.resize(400, 103)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/actions/resources/actions/document-preview.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        LogWidget.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(LogWidget)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Clear = QtGui.QPushButton(LogWidget)
        self.Clear.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/actions/resources/actions/edit-delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Clear.setIcon(icon1)
        self.Clear.setObjectName("Clear")
        self.horizontalLayout.addWidget(self.Clear)
        self.pushButton_2 = QtGui.QPushButton(LogWidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/actions/resources/actions/view-filter.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon2)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.textEdit = QtGui.QTextEdit(LogWidget)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)

        self.retranslateUi(LogWidget)
        QtCore.QMetaObject.connectSlotsByName(LogWidget)

    def retranslateUi(self, LogWidget):
        LogWidget.setWindowTitle(QtGui.QApplication.translate("LogWidget", "Log", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("LogWidget", "Filter", None, QtGui.QApplication.UnicodeUTF8))

import res_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    LogWidget = QtGui.QWidget()
    ui = Ui_LogWidget()
    ui.setupUi(LogWidget)
    LogWidget.show()
    sys.exit(app.exec_())

