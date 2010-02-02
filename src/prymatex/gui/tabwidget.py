#!/usr/bin/env python
#-*- encoding: utf-8 -*-
# Created: 02/02/2010 by defo

from PyQt4.QtGui import QTabWidget, QTextEdit, QMessageBox
from PyQt4.QtCore import QString, SIGNAL, Qt


from prymatex.lib.i18n import ugettext as _
import os

class PMXTextEdit(QTextEdit):
    _path = ''
    
    def __init__(self, parent, path = ''):
        QTextEdit.__init__(self, parent)
        print self.connect(self, SIGNAL("destroyed(QObject)"), self.cleanUp)
        
        self.path = path
        if os.path.exists(self.path):
            try:
                f = open(self.path)
                text = f.read()
                f.close()
                self.setPlainText(text)
            except Exception, e:
                QMessageBox.critical(self, _("Read Error"), _("Could not read %s<br/>") % self.path)
        
    
    def path(): #@NoSelf
        def fget(self):
            return self._path
        def fset(self, value):
            self._path = unicode(value)
        doc = u"Path property QString->unicode/str"
        return locals()
    path = property(**path())
    
    def cleanUp(self):
        print "HOLA"
        
    def destroy(self, destroyWindow, destroySubWindows):
        print "Chau"
    
#    @property
#    def index(self):
#        tabwidget = self.parent()
#        for index in range(tabwidget.count()):
#            widget = tabwidget.widget(index)
#            print widget, self
#            if widget == self:
#                return index
#        return -1
    @property
    def filename(self):
        if self.path:
            return self.path
        return _("This unsaved file")
    
    def setTitle(self, text):
        tabwidget = self.parent().parent()
        #print tabwidget, tabwidget.parent()
        index = tabwidget.indexOf(self)
        tabwidget.setTabText(index, text)
    
    def updateTitle(self):
        
        self.setTitle(os.path.basename(self.path))
    
    def requestClose(self):
        if self.document().isModified():
            resp = QMessageBox.question(self, _("File modified"), _("%s is modified", self.filename), 
                                 QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            return resp
        else:
            return True
        

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
        editor.updateTitle()
    
    
    def appendEmptyTab(self):
        editor = self.getEditor()
        index = self.addTab(editor, self.untitled_label())
        self.setCurrentIndex(index)
        if self.count() == 1:
            editor.setFocus(Qt.TabFocusReason)
    
    
    def closeTab(self, index):
        editor = self.widget(index)
        print editor
        if editor.requestClose():
            self.removeTab(index)