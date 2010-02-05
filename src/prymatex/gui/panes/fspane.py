from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os
from os.path import abspath, join
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
    
    
        

class FSPaneWidget(QWidget):
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
        
        #button_layout.addWidget(createButton(self, _("&Up")))
        #button_layout.addWidget(createButton(self, _("&Filter")))
        #button_layout.addWidget(createButton(self, _("&Set Root")))
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
    
    
    

class FSTree(QTreeView):
    def __init__(self, parent):
        QTreeView.__init__(self, parent)
        model = QDirModel(self)
#        for i in range(model.columnCount()):
#            val = model.headerData(i, Qt.Horizontal)
#            print val.toPyObject()
        
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
        self.fileMenu = QMenu(self)
        self.fileMenu.setObjectName('menuFile')
        addActionsToMenu(self.fileMenu,
                        (_("Copy Path To Clipboard"),),
                        (_("Rename"), ),
                        (_("Delete"), ),
                        (_("Open"),),
                        (_("Open Width"),),
                        None,
                        (_("Properties"),), 
        )
        
        
        # Directory Menus
        self.dirMenu = QMenu(self)
        self.dirMenu.setObjectName('menuDir')
        addActionsToMenu(self.dirMenu,
                        self.actionCopyPathToClipboard,
                        (_("Set As Root"),),
                        (_("Rename"),),
                        (_("Delete"),),
                        None,
                        (_("Properties"),),
                                         
        )
        
        
        
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
                self.fileMenu.popup(event.globalPos())
            elif os.path.isdir(data):
                self.dirMenu.popup(event.globalPos())
    

    @property
    def current_selected_path(self):
        pass
    
    def on_actionCopyPathToClipboard_triggered(self):
        index_list = self.selectedIndexes()
        if len(index_list) == 1:
            index = index_list[0]
            #QClipboard.setText(self.model().data(index))
            qApp.instance().clipboard().setText(self.model().filePath(index))
            
class FSPane(QDockWidget):
    def __init__(self, parent):
        QDockWidget.__init__(self, parent)
        self.setWindowTitle(_("File System Panel"))
        self.setWidget(FSPaneWidget(self))
        
        