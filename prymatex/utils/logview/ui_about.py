# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about.ui'
#
# Created: Sun Feb  6 14:39:53 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from qt import QtCore, QtGui

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName("AboutDialog")
        AboutDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        AboutDialog.resize(418, 288)
        self.buttonBox = QtGui.QDialogButtonBox(AboutDialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 250, 381, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.frame = QtGui.QFrame(AboutDialog)
        self.frame.setGeometry(QtCore.QRect(10, 10, 401, 231))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.layoutWidget = QtGui.QWidget(self.frame)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 100, 381, 121))
        self.layoutWidget.setObjectName("layoutWidget")
        self.vLay = QtGui.QVBoxLayout(self.layoutWidget)
        self.vLay.setObjectName("vLay")
        self.name = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.name.setFont(font)
        self.name.setObjectName("name")
        self.vLay.addWidget(self.name)
        self.version = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.version.setFont(font)
        self.version.setObjectName("version")
        self.vLay.addWidget(self.version)
        self.qtversion = QtGui.QLabel(self.layoutWidget)
        self.qtversion.setObjectName("qtversion")
        self.vLay.addWidget(self.qtversion)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vLay.addItem(spacerItem)
        self.copyright = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.copyright.setFont(font)
        self.copyright.setObjectName("copyright")
        self.vLay.addWidget(self.copyright)
        self.logo = QtGui.QLabel(self.frame)
        self.logo.setGeometry(QtCore.QRect(10, 10, 61, 81))
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap(":/rdclogo.png"))
        self.logo.setObjectName("logo")

        self.retranslateUi(AboutDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), AboutDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), AboutDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        AboutDialog.setWindowTitle(QtGui.QApplication.translate("AboutDialog", "About Python Log Viewer", None, QtGui.QApplication.UnicodeUTF8))
        self.name.setText(QtGui.QApplication.translate("AboutDialog", "Python Log Viewer", None, QtGui.QApplication.UnicodeUTF8))
        self.version.setText(QtGui.QApplication.translate("AboutDialog", "version 0.1", None, QtGui.QApplication.UnicodeUTF8))
        self.qtversion.setText(QtGui.QApplication.translate("AboutDialog", "PyQt version on Qt version", None, QtGui.QApplication.UnicodeUTF8))
        self.copyright.setText(QtGui.QApplication.translate("AboutDialog", "Copyright © 2011 Vinay M. Sajip.", None, QtGui.QApplication.UnicodeUTF8))

import logview_rc
