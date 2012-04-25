# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'githubclient.ui'
#
# Created: Tue Mar 13 00:30:54 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_GithubClient(object):
    def setupUi(self, GithubClient):
        GithubClient.setObjectName(_fromUtf8("GithubClient"))
        GithubClient.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(GithubClient)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(GithubClient)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(GithubClient)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEditQuery = QtGui.QLineEdit(GithubClient)
        self.lineEditQuery.setObjectName(_fromUtf8("lineEditQuery"))
        self.horizontalLayout_2.addWidget(self.lineEditQuery)
        self.pushButtonSearch = QtGui.QPushButton(GithubClient)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonSearch.setFont(font)
        self.pushButtonSearch.setObjectName(_fromUtf8("pushButtonSearch"))
        self.horizontalLayout_2.addWidget(self.pushButtonSearch)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.tableViewResults = QtGui.QTableView(GithubClient)
        self.tableViewResults.setObjectName(_fromUtf8("tableViewResults"))
        self.verticalLayout.addWidget(self.tableViewResults)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_5 = QtGui.QPushButton(GithubClient)
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.horizontalLayout.addWidget(self.pushButton_5)
        self.pushButton_2 = QtGui.QPushButton(GithubClient)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushClose = QtGui.QPushButton(GithubClient)
        self.pushClose.setObjectName(_fromUtf8("pushClose"))
        self.horizontalLayout.addWidget(self.pushClose)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(GithubClient)
        QtCore.QObject.connect(self.pushClose, QtCore.SIGNAL(_fromUtf8("clicked()")), GithubClient.close)
        QtCore.QMetaObject.connectSlotsByName(GithubClient)

    def retranslateUi(self, GithubClient):
        GithubClient.setWindowTitle(QtGui.QApplication.translate("GithubClient", "GitHub Client", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("GithubClient", "<html><head/><body><p>This tool allows you to get TextMate bundles from <br/>GitHub and install them in your current profile.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("GithubClient", "Search:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonSearch.setText(QtGui.QApplication.translate("GithubClient", "Search Github", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_5.setText(QtGui.QApplication.translate("GithubClient", "Info", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("GithubClient", "Actions", None, QtGui.QApplication.UnicodeUTF8))
        self.pushClose.setText(QtGui.QApplication.translate("GithubClient", "Close", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    GithubClient = QtGui.QWidget()
    ui = Ui_GithubClient()
    ui.setupUi(GithubClient)
    GithubClient.show()
    sys.exit(app.exec_())

