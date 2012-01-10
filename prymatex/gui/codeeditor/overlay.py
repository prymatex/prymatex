#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from prymatex.core.plugin import PMXBaseOverlay
from prymatex.gui.overlays.message import PMXMessageOverlay

class PMXEditorMessageOverlay(PMXMessageOverlay):      
    def initialize(self, editor):
        PMXMessageOverlay.initialize(self, editor)
        editor.themeChanged.connect(self.on_editor_themeChanged)
    
    def on_editor_themeChanged(self):
        # Update Message Colors
        self.setMessageTextColor( self.parent().colours['background'])
        self.setMessageBackgroundColor( self.parent().colours['foreground'] )
        self.setMessageBorderColor(self.parent().colours['selection'])

class PMXMiniMapOverlay(QtGui.QWidget, PMXBaseOverlay):
    # Padding
    paddingLeft = 5
    # Padding
    paddingTop = 5
    
    def updateOverlay(self):
        pass
    
    def boundingRect(self):
        return QtCore.QRectF(0, 0, 100, 200)
    
    def updateOverlay(self):
        if hasattr(self.parent(), 'viewport'):
            parentRect = self.parent().viewport().rect()
        else:
            parentRect = self.parent().rect()

        if not parentRect:
            return

        x = parentRect.width() - 100 - self.paddingLeft
        y = self.paddingTop
        self.setGeometry(x, y, 100, 200)
    
    def paintEvent(self, event):
        QtGui.QWidget.paintEvent(self, event)
        painter = QtGui.QPainter(self)
        color = QtGui.QColor(self.parent().colours['foreground'])
        color.setAlpha(200)
        painter.setBrush(QtGui.QBrush(color))
        painter.drawRect(self.boundingRect())
        painter.end()
