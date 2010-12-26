#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-*- encoding: utf-8 -*-
# Created: 02/02/2010 by defo

from PyQt4.QtGui import QTabWidget, QTextEdit, QMessageBox, QAction, QIcon
from PyQt4.QtCore import QString, SIGNAL, Qt
from prymatex.gui.editor import PMXCodeEdit

from prymatex.lib.i18n import ugettext as _
from prymatex.gui.utils import *
import itertools

class PMXTabWidget(QTabWidget):
    
    #Signal
    currentEditorChange = pyqtSignal(PMXCodeEdit)

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
        self.buttonTabList.setToolTip(_("Tab list"))
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
        widget = self.widgetFromTabPos( pos )
        if not widget:
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
        else:
            widget
    
    def on_syntax_change(self, syntax):
        editor = self.currentWidget()
        editor.set_syntax(syntax)
        
    def openLocalFile(self, path):
        '''
        Abre un archivo en una tab
        '''
        try:
            count = self.count()
            # Primero hay que buscar si no está abierto
            if count:
                for i in range(self.count()):
                    editor = self.widget(i)
                    if path == editor.path:
                        self.setCurrentWidget(editor)
                        return tabWidgetEditors
            
            if count == 1 and not self.widget(0).document().isModified() and \
                not self.widget(0).path:
                #print "Reutilizando vacio"
                editor = self.widget(0)
                
                editor.path = path
                editor.afterInsertionEvent()
                editor.getFocus()
                
            else:
                editor = self.getEditor(path)
                index = self.addTab(editor, _("Loading..."))
                self.setCurrentIndex(index)
        except UnicodeDecodeError, e:
            QMessageBox.critical(self, _("Could not decode file %s", path), 
                                 _("""<p>File %s could not be decoded</p>
                                 <p>Some exception data:</p>
                                 <pre>%s</pre>""", path, unicode(e)[:40]))
    
    def appendEmptyTab(self):
        '''
        Creates a new empty tab and returns it
        '''
        from prymatex.gui.editor.widget import PMXEditorWidget
        editor =PMXEditorWidget.getEditor(self)
        # Title should be filled after tab insertion
        index = self.addTab(editor, editor.title)
        
        self.setCurrentIndex(index)
        if self.count() == 1:
            editor.setFocus(Qt.TabFocusReason)
        return editor
    
    
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
        if not widget.actionMenuTab.isChecked():
            widget.actionMenuTab.setChecked(True)
            
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

class PMWTabsMenu(QMenu):
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
        
    


    
        
        
        
