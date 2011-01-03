#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-*- encoding: utf-8 -*-
# Created: 02/02/2010 by defo

from PyQt4.QtGui import QTabWidget, QTextEdit, QMessageBox, QAction, QIcon
from PyQt4.QtCore import QString, SIGNAL, Qt
import itertools

from prymatex.gui.utils import *
from prymatex.gui.editor.widget import PMXEditorWidget


class PMXTabWidget(QTabWidget):
    
    #Signal
    currentEditorChange = pyqtSignal(PMXEditorWidget)

    counter = 1
    
    def __init__(self, parent):
        QTabWidget.__init__(self, parent)
        
        self.setupActions() # Call it at first so the QMetaObject.connectSlotsByName is called in the setupUi
        self.setupUi()

        if not self.count():
            self.appendEmptyTab()
        
        
        self.connect(self, SIGNAL("tabCloseRequested(int)"), self.closeTab)
        self.connect(self, SIGNAL("currentChanged(int)"), self.indexChanged)
        self.currentChanged.connect(self.on_current_changed)
        
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
    def on_actionCloseAll_triggered(self):
        QMessageBox.information(self, "", "Close All")
        
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


    
    def on_current_changed(self, index):
        '''
        TODO: Resync all menus
        '''
        self.currentEditorChange.emit(self.widget(index))
        
    def mouseDoubleClickEvent(self, mouse_event):
        '''
        Opens a new tab when double-clicking on the tab bar
        '''
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
    
    def on_syntax_change(self, syntax):
        editor = self.currentWidget()
        editor.set_syntax(syntax)

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
        for i in range(self.count):
            tab = self.widget(i)
            if isinstance(tab, PMXEditorWidget):
                l.append( tab ) # It's and editor
        return l

    def __len__(self):
        return self.count()
        
    def __getitem__(self, index):
        assert isinstance(index, int)
        if index < 0 or index > len(self):
            raise IndexError("%s-nth widget does not exist in %s" % (index, self) )
        return self.widget( index )

    
                
    def openLocalFile(self, path):
        '''
        Opens a file in a tab, tries to reuse an empty one if it's
        focused
        @param path: A local file path
        '''
        try:
            count = self.count()
            try:
                first_editor = self.editors[0]
            except IndexError:
                first_editor = None
            # Is there any tab opened?
            if path in self.openedFileMap():
                logger.info("%s is already opened", path)
                self.openedFileMap()[path].setFocus(Qt.MouseFocusReason)
                return
            
            elif count == 1 and first_editor and not first_editor.modified and not first_editor.path:
                first_editor.open(path)
                editor.getFocus()
                
            else:
                editor = self.getEditor(path)
                index = self.addTab(editor, self.trUtf8("Loading..."))
                self.setCurrentIndex(index)
        except UnicodeDecodeError, e:
            QMessageBox.critical(self, self.trUtf8("Could not decode file %s", path),
                                 self.trUtf8("""<p>File %s could not be decoded</p>
                                 <p>Some exception data:</p>
                                 <pre>%s</pre>""", path, unicode(e)[:40]))
    
    def openFile(self, path):
        '''
        Creates a tab with the file contents and returns it
        '''
        from prymatex.gui.editor.widget import PMXEditorWidget
        editor = PMXEditorWidget.getEditor(self, path)
        self.addTab(editor, '...')
        return editor
        
    
    def appendEmptyTab(self):
        '''
        Creates a new empty tab and returns it
        '''
        
        editor = PMXEditorWidget.getEditor(self)
        # Title should be filled after tab insertion
        self.addTab(editor, '...')
        return editor
    
    def addTab(self, widget, title, autoFocus = True):
        ''' Overrides QTabWidget.addTab(page, title) so that
        afterInsertion is called '''
        index = super(PMXTabWidget, self).addTab(widget, title)
        
        if autoFocus:
            self.setCurrentIndex(index)
            if self.count() == 1:
                widget.setFocus(Qt.MouseFocusReason)
                
        if hasattr(widget, 'afterInsertion'):
            widget.afterInsertion(self, index)
            
        return index
        
    
    
    def closeTab(self, index):
        '''
        Asks the editor to be closed
        '''
        editor = self.widget(index)
        count = self.count()
        if editor.requestClose():
            self.removeTab(index)
            return True
        return False
    
    def removeTab(self, index):
        '''
        Lets the widget know when it has been removed
        '''
        widget = self.widget(index)
        retval = QTabWidget.removeTab(self, index)
        if hasattr(widget, 'afterRemoveEvent' ):
            widget.afterRemoveEvent()
        return retval
    
    def tabRemoved(self, index):
        if not self.count():
            self.appendEmptyTab()
        # 
        widget = self.currentWidget()
        #if not widget.actionMenuTab.isChecked():
        #    widget.actionMenuTab.setChecked(True)
            
    def indexChanged(self, index):
        #if index >= 0:
        #    widget = self.widget(index)
        #    widget.actionMenuTab.setChecked(True)
        pass
    
    def tabInserted(self, index):
        '''
        Lets the widget know when it has been inserted
        '''
        widget = self.widget(index)
        if hasattr(widget, 'afterInsertionEvent' ):
            widget.afterInsertionEvent()
        if not self.count():
            widget.actionMenuTab.setChecked(True)

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
        if self.count() == 1:
            return
        count = self.count()
        index = self.currentIndex()
        text = self.tabText(index)
        widget = self.currentWidget()
        self.removeTab(index)
        index += 1
        if index >= count:
            index = 0
        self.insertTab(index, widget, text)
        self.setCurrentWidget(widget)




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
        
    
