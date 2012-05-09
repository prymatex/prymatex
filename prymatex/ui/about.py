# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources\ui\about.ui'
#
# Created: Wed May 09 07:31:33 2012
#      by: PyQt4 UI code generator 4.8.2
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
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
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/prymatex/logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
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
