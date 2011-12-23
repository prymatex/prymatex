# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/dockers/projects.ui'
#
# Created: Thu Dec 22 23:22:43 2011
#      by: PyQt4 UI code generator 4.8.4
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
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.treeViewProjects = QtGui.QTreeView(self.dockWidgetContents)
        self.treeViewProjects.setUniformRowHeights(True)
        self.treeViewProjects.setHeaderHidden(True)
        self.treeViewProjects.setObjectName(_fromUtf8("treeViewProjects"))
        self.verticalLayout.addWidget(self.treeViewProjects)
        ProjectsDock.setWidget(self.dockWidgetContents)
        self.actionNewFile = QtGui.QAction(ProjectsDock)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/document-new.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNewFile.setIcon(icon)
        self.actionNewFile.setObjectName(_fromUtf8("actionNewFile"))
        self.actionNewFolder = QtGui.QAction(ProjectsDock)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/folder-new.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNewFolder.setIcon(icon1)
        self.actionNewFolder.setObjectName(_fromUtf8("actionNewFolder"))
        self.actionNewFromTemplate = QtGui.QAction(ProjectsDock)
        self.actionNewFromTemplate.setIcon(icon)
        self.actionNewFromTemplate.setObjectName(_fromUtf8("actionNewFromTemplate"))
        self.actionDelete = QtGui.QAction(ProjectsDock)
        self.actionDelete.setObjectName(_fromUtf8("actionDelete"))
        self.actionNewProject = QtGui.QAction(ProjectsDock)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/project-development-new-template.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNewProject.setIcon(icon2)
        self.actionNewProject.setObjectName(_fromUtf8("actionNewProject"))
        self.actionCloseProject = QtGui.QAction(ProjectsDock)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/project-development-close.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCloseProject.setIcon(icon3)
        self.actionCloseProject.setObjectName(_fromUtf8("actionCloseProject"))
        self.actionOpenProject = QtGui.QAction(ProjectsDock)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/project-open.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpenProject.setIcon(icon4)
        self.actionOpenProject.setObjectName(_fromUtf8("actionOpenProject"))
        self.actionProperties = QtGui.QAction(ProjectsDock)
        self.actionProperties.setObjectName(_fromUtf8("actionProperties"))
        self.actionRefresh = QtGui.QAction(ProjectsDock)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/actions/view-refresh.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRefresh.setIcon(icon5)
        self.actionRefresh.setObjectName(_fromUtf8("actionRefresh"))
        self.actionOpen = QtGui.QAction(ProjectsDock)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionOpenSystemEditor = QtGui.QAction(ProjectsDock)
        self.actionOpenSystemEditor.setObjectName(_fromUtf8("actionOpenSystemEditor"))
        self.actionOpenDefaultEditor = QtGui.QAction(ProjectsDock)
        self.actionOpenDefaultEditor.setObjectName(_fromUtf8("actionOpenDefaultEditor"))

        self.retranslateUi(ProjectsDock)
        QtCore.QMetaObject.connectSlotsByName(ProjectsDock)

    def retranslateUi(self, ProjectsDock):
        ProjectsDock.setWindowTitle(_('Projects'))
        self.actionNewFile.setText(_('File'))
        self.actionNewFolder.setText(_('Folder'))
        self.actionNewFromTemplate.setText(_('From Template'))
        self.actionDelete.setText(_('Delete'))
        self.actionNewProject.setText(_('Project'))
        self.actionCloseProject.setText(_('Close'))
        self.actionOpenProject.setText(_('Open'))
        self.actionProperties.setText(_('Properties'))
        self.actionRefresh.setText(_('Refresh'))
        self.actionRefresh.setShortcut(_('F5'))
        self.actionOpen.setText(_('Open'))
        self.actionOpenSystemEditor.setText(_('System Editor'))
        self.actionOpenDefaultEditor.setText(_('Default Editor'))

from prymatex import resources_rc
