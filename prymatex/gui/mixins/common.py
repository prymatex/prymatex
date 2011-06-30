#!/usr/bin/env python
#-*- encoding: utf-8 -*-
# Created: 05/02/2010 by defo
from PyQt4.Qt import qApp, QAction
from PyQt4.QtCore import QObject, SIGNAL

class CenterWidget(object):
    
    def center(self):
        dsk_geo = qApp.instance().desktop().availableGeometry()
        dwidth, dheight = dsk_geo.width(), dsk_geo.height() 
        width = dwidth * 0.7
        height = dheight * 0.67
        x0 = (dwidth - width) / 2 
        y0 = (dheight - height) / 2
        self.setGeometry(x0,y0,width,height)
    
class ShownByQAction(object):
    '''
    Some widgets have to be connected to an action
    so when the action is checked, they are show, and 
    when it's unchecked they hide.
    '''
    __action = None
    
    @property
    def action(self):
        return self.__action
    
    @action.setter
    def action(self, action):
        # Type check
        assert isinstance(action, QAction)
        assert action.isCheckable(), "QAction should be checkable to be bound"\
                                     " to a widget"
        assert self.action is None, "An action has already been defined for"\
                                    " this widget"
        self.__action = action
        self.make_connections(action)
        
        
    def handleShow(self, checked):
        if checked:
            if self.isHidden():
                self.show()
        else:
            if self.isVisible():
                self.hide()
    
    
    def make_connections(self, action):
        QObject.connect(self.action, SIGNAL('triggered(bool)'), self.handleShow)
    
    def hideEvent(self, event):
        self.action.setChecked(False)
        
if __name__ == "__main__":
    from PyQt4.QtGui import QApplication, QLabel, QMainWindow, QMenuBar, QWidget
    from PyQt4.QtGui import QVBoxLayout
    import sys
    
    app = QApplication(sys.argv)
    window = QMainWindow()
    
    class TestWidget(QWidget, ShownByQAction):
        def __init__(self, parent = None):
            super(TestWidget, self).__init__(parent)
            layout = QVBoxLayout()
            layout.addWidget(QLabel("This widget is bound to a %s action" % \
                             str(self.action)))
            self.setLayout(layout)
            
            
    window.setMenuBar(QMenuBar())
    window.setCentralWidget(QLabel("<h1>ShownByQAction test</h1>"
                                   "<p>Tests the binding between a widget"
                                   "and a QAction</p>"))
    menu = window.menuBar().addMenu("Test")
    action = QAction("Show", window)
    action.setCheckable(True)
    test_widget = TestWidget()
    test_widget.action = action
    menu.addAction(action)
    window.show()
    sys.exit(app.exec_())
    
    
