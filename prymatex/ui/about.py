# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/about.ui'
#
# Created: Thu Mar 22 13:24:50 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName(_fromUtf8("AboutDialog"))
        AboutDialog.resize(400, 465)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/prymatex/Prymatex_Logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AboutDialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(AboutDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.labelLogo = QtGui.QLabel(AboutDialog)
        self.labelLogo.setText(_fromUtf8(""))
        self.labelLogo.setPixmap(QtGui.QPixmap(_fromUtf8(":/icons/prymatex/Prymatex_Logo.png")))
        self.labelLogo.setAlignment(QtCore.Qt.AlignCenter)
        self.labelLogo.setObjectName(_fromUtf8("labelLogo"))
        self.verticalLayout.addWidget(self.labelLogo)
        self.labelTitle = QtGui.QLabel(AboutDialog)
        self.labelTitle.setObjectName(_fromUtf8("labelTitle"))
        self.verticalLayout.addWidget(self.labelTitle)
        self.textInformation = QtGui.QTextEdit(AboutDialog)
        self.textInformation.setObjectName(_fromUtf8("textInformation"))
        self.verticalLayout.addWidget(self.textInformation)
        self.buttonBox = QtGui.QDialogButtonBox(AboutDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AboutDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AboutDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AboutDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        AboutDialog.setWindowTitle(QtGui.QApplication.translate("AboutDialog", "About Prymatex", None, QtGui.QApplication.UnicodeUTF8))
        self.labelTitle.setText(QtGui.QApplication.translate("AboutDialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:600;\">Prymatex</span></p><hr/><p align=\"center\">Oprn Source Text Editor<br/><br/>© Prymatex Team 2009-2012<br/>van Haaster Diego<br/>Defossé Nahuel</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

import prymatex.resources_rc
