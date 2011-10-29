# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/panefilesystem.ui'
#
# Created: Fri Oct 28 21:42:06 2011
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_FileSystemDock(object):
    def setupUi(self, FileSystemDock):
        FileSystemDock.setObjectName(_fromUtf8("FileSystemDock"))
        FileSystemDock.resize(330, 484)
        FileSystemDock.setWindowTitle(_('File System'))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.buttonsLayout = QtGui.QHBoxLayout()
        self.buttonsLayout.setSpacing(2)
        self.buttonsLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.buttonsLayout.setObjectName(_fromUtf8("buttonsLayout"))
        self.pushButtonUp = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButtonUp.setMaximumSize(QtCore.QSize(24, 24))
        self.pushButtonUp.setToolTip(_('Go up one level'))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/go-up.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonUp.setIcon(icon)
        self.pushButtonUp.setFlat(True)
        self.pushButtonUp.setObjectName(_fromUtf8("pushButtonUp"))
        self.buttonsLayout.addWidget(self.pushButtonUp)
        self.pushButtonBack = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButtonBack.setMaximumSize(QtCore.QSize(24, 24))
        self.pushButtonBack.setToolTip(_('Go previous place'))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/go-previous.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonBack.setIcon(icon1)
        self.pushButtonBack.setFlat(True)
        self.pushButtonBack.setObjectName(_fromUtf8("pushButtonBack"))
        self.buttonsLayout.addWidget(self.pushButtonBack)
        self.pushButtonFoward = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButtonFoward.setMaximumSize(QtCore.QSize(24, 24))
        self.pushButtonFoward.setToolTip(_('Go next place'))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/go-next.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonFoward.setIcon(icon2)
        self.pushButtonFoward.setFlat(True)
        self.pushButtonFoward.setObjectName(_fromUtf8("pushButtonFoward"))
        self.buttonsLayout.addWidget(self.pushButtonFoward)
        self.pushButtonSync = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButtonSync.setMaximumSize(QtCore.QSize(24, 24))
        self.pushButtonSync.setToolTip(_('Sync folder with current editor file path'))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/system-switch-user.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonSync.setIcon(icon3)
        self.pushButtonSync.setFlat(True)
        self.pushButtonSync.setObjectName(_fromUtf8("pushButtonSync"))
        self.buttonsLayout.addWidget(self.pushButtonSync)
        spacerItem = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.buttonsLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.buttonsLayout)
        self.comboBoxLocation = QtGui.QComboBox(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxLocation.sizePolicy().hasHeightForWidth())
        self.comboBoxLocation.setSizePolicy(sizePolicy)
        self.comboBoxLocation.setToolTip(_('Folders'))
        self.comboBoxLocation.setEditable(True)
        self.comboBoxLocation.setObjectName(_fromUtf8("comboBoxLocation"))
        self.verticalLayout.addWidget(self.comboBoxLocation)
        self.treeViewFileSystem = QtGui.QTreeView(self.dockWidgetContents)
        self.treeViewFileSystem.setObjectName(_fromUtf8("treeViewFileSystem"))
        self.verticalLayout.addWidget(self.treeViewFileSystem)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.dockWidgetContents)
        self.label.setText(_('Filter:'))
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.lineEditFilter = QtGui.QLineEdit(self.dockWidgetContents)
        self.lineEditFilter.setObjectName(_fromUtf8("lineEditFilter"))
        self.horizontalLayout.addWidget(self.lineEditFilter)
        self.verticalLayout.addLayout(self.horizontalLayout)
        FileSystemDock.setWidget(self.dockWidgetContents)
        self.actionNewFile = QtGui.QAction(FileSystemDock)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/document-new.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNewFile.setIcon(icon4)
        self.actionNewFile.setText(_('File'))
        self.actionNewFile.setObjectName(_fromUtf8("actionNewFile"))
        self.actionNewFolder = QtGui.QAction(FileSystemDock)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/folder-new.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNewFolder.setIcon(icon5)
        self.actionNewFolder.setText(_('Folder'))
        self.actionNewFolder.setObjectName(_fromUtf8("actionNewFolder"))
        self.actionNewFromTemplate = QtGui.QAction(FileSystemDock)
        self.actionNewFromTemplate.setText(_('From Template'))
        self.actionNewFromTemplate.setObjectName(_fromUtf8("actionNewFromTemplate"))
        self.actionDelete = QtGui.QAction(FileSystemDock)
        self.actionDelete.setText(_('Delete'))
        self.actionDelete.setObjectName(_fromUtf8("actionDelete"))
        self.actionOrderByName = QtGui.QAction(FileSystemDock)
        self.actionOrderByName.setCheckable(True)
        self.actionOrderByName.setText(_('By Name'))
        self.actionOrderByName.setObjectName(_fromUtf8("actionOrderByName"))
        self.actionOrderBySize = QtGui.QAction(FileSystemDock)
        self.actionOrderBySize.setCheckable(True)
        self.actionOrderBySize.setText(_('By Size'))
        self.actionOrderBySize.setObjectName(_fromUtf8("actionOrderBySize"))
        self.actionOrderByDate = QtGui.QAction(FileSystemDock)
        self.actionOrderByDate.setCheckable(True)
        self.actionOrderByDate.setText(_('By Date'))
        self.actionOrderByDate.setObjectName(_fromUtf8("actionOrderByDate"))
        self.actionOrderByType = QtGui.QAction(FileSystemDock)
        self.actionOrderByType.setCheckable(True)
        self.actionOrderByType.setText(_('By Type'))
        self.actionOrderByType.setObjectName(_fromUtf8("actionOrderByType"))
        self.actionOrderDescending = QtGui.QAction(FileSystemDock)
        self.actionOrderDescending.setCheckable(True)
        self.actionOrderDescending.setText(_('Descending'))
        self.actionOrderDescending.setObjectName(_fromUtf8("actionOrderDescending"))
        self.actionOrderFoldersFirst = QtGui.QAction(FileSystemDock)
        self.actionOrderFoldersFirst.setCheckable(True)
        self.actionOrderFoldersFirst.setText(_('Folders First'))
        self.actionOrderFoldersFirst.setObjectName(_fromUtf8("actionOrderFoldersFirst"))

        self.retranslateUi(FileSystemDock)
        QtCore.QMetaObject.connectSlotsByName(FileSystemDock)

    def retranslateUi(self, FileSystemDock):
        pass

from prymatex import resources_rc
