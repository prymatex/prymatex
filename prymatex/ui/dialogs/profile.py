# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/sda5/Projects/Prymatex/prymatex/resources/ui/dialogs/profile.ui'
#
# Created: Wed Oct 22 18:41:36 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ProfileDialog(object):
    def setupUi(self, ProfileDialog):
        ProfileDialog.setObjectName("ProfileDialog")
        ProfileDialog.resize(400, 250)
        ProfileDialog.setMinimumSize(QtCore.QSize(400, 0))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/prymatex/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ProfileDialog.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(ProfileDialog)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(ProfileDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.buttonCreate = QtWidgets.QPushButton(ProfileDialog)
        icon = QtGui.QIcon.fromTheme("list-add-user")
        self.buttonCreate.setIcon(icon)
        self.buttonCreate.setObjectName("buttonCreate")
        self.verticalLayout_2.addWidget(self.buttonCreate)
        self.buttonRename = QtWidgets.QPushButton(ProfileDialog)
        icon = QtGui.QIcon.fromTheme("user-properties")
        self.buttonRename.setIcon(icon)
        self.buttonRename.setObjectName("buttonRename")
        self.verticalLayout_2.addWidget(self.buttonRename)
        self.buttonDelete = QtWidgets.QPushButton(ProfileDialog)
        icon = QtGui.QIcon.fromTheme("list-remove-user")
        self.buttonDelete.setIcon(icon)
        self.buttonDelete.setObjectName("buttonDelete")
        self.verticalLayout_2.addWidget(self.buttonDelete)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.listViewProfiles = QtWidgets.QListView(ProfileDialog)
        self.listViewProfiles.setObjectName("listViewProfiles")
        self.verticalLayout_3.addWidget(self.listViewProfiles)
        self.checkDontAsk = QtWidgets.QCheckBox(ProfileDialog)
        self.checkDontAsk.setObjectName("checkDontAsk")
        self.verticalLayout_3.addWidget(self.checkDontAsk)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.buttonExit = QtWidgets.QPushButton(ProfileDialog)
        icon = QtGui.QIcon.fromTheme("application-exit")
        self.buttonExit.setIcon(icon)
        self.buttonExit.setObjectName("buttonExit")
        self.horizontalLayout_2.addWidget(self.buttonExit)
        self.buttonStartPrymatex = QtWidgets.QPushButton(ProfileDialog)
        icon = QtGui.QIcon.fromTheme("system-run")
        self.buttonStartPrymatex.setIcon(icon)
        self.buttonStartPrymatex.setObjectName("buttonStartPrymatex")
        self.horizontalLayout_2.addWidget(self.buttonStartPrymatex)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(ProfileDialog)
        QtCore.QMetaObject.connectSlotsByName(ProfileDialog)

    def retranslateUi(self, ProfileDialog):
        _translate = QtCore.QCoreApplication.translate
        ProfileDialog.setWindowTitle(_translate("ProfileDialog", "Prymatex Choose User Profile"))
        self.label.setText(_translate("ProfileDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Prymatex stores information about your settings, preferences and other items in your user profile.</p></body></html>"))
        self.buttonCreate.setText(_translate("ProfileDialog", "&Create Profile"))
        self.buttonRename.setText(_translate("ProfileDialog", "&Rename Profile"))
        self.buttonDelete.setText(_translate("ProfileDialog", "&Delete Profile"))
        self.checkDontAsk.setText(_translate("ProfileDialog", "Don\'t a&sk at startup"))
        self.buttonExit.setText(_translate("ProfileDialog", "Exit"))
        self.buttonStartPrymatex.setText(_translate("ProfileDialog", "Start Prymatex"))

