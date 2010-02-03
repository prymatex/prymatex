#!/usr/bin/env python
#-*- encoding: utf-8 -*-
# Created: 02/02/2010 by defo

from PyQt4.QtGui import QTabWidget, QTextEdit, QMessageBox, QAction
from PyQt4.QtCore import QString, SIGNAL, Qt
from prymatex.gui.editor import PMXTextEdit

from prymatex.lib.i18n import ugettext as _


        

class PMXTabWidget(QTabWidget):
    EDIT_TAB_WIDGET = PMXTextEdit
    UNTITLED_LABEL = _("New File %s")
    
    counter = 1
    
    def untitled_label(self):
        counter = self.counter
        self.counter += 1
        return self.UNTITLED_LABEL % counter
    
    def __init__(self, parent):
        QTabWidget.__init__(self, parent)
        if not self.count():
            self.appendEmptyTab()
        self.setTabsClosable(True)
        self.setMovable(True)
        self.connect(self, SIGNAL("tabCloseRequested(int)"), self.closeTab)
        self.connect(self, SIGNAL("currentChanged(int)"), self.indexChanged)
        
        #self.setTab
    
    
    
    def mouseDoubleClickEvent(self, event):
        self.appendEmptyTab()
    
    
    def getEditor(self, *largs, **kwargs):
        '''
        Editor Factory
        '''
        return self.EDIT_TAB_WIDGET(self, *largs, **kwargs)
    
    def tabRemoved(self, index):
        if not self.count():
            self.appendEmptyTab()
    
    
    def openLocalFile(self, path):
        editor = self.getEditor(path)
        index = self.addTab(editor, _("Loading..."))
        self.setCurrentIndex(index)
        
    
    
    def appendEmptyTab(self):
        editor = self.getEditor()
        # Title should be filled after tab insertion
        index = self.addTab(editor, '')
        
        self.setCurrentIndex(index)
        if self.count() == 1:
            editor.setFocus(Qt.TabFocusReason)
    
    
    def closeTab(self, index):
        '''
        Asks the editor to be closed
        '''
        editor = self.widget(index)
        if editor.requestClose():
            self.removeTab(index)
    
    def addTab(self, widget, label):
        '''
        Lets the widget know when it has been inserted
        '''
        retval = QTabWidget.addTab(self, widget, label)
        if hasattr(widget, 'afterInsertionEvent' ):
            widget.afterInsertionEvent()
        if not self.count():
            widget.menu_action.setChecked(True)
        return retval
            
    def removeTab(self, index):
        '''
        Lets the widget know when it has been removed
        '''
        widget = self.widget(index)
        retval = QTabWidget.removeTab(self, index)
        if hasattr(widget, 'afterRemoveEvent' ):
            widget.afterRemoveEvent()
        return retval
    
    #def setCurrentIndex(self, index):
    #    QTabWidget.setCurrentIndex(self, index)
    #    self.currentWidget().menu_action.setChecked(True)
    
    def indexChanged(self, index):
        if index > 0:
            widget = self.widget(index)
            widget.menu_action.setChecked(True)
        