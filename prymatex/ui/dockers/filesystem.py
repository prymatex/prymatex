# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/sda5/Projects/Prymatex/prymatex/resources/ui/dockers/filesystem.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FileSystemDock(object):
    def setupUi(self, FileSystemDock):
        FileSystemDock.setObjectName("FileSystemDock")
        FileSystemDock.resize(347, 484)
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
        self.comboBoxLocation = QtWidgets.QComboBox(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxLocation.sizePolicy().hasHeightForWidth())
        self.comboBoxLocation.setSizePolicy(sizePolicy)
        self.comboBoxLocation.setEditable(True)
        self.comboBoxLocation.setObjectName("comboBoxLocation")
        self.verticalLayout.addWidget(self.comboBoxLocation)
        self.treeViewFileSystem = QtWidgets.QTreeView(self.dockWidgetContents)
        self.treeViewFileSystem.setObjectName("treeViewFileSystem")
        self.verticalLayout.addWidget(self.treeViewFileSystem)
        FileSystemDock.setWidget(self.dockWidgetContents)

        self.retranslateUi(FileSystemDock)
        QtCore.QMetaObject.connectSlotsByName(FileSystemDock)

    def retranslateUi(self, FileSystemDock):
        _translate = QtCore.QCoreApplication.translate
        FileSystemDock.setWindowTitle(_translate("FileSystemDock", "Files"))
        self.pushButtonGoPrevious.setToolTip(_translate("FileSystemDock", "Go previous place"))
        self.pushButtonGoNext.setToolTip(_translate("FileSystemDock", "Go next place"))
        self.pushButtonGoUp.setToolTip(_translate("FileSystemDock", "Go up one level"))
        self.comboBoxLocation.setToolTip(_translate("FileSystemDock", "Folders"))

