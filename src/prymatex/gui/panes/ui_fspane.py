# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/fspane.ui'
#
# Created: Mon Feb 22 20:33:48 2010
#      by: PyQt4 UI code generator 4.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_FSPane(object):
    def setupUi(self, FSPane):
        FSPane.setObjectName("FSPane")
        FSPane.resize(293, 457)
        FSPane.setStyleSheet("QPushButton {\n"
"    padding: 5px;\n"
"\n"
"}")
        self.verticalLayout = QtGui.QVBoxLayout(FSPane)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.buttonUp = QtGui.QPushButton(FSPane)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/resources/actions/go-up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonUp.setIcon(icon)
        self.buttonUp.setObjectName("buttonUp")
        self.horizontalLayout.addWidget(self.buttonUp)
        self.buttonFilter = QtGui.QPushButton(FSPane)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/resources/actions/view-filter.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonFilter.setIcon(icon1)
        self.buttonFilter.setObjectName("buttonFilter")
        self.horizontalLayout.addWidget(self.buttonFilter)
        self.buttonSyncTabFile = QtGui.QPushButton(FSPane)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/resources/actions/system-switch-user.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonSyncTabFile.setIcon(icon2)
        self.buttonSyncTabFile.setObjectName("buttonSyncTabFile")
        self.horizontalLayout.addWidget(self.buttonSyncTabFile)
        self.buttonBackRoot = QtGui.QPushButton(FSPane)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/resources/actions/go-previous.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonBackRoot.setIcon(icon3)
        self.buttonBackRoot.setObjectName("buttonBackRoot")
        self.horizontalLayout.addWidget(self.buttonBackRoot)
        self.buttonNextkRoot = QtGui.QPushButton(FSPane)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/resources/actions/go-next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonNextkRoot.setIcon(icon4)
        self.buttonNextkRoot.setObjectName("buttonNextkRoot")
        self.horizontalLayout.addWidget(self.buttonNextkRoot)
        self.buttonCollapseAll = QtGui.QPushButton(FSPane)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/resources/actions/zoom-out.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonCollapseAll.setIcon(icon5)
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

from fstree import FSTree
import res_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    FSPane = QtGui.QWidget()
    ui = Ui_FSPane()
    ui.setupUi(FSPane)
    FSPane.show()
    sys.exit(app.exec_())

