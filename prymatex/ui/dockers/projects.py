# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/dockers/projects.ui'
#
# Created: Tue Dec  6 17:39:08 2011
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from prymatex.utils.i18n import ugettext as _
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ProjectsDock(object):
    def setupUi(self, ProjectsDock):
        ProjectsDock.setObjectName(_fromUtf8("ProjectsDock"))
        ProjectsDock.resize(330, 484)
        ProjectsDock.setWindowTitle(_('Projects'))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.treeViewProjects = QtGui.QTreeView(self.dockWidgetContents)
        self.treeViewProjects.setUniformRowHeights(True)
        self.treeViewProjects.setObjectName(_fromUtf8("treeViewProjects"))
        self.treeViewProjects.header().setVisible(False)
        self.verticalLayout.addWidget(self.treeViewProjects)
        ProjectsDock.setWidget(self.dockWidgetContents)
        self.actionNewFile = QtGui.QAction(ProjectsDock)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/document-new.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNewFile.setIcon(icon)
        self.actionNewFile.setText(_('File'))
        self.actionNewFile.setObjectName(_fromUtf8("actionNewFile"))
        self.actionNewFolder = QtGui.QAction(ProjectsDock)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/folder-new.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNewFolder.setIcon(icon1)
        self.actionNewFolder.setText(_('Folder'))
        self.actionNewFolder.setObjectName(_fromUtf8("actionNewFolder"))
        self.actionNewFromTemplate = QtGui.QAction(ProjectsDock)
        self.actionNewFromTemplate.setIcon(icon)
        self.actionNewFromTemplate.setText(_('From Template'))
        self.actionNewFromTemplate.setObjectName(_fromUtf8("actionNewFromTemplate"))
        self.actionDelete = QtGui.QAction(ProjectsDock)
        self.actionDelete.setText(_('Delete'))
        self.actionDelete.setObjectName(_fromUtf8("actionDelete"))
        self.actionNewProject = QtGui.QAction(ProjectsDock)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/project-development-new-template.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNewProject.setIcon(icon2)
        self.actionNewProject.setText(_('Project'))
        self.actionNewProject.setObjectName(_fromUtf8("actionNewProject"))
        self.actionCloseProject = QtGui.QAction(ProjectsDock)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/project-development-close.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCloseProject.setIcon(icon3)
        self.actionCloseProject.setText(_('Close'))
        self.actionCloseProject.setObjectName(_fromUtf8("actionCloseProject"))
        self.actionOpenProject = QtGui.QAction(ProjectsDock)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/project-open.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpenProject.setIcon(icon4)
        self.actionOpenProject.setText(_('Open'))
        self.actionOpenProject.setObjectName(_fromUtf8("actionOpenProject"))

        self.retranslateUi(ProjectsDock)
        QtCore.QMetaObject.connectSlotsByName(ProjectsDock)

    def retranslateUi(self, ProjectsDock):
        pass

from prymatex import resources_rc
