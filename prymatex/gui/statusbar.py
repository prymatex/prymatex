# encoding: utf-8
'''
This module contains the main window status bar definition and widgets.
Some of the widgets defined here are:
    * The line counter
    * Syntax selector
    * 
'''
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL
from prymatex.utils.i18n import ugettext as _
from prymatex import resources
            
class PMXStatusBar(QtGui.QStatusBar):
    def __init__(self, parent):
        QtGui.QStatusBar.__init__(self, parent)
        self.widgets = []
        
    def addPermanentWidget(self, widget):
        self.widgets.append(widget)
        QtGui.QStatusBar.addPermanentWidget(self, widget, 1)
    
    def setCurrentEditor(self, editor):
        for widget in self.widgets:
            widget.setEditor(editor)