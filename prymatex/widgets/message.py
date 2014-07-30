#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections

from prymatex.qt import QtCore, QtGui

class ToolTipLabel(QtGui.QLabel):
    
    margin = 10
    
    def __init__(self, parent):
        QtGui.QLabel.__init__(self, parent)
        
        self.linkActivated.connect(self.linkHandler)
        
        self.goe = QtGui.QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.goe)

        self.timeoutTimer = QtCore.QTimer(self)
        self.timeoutTimer.setSingleShot(True)
        
        self.animationIn = QtCore.QPropertyAnimation(self.goe, "opacity")
        self.animationIn.setDuration(300)
        self.animationIn.setStartValue(0)
        self.animationIn.setEndValue(1.0)
        self.animationIn.finished.connect(self.timeoutTimer.start)

        self.animationOut = QtCore.QPropertyAnimation(self.goe, "opacity")
        self.animationOut.setDuration(300)
        self.animationOut.setStartValue(1.0)
        self.animationOut.setEndValue(0)
        self.animationOut.finished.connect(self.hide)

        self.timeoutTimer.timeout.connect(self.animationOut.start)
        self.hide()
        
    def showMessage(self, message, frmt="text", timeout=2000, icon=None,
        point=None, links={}):
        if frmt == "text" and links:
            message = "<pre>%s</pre>" % message
        if links:
            message += "<hr><div style='text-align: right; font-size: small;'>"
            for key in links.keys():
                message += "<a href='%s'>%s</a>" % (key, key.title())
            message += "</div>"
        
        self.setText(message)
        self.adjustSize()
        self.updatePosition(point)
        self.links = links
        self.timeoutTimer.setInterval(timeout)
        self.show()
        self.animationIn.start()

    def linkHandler(self, link):
        callback = self.links.get(link, None)
        if isinstance(callback, collections.Callable):
            callback()
  
    def updatePosition(self, point = None):
        if point is not None:
            x, y = point.x(), point.y()
        else:
            rect = self.parent().geometry()
            x = rect.width() - self.width() - self.margin
            y = rect.height() - self.height() - self.margin

        self.setGeometry(x, y, self.width(), self.height())

    def enterEvent(self, event):
        if self.timeoutTimer.isActive():
            self.timeoutTimer.stop()
    
    def leaveEvent(self, event):
        self.timeoutTimer.start()
