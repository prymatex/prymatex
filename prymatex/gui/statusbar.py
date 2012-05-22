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
        if editor is None:
            #Propagate and hide
            map(lambda bar: bar.setCurrentEditor(editor), self.activeBars)
            self.hide()
        else:
            for bar in self.statusBars:
                if bar.acceptEditor(editor):
                    self.activeBars.append(bar)
                    bar.setCurrentEditor(editor)
                    bar.setVisible(True)
                else:
                    bar.setVisible(False)
            self.show()
        self.updateMenuForStatusBar()
    
    def updateMenuForStatusBar(self):
        activeClasses = map(lambda bar: bar.__class__, self.activeBars)
        
        for statusClass, actions in self.customActions.iteritems():
            for action in actions:
                action.setVisible(statusClass in activeClasses)
                if action.isCheckable() and hasattr(action, 'testChecked'):
                    action.setChecked(action.testChecked(self.activeBars[activeClasses.index(statusClass)]))
    
    def actionDispatcher(self, checked, action):
        #Find class for action
        statusClasses = filter(lambda (cls, actions): action in actions, self.customActions.items())
        assert len(statusClasses) == 1, "More than one status class for action %s" % action
        statusClass = statusClasses[0][0]
        #Find instance
        statusInstance = filter(lambda status: status.__class__ == statusClass, self.statusBars)
        assert len(statusInstance) == 1, "More than one instance for class %s" % statusClass
        statusInstance = statusInstance[0]
        
        callbackArgs = [ statusInstance ]
        if action.isCheckable():
            callbackArgs.append(checked)
        action.callback(*callbackArgs)
    
    def registerStatusClassActions(self, statusClass, actions):
        for action in actions:
            if hasattr(action, 'callback'):
                receiver = lambda checked, action = action: self.actionDispatcher(checked, action)
                self.connect(action, QtCore.SIGNAL('triggered(bool)'), receiver)
        self.customActions[statusClass] = actions