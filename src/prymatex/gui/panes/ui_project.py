# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/project.ui'
#
# Created: Sat Feb 20 18:10:45 2010
#      by: PyQt4 UI code generator 4.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ProjectPane(object):
    def setupUi(self, ProjectPane):
        ProjectPane.setObjectName("ProjectPane")
        ProjectPane.resize(213, 464)
        self.verticalLayout = QtGui.QVBoxLayout(ProjectPane)
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeProject = QtGui.QTreeView(ProjectPane)
        self.treeProject.setObjectName("treeProject")
        self.verticalLayout.addWidget(self.treeProject)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.buttonAdd = QtGui.QPushButton(ProjectPane)
        self.buttonAdd.setObjectName("buttonAdd")
        self.horizontalLayout.addWidget(self.buttonAdd)
        self.buttonRemove = QtGui.QPushButton(ProjectPane)
        self.buttonRemove.setObjectName("buttonRemove")
        self.horizontalLayout.addWidget(self.buttonRemove)
        self.buttonSettings = QtGui.QPushButton(ProjectPane)
        self.buttonSettings.setObjectName("buttonSettings")
        self.horizontalLayout.addWidget(self.buttonSettings)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ProjectPane)
        QtCore.QMetaObject.connectSlotsByName(ProjectPane)

    def retranslateUi(self, ProjectPane):
        ProjectPane.setWindowTitle(QtGui.QApplication.translate("ProjectPane", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonAdd.setToolTip(QtGui.QApplication.translate("ProjectPane", "Add files/folders", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonAdd.setText(QtGui.QApplication.translate("ProjectPane", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonRemove.setToolTip(QtGui.QApplication.translate("ProjectPane", "Remove File/Folders", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonRemove.setText(QtGui.QApplication.translate("ProjectPane", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonSettings.setText(QtGui.QApplication.translate("ProjectPane", "S", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ProjectPane = QtGui.QWidget()
    ui = Ui_ProjectPane()
    ui.setupUi(ProjectPane)
    ProjectPane.show()
    sys.exit(app.exec_())

