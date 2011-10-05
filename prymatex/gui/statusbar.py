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
            
#TODO: Preparar la statusbar para que pueda mandar los eventos correctamente a cada widget
# por ahora solo administra el widget status de PMXCodeEditor
class PMXStatusBar(QtGui.QStatusBar):
    def __init__(self, parent):
        QtGui.QStatusBar.__init__(self, parent)
        self.widgets = []
        
    def __getattr__(self, name):
        #TODO: en funcion del current editor retornar el metodo del widget correspondiente
        return getattr(self.widgets[0], name)
    
    def addPermanentWidget(self, widget):
        self.widgets.append(widget)
        QtGui.QStatusBar.addPermanentWidget(self, widget, 1)
    
    def setCurrentEditor(self, editor):
        if editor is not None:
            self.widgets[0].setCurrentEditor(editor)
            self.show()
        else:
            self.hide()