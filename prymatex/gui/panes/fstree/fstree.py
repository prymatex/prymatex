#!/usr/bin/env python
#-*- encoding: utf-8 -*-
from PyQt4.QtGui import QTreeView, QFileSystemModel, QMenu, QAction, QMessageBox, qApp
from PyQt4.QtGui import QInputDialog, QApplication, QPixmap, QIcon
from PyQt4.QtCore import QMetaObject, Qt, pyqtSignature, SIGNAL, QDir, pyqtSignal
import os
import shutil
from os.path import join, abspath, isfile, isdir, dirname
import logging
from prymatex.gui.editor.editorwidget import PMXEditorWidget
from prymatex.core.base import PMXObject

logger = logging.getLogger(__name__)

class FSTree(QTreeView, PMXObject):
    '''
    File tree panel
    '''
    rootChanged = pyqtSignal(object)
    
    class Meta:
        settings = 'fspane.fstree'
    
    def __init__(self, parent = None):
        QTreeView.__init__(self, parent)
        
        
        self.dirmodelFiles = QFileSystemModel(self)
        self.dirmodelFiles.setRootPath('.')
        self.createMenus()        
        self.setModel(self.dirmodelFiles)
        for i in range(1,self.dirmodelFiles.columnCount()):
            self.setColumnHidden(i, True)
        self.setAnimated(False)
        self.setIndentation(20)
        self.setSortingEnabled(True)
        self.dirmodelFiles.sort(0)
        print self.mainWindow
        #self.mainWindow.tabWidget.currentEditorChanged.connect(self.focusWidgetPath)
        self.setExpandsOnDoubleClick(True)
        QMetaObject.connectSlotsByName(self)
    
    def followWidgetFoucs(self, follow):
        print "Follow", follow
    
    
    def focusWidgetPath(self, widget):
        '''
        Editor has been hanged in the main window
        '''
        # Is sync enabled?
        if not self.parent().buttonSyncTabFile.isChecked():
            # The Sync checkbox is not checked so we should not
            # foucs the current file in the tree
            self.debug("No sincronizado")
            
        elif isinstance(widget, (PMXEditorWidget, )):
            if widget.file.path:
                path = widget.file.path
                index = self.model().index(path)
                self.setCurrentIndex(index) 
    
    def createMenus(self):
        from prymatex.utils.i18n import ugettext as _
        # File Menu
        self.menuFile = QMenu(self)
        self.menuFile.setObjectName('menuFile')
        
        # Directory Menu
        self.menuDir = QMenu(self)
        self.menuDir.setObjectName('menuDir')
        
        # Default menu 
        self.defaultMenu = QMenu(self)
        self.defaultMenu.setObjectName("defaultMenu")
        
        # Actions for those menus
        self.actionCopyPathToClipBoard = QAction(_("Copy Path To &Clipboard"), self)
        self.actionCopyPathToClipBoard.setObjectName("actionCopyPathToClipBoard")
        self.actionCopyPathToClipBoard.triggered.connect(self.copyPathToClipboard)
        self.menuFile.addAction(self.actionCopyPathToClipBoard)
        
        self.actionRename = QAction(_("&Rename"), self)
        self.actionRename.setIcon(QIcon(":/icons/actions/edit-rename.png"))
        self.actionRename.setObjectName("actionRename")
        self.menuFile.addAction(self.actionRename)
        
        self.actionDelete = QAction(_("&Delete"), self)
        self.actionDelete.setObjectName("actionDelete")
        self.menuFile.addAction(self.actionDelete)
        
        self.actionFileOpen = QAction(_("&Open"), self)
        self.actionFileOpen.setObjectName("actionFileOpen")
        self.actionFileOpen.setIcon(QIcon(":/icons/actions/document-open.png"))
        self.menuFile.addAction(self.actionFileOpen)
        
        self.actionRefresh = QAction(_("&Refresh"), self)
        self.actionRefresh.setIcon(QIcon(":/icons/actions/view-refresh.png"))
        self.actionRefresh.setObjectName("actionRefresh")
        self.menuFile.addAction(self.actionRefresh)
        
        self.actionProperties = QAction(_("&Properties"), self)
        self.actionProperties.setObjectName("actionProperties")
        self.actionProperties.setIcon(QIcon(":/icons/actions/document-properties.png"))
        #self.actionProperties.setShortcut("")
        self.menuFile.addAction(self.actionProperties)
        
        
        # Directory Menus
        self.menuNewFileSystemElement = QMenu(_("&New.."), self)
        self.menuNewFileSystemElement.setObjectName('menuNewFileSystemElement')
        self.menuNewFileSystemElement.setIcon(QIcon(":/icons/actions/document-new.png"))
        self.actionFileNew = self.menuNewFileSystemElement.addAction('File')
        self.actionFileNew.setObjectName("actionFileNew")
        
        self.menuNewFileSystemElement.setObjectName('newFile')
        self.actionDirNew = self.menuNewFileSystemElement.addAction('Directory')
        self.actionDirNew.setObjectName("actionDirNew")
        
        
        self.menuDir.addMenu(self.menuNewFileSystemElement)
        self.menuDir.addAction(self.actionCopyPathToClipBoard)
        
        self.actionSetAsRoot = QAction(_("&Set as root"), self)
        self.actionSetAsRoot.setObjectName("actionSetAsRoot")
        
        self.actionCreateProjectOnPath = QAction(_("Create project"
                                                 " on this path"), self)
        self.actionCreateProjectOnPath.setObjectName('actionCreateProjectOnPath')
        
                                                 
                                                 
        
        
        # Menu oerder
        self.menuDir.addAction(self.actionSetAsRoot)
        
        self.menuDir.addAction(self.actionCreateProjectOnPath)
        self.menuDir.addAction(self.actionRefresh)
        
        self.menuDir.addAction(self.actionRename)
        self.menuDir.addAction(self.actionDelete)
        
        self.menuDir.addAction(self.actionProperties)
        
        
        
        self.defaultMenu.addMenu(self.menuNewFileSystemElement)
        self.defaultMenu.addAction(self.actionRefresh)
        #self.defaultMenu.addAction()
    
    def copyPathToClipboard(self):
        paths = map(self.model().filePath, self.selectedIndexes())
        if len(paths) == 1:
            QApplication.clipboard().setText(paths[0])
            
    
    def mouseDoubleClickEvent(self, event):
        if event.button() != Qt.LeftButton:
            return
        QTreeView.mouseDoubleClickEvent(self, event)
        
        index = self.indexAt(event.pos())
        path = unicode(self.model().filePath(index))
        print path
        if os.path.isfile(path):
            self.mainWindow.openFile(path)
            
        if os.path.isdir(path):
            if self.model().hasChildren(index):
                self.setRootIndex(index)

        
    def goUp(self):
        current_top = unicode(self.model().filePath(self.rootIndex()))
        #self.tree.setRootIndex(self.tree.model().index(QDir.currentPath()))
        upper = abspath(join(current_top, '..'))
        
        if upper != current_top:
            self.setRootIndex(self.model().index(upper))
    
    def on_actionSetAsRoot_triggered(self):
        index_list = self.selectedIndexes()
        if len(index_list) == 1:
            index = index_list[0]
            self.setRootIndex(index)
    
    
    
    def mouseReleaseEvent(self, event):
        QTreeView.mouseReleaseEvent(self, event)
        if event.button() == Qt.RightButton:
            index = self.indexAt(event.pos())
            data = unicode(self.model().filePath(index))
            if os.path.isfile(data):
                self.menuFile.popup(event.globalPos())
            elif os.path.isdir(data):
                self.menuDir.popup(event.globalPos())
            else:
                self.defaultMenu.popup(event.globalPos())
    

    @property
    def current_selected_path(self):
        index_list = self.selectedIndexes()
        if len(index_list) == 1:
            index = index_list[0]
        else:
            index = self.rootIndex()
        return unicode(self.model().filePath(index))
    
    def on_actionCopyPathToClipboard_triggered(self):
        index_list = self.selectedIndexes()
        if len(index_list) == 1:
            index = index_list[0]
            #QClipboard.setText(self.model().data(index))
            qApp.instance().clipboard().setText(self.model().filePath(index))
    
    
    @pyqtSignature('')
    def on_actionDirNew_triggered(self):
        from prymatex.utils.i18n import ugettext as _
        
        pth = self.current_selected_path
        base = isdir(pth) and pth or dirname(pth)
        
        
        newdir_name, ok = QInputDialog.getText(self, _("New directoy name"),
                             _("Please enter the new directoy name in < /br>%s:", base))
        print newdir_name, ok
    
    @pyqtSignature('')
    def on_actionFileNew_triggered(self):
        print ("New file")
    
    @pyqtSignature('')
    def on_actionRefresh_triggered(self):
        self.model().refresh()
        print "Refresh"
    
    @pyqtSignature('')
    def on_actionDelete_triggered(self):
        curpath = abspath(self.current_selected_path)
        filename = curpath.split(os.sep)[-1]
#        if isfile(filename):
#            file = basename(filename)
#        else:
#            filename = file.split(os.sep)[-1]
            
        resp = QMessageBox.question(self, _("Deletion Confirmation"), 
                             _("Are you sure you want to delete <b>%s</b>?", 
                               filename),
                               QMessageBox.Ok | QMessageBox.No | QMessageBox.Cancel
                             )
        if resp == QMessageBox.Ok:
            if isfile(curpath):
                # Primero hay que cerrar el editor si hay
                os.unlink(curpath)
            else:
                shutil.rmtree(curpath)
            self.actionRefresh.trigger()

    def setRootIndex(self, index):
        path = self.model().filePath(index)
        super(FSTree, self).setRootIndex(index)
        self.rootChanged.emit(path)
        
