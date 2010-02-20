# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/symbols.ui'
#
# Created: Sat Feb 20 18:17:16 2010
#      by: PyQt4 UI code generator 4.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_SymbolList(object):
    def setupUi(self, SymbolList):
        SymbolList.setObjectName("SymbolList")
        SymbolList.resize(184, 364)
        self.verticalLayout = QtGui.QVBoxLayout(SymbolList)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtGui.QLineEdit(SymbolList)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtGui.QPushButton(SymbolList)
        self.pushButton.setStyleSheet("QPushButton {\n"
"padding: 0px;\n"
"margin: 0px;\n"
"}")
        self.pushButton.setFlat(True)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.treeView = QtGui.QTreeView(SymbolList)
        self.treeView.setObjectName("treeView")
        self.verticalLayout.addWidget(self.treeView)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_2 = QtGui.QPushButton(SymbolList)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(SymbolList)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.lineEdit.clear)
        QtCore.QMetaObject.connectSlotsByName(SymbolList)

    def retranslateUi(self, SymbolList):
        SymbolList.setWindowTitle(QtGui.QApplication.translate("SymbolList", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("SymbolList", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("SymbolList", "R", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    SymbolList = QtGui.QWidget()
    ui = Ui_SymbolList()
    ui.setupUi(SymbolList)
    SymbolList.show()
    sys.exit(app.exec_())

