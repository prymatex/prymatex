# encoding: utf-8
'''
This module contains the main window status bar definition and widgets.
Some of the widgets defined here are:
    * The line counter
    * Syntax selector
    * 
'''
from prymatex.qt import QtCore, QtGui
from prymatex.utils.i18n import ugettext as _
            
class PMXStatusBar(QtGui.QStatusBar):
    def __init__(self, mainWindow):
        QtGui.QStatusBar.__init__(self, mainWindow)
        mainWindow.currentEditorChanged.connect(self.on_currentEditorChanged)
        self.statusBars = []
        self.activeBars = []

    def addPermanentWidget(self, widget):
        self.statusBars.append(widget)
        QtGui.QStatusBar.addPermanentWidget(self, widget, 1)
    
    def on_currentEditorChanged(self, editor):
        self.activeBars = []
        if editor is None:
            #Propagate and hide
            list(map(lambda bar: bar.setCurrentEditor(editor), self.activeBars))
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
