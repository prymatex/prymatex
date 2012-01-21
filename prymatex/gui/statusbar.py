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
        self.statusBars = []
        self.activeBars = []
        self.customActions = {}
        
    def addPermanentWidget(self, widget):
        self.statusBars.append(widget)
        QtGui.QStatusBar.addPermanentWidget(self, widget, 1)
    
    def setCurrentEditor(self, editor):
        self.activeBars = []
        for bar in self.statusBars:
            if bar.acceptEditor(editor):
                self.activeBars.append(bar)
                bar.setVisible(True)
        map(lambda bar: bar.setCurrentEditor(editor), self.activeBars)
        if editor is None:
            self.hide()
        else:
            self.show()
    
    def actionDispatcher(self, checked, action):
        print action, checked
    
    def registerStatusClassActions(self, statusClass, actions):
        for action in actions:
            if hasattr(action, 'callback'):
                receiver = lambda checked, action = action: self.actionDispatcher(checked, action)
                self.connect(action, QtCore.SIGNAL('triggered(bool)'), receiver)
        self.customActions[statusClass] = actions