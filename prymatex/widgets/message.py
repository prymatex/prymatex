#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from PyQt4 import QtCore, QtGui

class PopupMessageWidget(QtGui.QLabel):
    ''' 
    Inner message QLabel.
    StyleSheet
    '''

    STYLESHEET = '''
    QLabel, QLabel link {
        color: rgb(0, 0, 0);
        background-color: rgb(248, 240, 200);
        border: 1px solid;
        border-color: rgb(173, 114, 47);
        border-radius: 5px;
        padding: 2px;
    }
    '''

    # Padding
    paddingLeft = 10
    # Padding
    paddingBottom = 10
    
    def __init__(self, parent):
        '''
        This label is managed from PMXMessageOverlay mixin, should not be
        used outside this module
        '''
        QtGui.QLabel.__init__(self, parent)
        
        self.setStyleSheet(self.STYLESHEET)
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
        
    def showMessage(self, message, timeout = 2000, icon = None, point = None, hrefCallbacks = {} ):
        '''
        @param message: Text message, can be HTML
        @param timeout: Timeout before message fades
        @param icon: A QIcon instance to show
        @param pos: An x, y tuple with message position
        @param link_map: 
        '''
        self.setText(message)
        self.updatePosition(point)
        self.adjustSize()
        self.linkMap = hrefCallbacks
        self.timeoutTimer.setInterval(timeout)
        self.show()
        self.animationIn.start()

    def linkHandler(self, link):
        callback = self.linkMap.get(link, None)
        if callback is None:
            self.logger.warn("No callback for %s" % link)
            return
        if not callable(callback):
            self.logger.warn("Callback for %s is not callable: %s" % (link, callback))
            return
        
        self.logger.debug( "Running callback: %s %s" % (link, callback))
        callback()
  
    def updatePosition(self, point = None):
        if point is not None:
            x, y = point.x(), point.y()
        else:
            rect = self.parent().geometry()
            x = rect.width() - self.width() - self.paddingLeft
            y = rect.height() - self.height() - self.paddingBottom

        self.setGeometry(x, y, self.width(), self.height())

    def enterEvent(self, event):
        if self.timeoutTimer.isActive():
            self.timeoutTimer.stop()
    
    def leaveEvent(self, event):
        self.timeoutTimer.start()
