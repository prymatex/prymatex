#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-*- encoding: utf-8 -*-
# Created: 02/02/2010 by defo

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QTabWidget, QTextEdit, QMessageBox, QAction, QIcon
from PyQt4.QtCore import QString, SIGNAL, Qt
import itertools

from prymatex.gui.utils import *
from prymatex.gui.editor.editorwidget import PMXEditorWidget
from choosetab import ChooseTabDialog
from prymatex.core.base import PMXObject
import logging
from prymatex.core.exceptions import APIUsageError
from prymatex.core.filemanager import PMXFile
from prymatex.core.config import pmxConfigPorperty

logger = logging.getLogger(__name__)

ICON_FILE_STATUS_NORMAL = QIcon(qApp.instance().trUtf8(''
':/actions/resources/mimetypes/x-office-document.png'))
ICON_FILE_STATUS_MODIFIED = QIcon(qApp.instance().trUtf8(
':/actions/resources/actions/document-save-all.png'))

class PMXTabWidget(QTabWidget, PMXObject):
    '''
    TabWidget holds the editors.
    It overrides Qt's addTab() method, titles are put through
    callbacks
    '''
    
    class Meta:
        settings = 'TabWidget'
        
    # Settings
    TABBAR_NEVER_SHOWN = 0x00
    TABBAR_ALWAYS_SHOWN = 0x01
    TABBAR_WHEN_MULTIPLE = 0x02
    
    def setShowTabBar(self, value):
        values = [
                  self.TABBAR_NEVER_SHOWN,
                  self.TABBAR_ALWAYS_SHOWN,
                  self.TABBAR_WHEN_MULTIPLE,
                  ]
        if not value in values:
            raise APIUsageError("setShowTabBar expected a valid constant")
        self.showTabBarCheck() # Update
        
    showTabBar = pmxConfigPorperty(default = TABBAR_ALWAYS_SHOWN, fset=setShowTabBar)
     
    # Signals
    currentEditorChanged = QtCore.pyqtSignal(QWidget)
    
    def __init__(self, parent):
        super(PMXTabWidget, self).__init__(parent)
        
        self.setupActions() # Call it at first so the QMetaObject.connectSlotsByName is called in the setupUi
        self.setupUi()

        self.buttonTabList = QPushButton(self)
        self.buttonTabList.setObjectName("buttonTabList")
        self.buttonTabList.setToolTip(self.trUtf8("Tab list"))
        self.buttonTabList.setShortcut(text_to_KeySequence("Ctrl+Tab"))
        self.buttonTabList.setIcon(QIcon(":/actions/resources/actions/view-close.png"))
        self.buttonTabList.setStyleSheet('''
            QPushButton {
                padding: 5px;
            }
        ''')
        self.setCornerWidget(self.buttonTabList, Qt.TopRightCorner)
        self.chooseFileDlg = QDialog()
        self.connectSignals()
        self.configure()
    
    def connectSignals(self):
        #External events
        self.connect(self.mainWindow, SIGNAL('statusBarSytnaxChangedEvent'), self.updateEditorSyntax )
        
        #Internal signals
        self.connect(self, SIGNAL("tabCloseRequested(int)"), self.closeTab)
        self.connect(self, SIGNAL("currentChanged(int)"), self.indexChanged)
        

    def setupUi(self):
        self.setTabsClosable(True)
        self.setMovable(True)
        QMetaObject.connectSlotsByName(self)
        
    def setupActions(self):
        '''
        QAction setup. Some of these actions are used for the context menus
        '''
        self.actionNewTab = QAction(self.trUtf8("&New tab"), self)
        self.actionNewTab.setObjectName("actionNewTab")
        
        self.actionCloseAll = QAction(self.trUtf8("Close &All"), self)
        self.actionCloseAll.setObjectName("actionCloseAll")
        
        self.actionCloseOthers = QAction(self.trUtf8("Close &Others"), self)
        self.actionCloseOthers.setObjectName("actionCloseOthers")
        
        self.actionCloseTab = QAction(self.trUtf8("&Close"), self)
        self.actionCloseTab.setObjectName("actionCloseTab")

        self.actionOrderTabsByName = QAction(self.trUtf8("Order by &name"), self)
        self.actionOrderTabsByName.setObjectName("actionOrderTabsByName")
        
        self.actionOrderOpenOrder = QAction(self.trUtf8("Order by Open Order"), self)
        self.actionOrderOpenOrder.setObjectName("actionOrderOpenOrder")
        
        self.actionOrderByURL = QAction(self.trUtf8("Order by &URL"), self)
        self.actionOrderByURL.setObjectName("actionOrderByURL")

    @pyqtSignature("")
    def on_actionNewTab_triggered(self):
        self.appendEmptyTab()

    @pyqtSignature("")
    def on_actionCloseAll_triggered(self):
        for index in range(self.count()):
            if not self.closeTab(0):
                return

    @pyqtSignature("")
    def on_actionCloseTab_triggered(self):
        self.closeTab(self.currentIndex())

    @pyqtSignature("")
    def on_actionCloseOthers_triggered(self):
        current_index = self.currentIndex()
        for index in range(current_index):
            if not self.closeTab(0):
                return
        for index in range(1, self.count()):
            if not self.closeTab(1):
                return
    
    def mouseDoubleClickEvent(self, mouse_event):
        '''
        Opens a new tab when double-clicking on the tab bar
        '''
        super(PMXTabWidget, self).mouseDoubleClickEvent(mouse_event)
        tabbar = self.tabBar()
        
        
        if mouse_event.button() == Qt.LeftButton:
            self.appendEmptyTab()

    def widgetFromTabPos(self, point):
        '''
        Returns the widget at a point
        '''
        # http://lists.trolltech.com/qt-interest/2006-02/msg01471.html
        tabBar = self.tabBar()
        for index in range(self.count()):
            if tabBar.tabRect( index ).contains( point ):
                return self.widget( index )
    
    def contextMenuEvent(self, context_event):
        '''
        Event
        '''
        pos = context_event.pos()
        m = QMenu()
        m.addAction(self.actionNewTab)
        m.addSeparator()
        m.addAction(self.actionCloseTab)
        m.addAction(self.actionCloseAll)
        m.addAction(self.actionCloseOthers)
        m.addSeparator()
        m_order = m.addMenu(self.trUtf8("Tab &Order"))
        m_order.addAction(self.actionOrderTabsByName)
        m_order.addAction(self.actionOrderOpenOrder)
        m_order.addAction(self.actionOrderByURL)

        m.exec_( context_event.globalPos() )

        # Separate menus when clicking on a tab?
        # widget = self.widgetFromTabPos( pos )
        #if not widget:
        #
        #else:
        #    widget
    
    #----------------------------------------------------------------------------------
    # Widget acces and Python collection emulation
    #----------------------------------------------------------------------------------
    def openedFileMap(self):
        '''
        @returns: A path -> widget for every editor in the tab widget
        '''
        
        d = {}
        for editor in self.editors:
            if editor.path:
                d[unicode(editor.path)] = editor
        return d

    @property
    def editors(self):
        ''' List of PMXEditorWidget insances in the tab widget '''
        l = []
        for i in range(len(self)):
            tab = self.widget(i)
            if isinstance(tab, PMXEditorWidget):
                l.append( tab ) # It's and editor
        return l

    def __len__(self):
        return self.count()
        
    def __getitem__(self, index):
        if type(index) in (int, ):
            if index < 0 or index > len(self):
                raise IndexError("%s-nth widget does not exist in %s" % (index, self) )
            return self.widget( index )
        elif isinstance(index, PMXFile):
            for i in range(len(self)):
                tab = self.widget(i)
                if isinstance(tab, PMXEditorWidget):
                    if tab.file == index:
                        return tab
            raise KeyError("%s has no %s file" % (self, index))
        raise APIUsageError("%s only supports integer and PMXFile indexes" % (type(self).__name__))
        
    def __contains__(self, other):
        
        assert isinstance(other, PMXFile)
        for i in range(len(self)):
            tab = self.widget(i)
            if isinstance(tab, PMXEditorWidget):
                if tab.file == other:
                    return True
        return False
    
    def focusEditor(self, editor):
        
        for i in range(len(self)):
            tab = self.widget(i)
            if isinstance(tab, PMXEditorWidget):
                if tab == editor:
                    self.setCurrentIndex(i)
                    tab.setFocus(Qt.MouseFocusReason)
                    return
        raise APIUsageError("Could not foucs %s in %s" % (editor, self))
        
    def appendEmptyTab(self):
        '''
        Creates a new empty tab and returns it
        '''
        #print "** appendEmptyTab called!"
        #import traceback
        #traceback.print_stack()
        file_manager = qApp.instance().file_manager
        empty_file = file_manager.getEmptyFile()
        editor = PMXEditorWidget.editorFactory(empty_file, parent = self)
        # Title should be filled after tab insertion
        self.addTab(editor)
        return editor
    
    def addTab(self, widget, autoFocus = True):
        ''' 
        Overrides QTabWidget.addTab(page, title) so that
        afterInsertion is called 
        '''
        if len(self) == 1:
            editor = self[0]
            
            if editor.file.path is None and not editor.modified:
                self.removeTab(1)
                    
        if type(autoFocus) is not bool:
            # Detect old API calls
            raise APIUsageError("addTab received somethign wierd as autoFoucs %s (should be bool)" % autoFocus)
        
        widget.setParent(self)
        title = widget.file.filename
        #print "Adding %s with title %s" % (widget, title)
        index = super(PMXTabWidget, self).addTab(widget, '...')
        
        self.setTabIcon(index, ICON_FILE_STATUS_NORMAL)
        
        widget.fileTitleUpdate.connect(self.updateTabInfo)
        
        widget.fileTitleUpdate.connect(self.updateTabInfo)
        #self.connect(widget, SIGNAL('fileTitleUpdate()'), self.updateTabInfo)
        
        widget.fileStatusModified.connect(self.editorModified)
        widget.fileStatusSynced.connect(self.editorSynced)
        
        if autoFocus:
            self.setCurrentIndex(index)
            if self.count() == 1:
                widget.setFocus(Qt.MouseFocusReason)
    
        return index
    
    def updateTabInfo(self):
        editor = self.sender()
        editor_index = self.indexOf(editor)
        
        self.setTabText(editor_index, editor.file.filename)
        # Tooltip
        if editor.file.path:
            path = self.trUtf8("Not saved yet")
        else:
            path = editor.file.path
        if editor.codeEdit.syntax:
            syntax = editor.codeEdit.syntax.name
        else:
            syntax = "Not selected"
             
        self.setTabToolTip(editor_index, unicode(self.trUtf8(''
             'Path: %(path)s\n'
             'Syntax: %(syntax)s'
        '')).strip() % dict(path = path, syntax = syntax))
        
    def editorModified(self, editor):
        #print "Editor modified", editor
        self.setTabIcon(self.indexOf(editor), ICON_FILE_STATUS_MODIFIED)
            #self.setTabTextColor(self.COLOR_NORMAL)
    
    def editorSynced(self, editor):
        self.setTabIcon(self.indexOf(editor), ICON_FILE_STATUS_NORMAL)
        
    
    def updateEditorSyntax(self, source, syntax):
        editor_widget = self.currentWidget()
        editor_widget.codeEdit.setSyntax(syntax)
    
    def closeTab(self, index):
        '''
        Asks the editor to be closed
        '''
        editor = self.widget(index)
        if editor.request_close():
            self.removeTab(index)
            return True
        return False
    
    def removeTab(self, index):
        '''
        Lets the widget know when it has been removed
        '''
        widget = self.widget(index)
        retval = QTabWidget.removeTab(self, index)
        if hasattr(widget, 'afterRemoveCallback' ):
            widget.afterRemoveCallback()
        return retval
    
    def tabRemoved(self, index):
        if not self.count():
            self.appendEmptyTab()
        # 
        widget = self.currentWidget()
        #if not widget.actionMenuTab.isChecked():
        #    widget.actionMenuTab.setChecked(True)
            
    def indexChanged(self, index):
        editor = self.widget(index)
        if editor:
            self.currentEditorChanged.emit(editor)
        self.showTabBarCheck()
    
    def showTabBarCheck(self):
        ''' Updates PMXTabBar behavior '''
        tabBar = self.tabBar()
        if self.showTabBar == self.TABBAR_ALWAYS_SHOWN:
            if tabBar.isHidden():
                tabBar.show()
        elif self.showTabBar == self.TABBAR_NEVER_SHOWN:
            if not tabBar.isHidden():
                tabBar.hide()
        elif self.showTabBar == self.TABBAR_WHEN_MULTIPLE:
            count = self.count()
            if count > 1:
                self.tabBar().show()
            elif count == 1:
                self.tabBar().hide()
        
    
    def tabInserted(self, index):
        '''
        Lets the widget know when it has been inserted
        '''
        widget = self.widget(index)
        if hasattr(widget, 'afterInsertionCallback' ):
            widget.afterInsertionCallback() # Editor at least should update title
                                            # through updateTitle signal
            
    def focusNextTab(self):
        '''
        Focus next tab
        '''
        curr = self.currentIndex()
        count = self.count()

        if curr < count -1:
            prox = curr +1
        else:
            prox = 0
        self.setCurrentIndex(prox)
        self.currentWidget().setFocus( Qt.TabFocusReason )

    def focusPrevTab(self):
        curr = self.currentIndex()
        count = self.count()

        if curr > 0:
            prox = curr -1
        else:
            prox = count -1
        self.setCurrentIndex(prox)
        self.currentWidget().setFocus(Qt.TabFocusReason)



    def moveTabLeft(self):
        ''' Moves the current tab to the left '''
        if self.count() == 1:
            return
        count = self.count()
        index = self.currentIndex()
        text = self.tabText(index)
        widget = self.currentWidget()
        self.removeTab(index)
        index -= 1
        if index < 0:
            index = count
        self.insertTab(index, widget, text)
        self.setCurrentWidget(widget)

    def moveTabRight(self):
        '''
        Moves the current tab to the right
        '''
        tab_count = len(self)
        if tab_count == 1:
            return
        index = self.currentIndex()
        text = self.tabText(index)
        widget = self.currentWidget()
        self.removeTab(index)
        index += 1
        if index >= tab_count:
            index = 0
        self.insertTab(index, widget, text)
        self.setCurrentWidget(widget)

    @property
    def unsavedCounter(self):
        '''
        Returns the amount of unsaved documents
        '''
        counter = 0
        for w in self:
            if getattr(w, 'modified', False):
                counter += 1
        return counter
        # FIXME: Iterations returns none
        #return sum(map(lambda w: w.modified and 1 or 0, self))

class PMXTabWidgetIterator(object):
    ''' Iterates over the tab widget's widgets '''
    def __init__(self, tabwidget):
        self.count, self.current = tabwidget.count(), 0
        self.tabwidget = tabwidget
        
    def next(self):
        pass
        

class PMXTabsMenu(QMenu):
    '''
    A menu that keeps only one action active
    '''
    def __init__(self, caption, parent):
        QMenu.__init__(self, caption, parent)
        self.actionGroup = QActionGroup(self)
        self.shortcuts = []
        for i in range(1, 10):
            self.shortcuts.append(text_to_KeySequence("Alt+%d" % i))
    
    def addAction(self, action):
        QMenu.addAction(self, action)
        self.actionGroup.addAction(action)
        self.updateShortcuts()
        
    def removeAction(self, action):
        QMenu.removeAction(self, action)
        self.actionGroup.removeAction(action)
        self.updateShortcuts()
        
    def updateShortcuts(self):
        for action, shortcut in itertools.izip(self.actions(), self.shortcuts):
            action.setShortcut(shortcut)
        
    
