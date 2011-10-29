# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/paneproject.ui'
#
# Created: Fri Oct 28 21:42:07 2011
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ProjectPane(object):
    def setupUi(self, ProjectPane):
        ProjectPane.setObjectName(_fromUtf8("ProjectPane"))
        ProjectPane.resize(213, 464)
        ProjectPane.setWindowTitle(_('Project'))
        self.verticalLayout = QtGui.QVBoxLayout(ProjectPane)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.treeProject = QtGui.QTreeView(ProjectPane)
        self.treeProject.setObjectName(_fromUtf8("treeProject"))
        self.verticalLayout.addWidget(self.treeProject)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.buttonAdd = QtGui.QPushButton(ProjectPane)
        self.buttonAdd.setToolTip(_('Add files/folders'))
        self.buttonAdd.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/resources/actions/list-add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonAdd.setIcon(icon)
        self.buttonAdd.setObjectName(_fromUtf8("buttonAdd"))
        self.horizontalLayout.addWidget(self.buttonAdd)
        self.buttonRemove = QtGui.QPushButton(ProjectPane)
        self.buttonRemove.setToolTip(_('Remove File/Folders'))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/resources/actions/list-remove.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonRemove.setIcon(icon1)
        self.buttonRemove.setObjectName(_fromUtf8("buttonRemove"))
        self.horizontalLayout.addWidget(self.buttonRemove)
        self.buttonSettings = QtGui.QPushButton(ProjectPane)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/resources/actions/configure.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonSettings.setIcon(icon2)
        self.buttonSettings.setObjectName(_fromUtf8("buttonSettings"))
        self.horizontalLayout.addWidget(self.buttonSettings)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ProjectPane)
        QtCore.QMetaObject.connectSlotsByName(ProjectPane)

    def retranslateUi(self, ProjectPane):
        pass

from prymatex import resources_rc
