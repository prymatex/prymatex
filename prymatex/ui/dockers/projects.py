# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/diego/Projects/prymatex/resources/ui/dockers/projects.ui'
#
# Created: Wed May 27 08:01:35 2015
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ProjectsDock(object):
    def setupUi(self, ProjectsDock):
        ProjectsDock.setObjectName("ProjectsDock")
        ProjectsDock.resize(341, 484)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.buttonsLayout = QtWidgets.QHBoxLayout()
        self.buttonsLayout.setSpacing(2)
        self.buttonsLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.buttonsLayout.setObjectName("buttonsLayout")
        spacerItem = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.buttonsLayout.addItem(spacerItem)
        self.pushButtonGoPrevious = QtWidgets.QPushButton(self.dockWidgetContents)
        icon = QtGui.QIcon.fromTheme("go-previous")
        self.pushButtonGoPrevious.setIcon(icon)
        self.pushButtonGoPrevious.setObjectName("pushButtonGoPrevious")
        self.buttonsLayout.addWidget(self.pushButtonGoPrevious)
        self.pushButtonGoNext = QtWidgets.QPushButton(self.dockWidgetContents)
        icon = QtGui.QIcon.fromTheme("go-next")
        self.pushButtonGoNext.setIcon(icon)
        self.pushButtonGoNext.setObjectName("pushButtonGoNext")
        self.buttonsLayout.addWidget(self.pushButtonGoNext)
        self.pushButtonGoUp = QtWidgets.QPushButton(self.dockWidgetContents)
        icon = QtGui.QIcon.fromTheme("go-up")
        self.pushButtonGoUp.setIcon(icon)
        self.pushButtonGoUp.setObjectName("pushButtonGoUp")
        self.buttonsLayout.addWidget(self.pushButtonGoUp)
        self.line = QtWidgets.QFrame(self.dockWidgetContents)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.buttonsLayout.addWidget(self.line)
        self.toolButtonOptions = QtWidgets.QToolButton(self.dockWidgetContents)
        icon = QtGui.QIcon.fromTheme("options")
        self.toolButtonOptions.setIcon(icon)
        self.toolButtonOptions.setObjectName("toolButtonOptions")
        self.buttonsLayout.addWidget(self.toolButtonOptions)
        self.verticalLayout.addLayout(self.buttonsLayout)
        self.treeViewProjects = QtWidgets.QTreeView(self.dockWidgetContents)
        self.treeViewProjects.setUniformRowHeights(True)
        self.treeViewProjects.setHeaderHidden(True)
        self.treeViewProjects.setObjectName("treeViewProjects")
        self.verticalLayout.addWidget(self.treeViewProjects)
        ProjectsDock.setWidget(self.dockWidgetContents)

        self.retranslateUi(ProjectsDock)
        QtCore.QMetaObject.connectSlotsByName(ProjectsDock)

    def retranslateUi(self, ProjectsDock):
        _translate = QtCore.QCoreApplication.translate
        ProjectsDock.setWindowTitle(_translate("ProjectsDock", "Projects"))
        self.pushButtonGoPrevious.setToolTip(_translate("ProjectsDock", "Go previous place"))
        self.pushButtonGoNext.setToolTip(_translate("ProjectsDock", "Go next place"))
        self.pushButtonGoUp.setToolTip(_translate("ProjectsDock", "Go up one level"))

