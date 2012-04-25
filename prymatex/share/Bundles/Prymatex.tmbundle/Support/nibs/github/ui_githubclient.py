# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'githubclient.ui'
#
# Created: Wed Apr 25 20:36:21 2012
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_GitHubClientDialog(object):
    def setupUi(self, GitHubClientDialog):
        GitHubClientDialog.setObjectName(_fromUtf8("GitHubClientDialog"))
        GitHubClientDialog.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(GitHubClientDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(GitHubClientDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.labelSearch = QtGui.QLabel(GitHubClientDialog)
        self.labelSearch.setObjectName(_fromUtf8("labelSearch"))
        self.horizontalLayout_2.addWidget(self.labelSearch)
        self.lineEditQuery = QtGui.QLineEdit(GitHubClientDialog)
        self.lineEditQuery.setObjectName(_fromUtf8("lineEditQuery"))
        self.horizontalLayout_2.addWidget(self.lineEditQuery)
        self.buttonSearch = QtGui.QPushButton(GitHubClientDialog)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.buttonSearch.setFont(font)
        self.buttonSearch.setObjectName(_fromUtf8("buttonSearch"))
        self.horizontalLayout_2.addWidget(self.buttonSearch)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.tableViewResults = QtGui.QTableView(GitHubClientDialog)
        self.tableViewResults.setObjectName(_fromUtf8("tableViewResults"))
        self.verticalLayout.addWidget(self.tableViewResults)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.labelBundle = QtGui.QLabel(GitHubClientDialog)
        self.labelBundle.setObjectName(_fromUtf8("labelBundle"))
        self.horizontalLayout.addWidget(self.labelBundle)
        self.lineEditBundle = QtGui.QLineEdit(GitHubClientDialog)
        self.lineEditBundle.setObjectName(_fromUtf8("lineEditBundle"))
        self.horizontalLayout.addWidget(self.lineEditBundle)
        self.buttonClone = QtGui.QPushButton(GitHubClientDialog)
        self.buttonClone.setObjectName(_fromUtf8("buttonClone"))
        self.horizontalLayout.addWidget(self.buttonClone)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(GitHubClientDialog)
        QtCore.QMetaObject.connectSlotsByName(GitHubClientDialog)

    def retranslateUi(self, GitHubClientDialog):
        GitHubClientDialog.setWindowTitle(QtGui.QApplication.translate("GitHubClientDialog", "GitHub Client", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("GitHubClientDialog", "<html><head/><body><p>This tool allows you to get TextMate bundles from <br/>GitHub and install them in your current profile.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelSearch.setText(QtGui.QApplication.translate("GitHubClientDialog", "Search:", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonSearch.setText(QtGui.QApplication.translate("GitHubClientDialog", "Search Github", None, QtGui.QApplication.UnicodeUTF8))
        self.labelBundle.setText(QtGui.QApplication.translate("GitHubClientDialog", "Bundle:", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonClone.setText(QtGui.QApplication.translate("GitHubClientDialog", "Clone", None, QtGui.QApplication.UnicodeUTF8))

