# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/fspane.ui'
#
# Created: Sat Feb 20 19:46:04 2010
#      by: PyQt4 UI code generator 4.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_FSPane(object):
    def setupUi(self, FSPane):
        FSPane.setObjectName("FSPane")
        FSPane.resize(293, 457)
        self.verticalLayout = QtGui.QVBoxLayout(FSPane)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.buttonUp = QtGui.QPushButton(FSPane)
        self.buttonUp.setObjectName("buttonUp")
        self.horizontalLayout.addWidget(self.buttonUp)
        self.buttonFilter = QtGui.QPushButton(FSPane)
        self.buttonFilter.setObjectName("buttonFilter")
        self.horizontalLayout.addWidget(self.buttonFilter)
        self.buttonSyncTabFile = QtGui.QPushButton(FSPane)
        self.buttonSyncTabFile.setObjectName("buttonSyncTabFile")
        self.horizontalLayout.addWidget(self.buttonSyncTabFile)
        self.buttonBackRoot = QtGui.QPushButton(FSPane)
        self.buttonBackRoot.setObjectName("buttonBackRoot")
        self.horizontalLayout.addWidget(self.buttonBackRoot)
        self.buttonNextkRoot = QtGui.QPushButton(FSPane)
        self.buttonNextkRoot.setObjectName("buttonNextkRoot")
        self.horizontalLayout.addWidget(self.buttonNextkRoot)
        self.buttonCollapseAll = QtGui.QPushButton(FSPane)
        self.buttonCollapseAll.setObjectName("buttonCollapseAll")
        self.horizontalLayout.addWidget(self.buttonCollapseAll)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tree = FSTree(FSPane)
        self.tree.setObjectName("tree")
        self.verticalLayout.addWidget(self.tree)

        self.retranslateUi(FSPane)
        QtCore.QMetaObject.connectSlotsByName(FSPane)

    def retranslateUi(self, FSPane):
        FSPane.setWindowTitle(QtGui.QApplication.translate("FSPane", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonUp.setText(QtGui.QApplication.translate("FSPane", "Up", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonFilter.setText(QtGui.QApplication.translate("FSPane", "F", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonSyncTabFile.setText(QtGui.QApplication.translate("FSPane", "S", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonBackRoot.setText(QtGui.QApplication.translate("FSPane", "<-", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonNextkRoot.setText(QtGui.QApplication.translate("FSPane", "->", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonCollapseAll.setText(QtGui.QApplication.translate("FSPane", "-", None, QtGui.QApplication.UnicodeUTF8))

from fstree import FSTree

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    FSPane = QtGui.QWidget()
    ui = Ui_FSPane()
    ui.setupUi(FSPane)
    FSPane.show()
    sys.exit(app.exec_())

