# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/dialogs/profile.ui'
#
# Created: Sun May  6 02:21:05 2012
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ProfileDialog(object):
    def setupUi(self, ProfileDialog):
        ProfileDialog.setObjectName(_fromUtf8("ProfileDialog"))
        ProfileDialog.resize(400, 250)
        ProfileDialog.setMinimumSize(QtCore.QSize(400, 0))
        self.verticalLayout = QtGui.QVBoxLayout(ProfileDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(ProfileDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.buttonCreate = QtGui.QPushButton(ProfileDialog)
        self.buttonCreate.setObjectName(_fromUtf8("buttonCreate"))
        self.verticalLayout_2.addWidget(self.buttonCreate)
        self.buttonRename = QtGui.QPushButton(ProfileDialog)
        self.buttonRename.setObjectName(_fromUtf8("buttonRename"))
        self.verticalLayout_2.addWidget(self.buttonRename)
        self.buttonDelete = QtGui.QPushButton(ProfileDialog)
        self.buttonDelete.setObjectName(_fromUtf8("buttonDelete"))
        self.verticalLayout_2.addWidget(self.buttonDelete)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.listProfiles = QtGui.QListWidget(ProfileDialog)
        self.listProfiles.setObjectName(_fromUtf8("listProfiles"))
        self.verticalLayout_3.addWidget(self.listProfiles)
        self.checkDontAsk = QtGui.QCheckBox(ProfileDialog)
        self.checkDontAsk.setObjectName(_fromUtf8("checkDontAsk"))
        self.verticalLayout_3.addWidget(self.checkDontAsk)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.buttonExit = QtGui.QPushButton(ProfileDialog)
        self.buttonExit.setObjectName(_fromUtf8("buttonExit"))
        self.horizontalLayout_2.addWidget(self.buttonExit)
        self.buttonStartPrymatex = QtGui.QPushButton(ProfileDialog)
        self.buttonStartPrymatex.setObjectName(_fromUtf8("buttonStartPrymatex"))
        self.horizontalLayout_2.addWidget(self.buttonStartPrymatex)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(ProfileDialog)
        QtCore.QMetaObject.connectSlotsByName(ProfileDialog)

    def retranslateUi(self, ProfileDialog):
        ProfileDialog.setWindowTitle(_('Prymatex Choose User Profile'))
        self.label.setText(_('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n<html><head><meta name="qrichtext" content="1" /><style type="text/css">\np, li { white-space: pre-wrap; }\n</style></head><body style=" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;">\n<p style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">Prymatex stores information about your settings, preferences and other items in your user profile.</p></body></html>'))
        self.buttonCreate.setText(_('&Create Profile'))
        self.buttonRename.setText(_('&Rename Profile'))
        self.buttonDelete.setText(_('&Delete Profile'))
        self.checkDontAsk.setText(_('Don\'t a&sk at startup'))
        self.buttonExit.setText(_('Exit'))
        self.buttonStartPrymatex.setText(_('Start Prymatex'))

