# -*- coding: utf-8 -*-
from PyQt4.QtCore import SIGNAL, Qt
from PyQt4.QtGui import QDockWidget
from prymatex.core.base import PMXObject


class PaneDockBase(QDockWidget, PMXObject):
    '''
    Pane base functions
    '''
    action = None
    
    def associateAction(self, action, text_show, text_hide):
        assert self.action is None
        assert action.isCheckable()
        
        self.action = action
        self.text_show, self.text_hide = text_show, text_hide
        self.connect(self.action, SIGNAL("toggled(bool)"), self.toggleDock)
          
    def showEvent(self, event):
        QDockWidget.showEvent(self, event)
        self.setFocus(Qt.MouseFocusReason)
        self.emitWidgetShown(True)
    
    def hideEvent(self, event):
        QDockWidget.hideEvent(self, event)
        self.emitWidgetShown(False)
        if self.action.isChecked():
            self.action.setChecked(False)
        self.debug("Closing")
        #print "hide"
        self.mainWindow.tabWidget.currentWidget().setFocus(Qt.MouseFocusReason)
        
    def emitWidgetShown(self, val):
        self.emit(SIGNAL('widgetShown(bool)'), val)

    def toggleDock(self, check):
        if check:
            if self.isHidden():
                self.show()
            self.action.setText(self.text_hide)
        else:
            if not self.isHidden():
                self.hide()
            self.action.setText(self.text_show)
    
    
        