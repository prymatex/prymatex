from PyQt4.QtGui import *
from PyQt4.QtCore import *
from prymatex.gui.panes import ShowHideSignalsMixin
import shutil
import os
from os.path import abspath, join, dirname, isdir, isfile, basename
from prymatex.lib.i18n import ugettext as _
from prymatex.gui.utils import createButton, addActionsToMenu
 
#from pr

class QActionPushButton(QPushButton):
    
    def __init__(self, action):
        assert isinstance(action, QAction)
        QPushButton.__init__(self)
        self._action = action
        self.copyParams()
        self.connect(self, SIGNAL("pressed()"), self._action, SLOT("trigger()"))
        
    def copyParams(self):
        self.setText(self._action.text())
#        setTextOrig = self._action.setText
        self.setIcon(self._action.icon())
        self.setToolTip(self._action.toolTip())
    
    
class FSPaneWidget(QWidget, ShowHideSignalsMixin):
    
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setupGui()
        QMetaObject.connectSlotsByName(self)
        self.tree.setRootIndex(self.tree.model().index(QDir.currentPath()))
        
    def setupGui(self):
        mainlayout = QVBoxLayout()
        button_layout = QHBoxLayout()
        # Oneliner Watchout!! Sorry
        self.actionUp = QAction(_("Up"), self)
        self.actionUp.setObjectName('actionUp')
        self.buttonUp = QActionPushButton(self.actionUp)
        button_layout.addWidget(self.buttonUp)
        
        self.buttonFilter = QPushButton(_("F"), self)
        self.buttonFilter.setObjectName("buttonFilter")
        self.buttonFilter.setToolTip("Filter Settings")
        button_layout.addWidget(self.buttonFilter)
        
        self.buttonSyncTabFile = QPushButton(_("S"), self)
        self.buttonSyncTabFile.setToolTip(_("Sync opened file"))
        self.buttonSyncTabFile.setObjectName("self.buttonSyncTabFile")
        # Keeping it simple
        #self.buttonSyncTabFile.setCheckable(True)
        button_layout.addWidget(self.buttonSyncTabFile)
        
        
        self.buttonBackRoot = QPushButton(_("<-"), self)
        self.buttonBackRoot.setToolTip(_("Back to previous location"))
        self.buttonBackRoot.setEnabled(False)
        self.buttonBackRoot.setObjectName("buttonBackRoot")
        button_layout.addWidget(self.buttonBackRoot)
        
        self.buttonNextRoot = QPushButton(_("->"), self)
        self.buttonNextRoot.setToolTip(_("Next location"))
        self.buttonNextRoot.setObjectName("buttonNextkRoot")
        button_layout.addWidget(self.buttonNextRoot)  
        
        self.buttonCollapseAll = QPushButton(_("-"), self)
        self.buttonCollapseAll.setObjectName("buttonCollapseAll")
        self.buttonCollapseAll.setToolTip(_("Collapse All"))
        button_layout.addWidget(self.buttonCollapseAll)
        
        button_layout.addStretch()
        mainlayout.addLayout(button_layout)
        self.tree = FSTree(self)
        
        mainlayout.addWidget(self.tree)
        self.setLayout(mainlayout)
        
    
    @pyqtSignature('')
    def on_actionUp_triggered(self):
        #QMessageBox.information(self, "UP", "Up")
        #self.get
        self.tree.goUp()
    
    @pyqtSignature('')
    def on_buttonCollapseAll_pressed(self):
        self.tree.collapseAll()
        self.buttonSyncTabFile.setEnabled(False)
    
    
    

class FSTree(QTreeView):
    def __init__(self, parent):
        QTreeView.__init__(self, parent)
        model = QDirModel(self)
        
        self.createMenus()        

        self.setModel(model)
        for i in range(1,model.columnCount()):
            self.setColumnHidden(i, True)
        self.setAnimated(False)
        self.setIndentation(20)
        self.setSortingEnabled(True)
        self.setExpandsOnDoubleClick(True)
        QMetaObject.connectSlotsByName(self)
    
    def createMenus(self):
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
        self.menuFile.addAction(self.actionCopyPathToClipBoard)
        
        self.actionRename = QAction(_("&Rename"), self)
        self.actionRename.setObjectName("actionRename")
        self.menuFile.addAction(self.actionRename)
        
        self.actionDelete = QAction(_("&Delete"), self)
        self.actionDelete.setObjectName("actionDelete")
        self.menuFile.addAction(self.actionDelete)
        
        self.actionFileOpen = QAction(_("&Open"), self)
        self.actionFileOpen.setObjectName("actionFileOpen")
        self.menuFile.addAction(self.actionFileOpen)
        
        self.actionRefresh = QAction(_("&Refresh"), self)
        self.actionRefresh.setObjectName("actionRefresh")
        self.menuFile.addAction(self.actionRefresh)
        
        self.actionProperties = QAction(_("&Properties"), self)
        self.actionProperties.setObjectName("actionProperties")
        #self.actionProperties.setShortcut("")
        self.menuFile.addAction(self.actionProperties)
        
        
        # Directory Menus
        self.menuNewFileSystemElement = QMenu(_("&New.."), self)
        self.menuNewFileSystemElement.setObjectName('menuNewFileSystemElement')
        self.actionFileNew = self.menuNewFileSystemElement.addAction('File')
        self.actionFileNew.setObjectName("actionFileNew")
        
        self.menuNewFileSystemElement.setObjectName('newFile')
        self.actionDirNew = self.menuNewFileSystemElement.addAction('Directory')
        self.actionDirNew.setObjectName("actionDirNew")
        
        
        self.menuDir.addMenu(self.menuNewFileSystemElement)
        self.menuDir.addAction(self.actionCopyPathToClipBoard)
        
        self.actionSetAsRoot = QAction(_("&Set as root"), self)
        self.actionSetAsRoot.setObjectName("actionSetAsRoot")
        self.menuDir.addAction(self.actionSetAsRoot)
        
        self.menuDir.addAction(self.actionRefresh)
        
        self.menuDir.addAction(self.actionRename)
        self.menuDir.addAction(self.actionDelete)
        
        self.menuDir.addAction(self.actionProperties)
        
        
        
        self.defaultMenu.addMenu(self.menuNewFileSystemElement)
        self.defaultMenu.addAction(self.actionRefresh)
        #self.defaultMenu.addAction()
        
        
        
            

        
        
        
        
    def mouseDoubleClickEvent(self, event):
        if event.button() != Qt.LeftButton:
            return
        QTreeView.mouseDoubleClickEvent(self, event)
        
        index = self.indexAt(event.pos())
        data = unicode(self.model().filePath(index))
        print data
        if os.path.isfile(data):
            mainwin = self.parent().parent().parent()
            mainwin.tabWidgetEditors.openLocalFile(data)
        if os.path.isdir(data):
            if self.model().hasChildren(index):
                print "Cerpeta"
                
    
    def goUp(self):
        current_top = unicode(self.model().filePath(self.rootIndex()))
        #self.tree.setRootIndex(self.tree.model().index(QDir.currentPath()))
        upper = abspath(join(current_top, '..'))
        
        if upper != current_top:
            self.setRootIndex(self.model().index(upper))
#        print self.model().data(index).toPyObject()
#        print self.model().data(index.parent()).toPyObject()
#        print "Root", self.model().filePath(self.rootIndex())
    
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

class FSPane(QDockWidget):
    def __init__(self, parent):
        QDockWidget.__init__(self, parent)
        self.setWindowTitle(_("File System Panel"))
        self.setWidget(FSPaneWidget(self))


