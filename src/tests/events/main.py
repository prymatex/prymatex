#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore

class MyMousePressEvent(QtCore.QEvent):
    TYPE = QtCore.QEvent.registerEventType()
    def __init__(self, sender):
        super(QtCore.QEvent, self).__init__(self.TYPE)
        self.sender = sender

class MyPushButton(QtGui.QPushButton):
    def __init__(self, text, parent):
        super(QtGui.QPushButton, self).__init__(text, parent)
    
    def mousePressEvent(self, event):
        QtGui.QApplication.postEvent(self, MyMousePressEvent(self))
    
class Example(QtGui.QMainWindow):
  
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()
        self.connect(self, QtCore.SIGNAL("MyMousePressEvent"), self.on_MyMousePressEvent)
        
    def initUI(self):
      
        button1 = MyPushButton("Button 1", self)
        button1.move(30, 50)

        button2 = MyPushButton("Button 2", self)
        button2.move(150, 50)
      
        self.statusBar().showMessage('Ready')
        self.setWindowTitle('Event sender')
        self.resize(290, 150)

    def customEvent(self, event):
        self.emit(QtCore.SIGNAL(event.__class__.__name__), event.sender)
        event.accept()
        return True
        
    def on_MyMousePressEvent(self, sender):
        self.statusBar().showMessage(sender.text() + ' was pressed')

class MyApp(QtGui.QApplication):
    def notify(self, receiver, event):
        if event.type() > QtCore.QEvent.User:
            w = receiver
            while(w):
                res = w.customEvent(event);
                if res and event.isAccepted():
                    return res
                w = w.parent()
        return super(MyApp, self).notify(receiver, event)

if __name__ == "__main__":
    app = MyApp(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
