#!/usr/bin/env python
#-*- encoding: utf-8 -*-
# Created: 03/02/2010 by defo

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from prymatex.lib.i18n import ugettext as _
import os

class PMXTextEdit(QTextEdit):
    _path = ''
    
    def __init__(self, parent, path = ''):
        QTextEdit.__init__(self, parent)
        #print self.connect(self, SIGNAL("destroyed(QObject)"), self.cleanUp)
        
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
    
    def setToolTip(self, text):
        tabwidget = self.parent().parent()
        index = tabwidget.indexOf(self)
        tabwidget.setTabToolTip(index, text)
        
    def title(self):
        tabwidget = self.parent().parent()
        #print tabwidget, tabwidget.parent()
        index = tabwidget.indexOf(self)
        return tabwidget.tabText(index)
        
        
    def setTitle(self, text):
        tabwidget = self.parent().parent()
        #print tabwidget, tabwidget.parent()
        index = tabwidget.indexOf(self)
        tabwidget.setTabText(index, text)
    
    def updateTab(self):
        '''
        Updates tab info
        '''
        if self.path:
            self.setTitle(os.path.basename(self.path))
            self.setToolTip(self.path)
        else:
            self.setTitle(_("Unsaved File"))
            self.setToolTip(_("Unsaved File"))
        
    def requestClose(self):
        if self.document().isModified():
            resp = QMessageBox.question(self, _("File modified"), _("%s is modified", self.filename), 
                                 QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            return resp
        else:
            return True
    
    def afterRemoveEvent(self):
        print 'afterRemoveEvent', self
        mainwin = self.parent().parent().parent()
        menu = mainwin.window_menu
        menu.windowActionGroup.removeAction(self.menu_action)
        
    def afterInsertionEvent(self):
        #print 'afterRemoveEvent', self
        self.updateTab()
        mainwin = self.parent().parent().parent()
        menu = mainwin.window_menu
        self.menu_action = QAction(self)
        self.connect(self.menu_action, SIGNAL("toggled(bool)"), self.showTab)
        self.menu_action.setText(self.title())
        self.menu_action.setCheckable(True)
        menu.windowActionGroup.addAction(self.menu_action)
        
    def showTab(self, checked):
        if checked:
            tw = self.parent().parent()
            index = tw.indexOf(self)
            if index != tw.currentIndex():
                tw.setCurrentIndex(index)