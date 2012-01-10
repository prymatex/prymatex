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

class PMXMiniMapOverlay(QtGui.QPlainTextEdit, PMXBaseOverlay):
    # Padding
    paddingLeft = 5
    # Padding
    paddingTop = 5
    
    def __init__(self, parent):
        QtGui.QPlainTextEdit.__init__(self, parent)
        font = self.document().defaultFont()
        font.setPixelSize(1)
        self.document().setDefaultFont(font)
        self.setReadOnly(True)
        
    def initialize(self, editor):
        PMXBaseOverlay.initialize(self, editor)
        editor.textChanged.connect(self.updateDocumentText)
        
    def updateDocumentText(self):
        text = self.parent().toPlainText()
        self.setPlainText(text)
        
    def updateOverlay(self):
        parentRect = self.parent().viewport().rect()
        
        x = self.parent().lineNumberAreaWidth() + parentRect.width() - 100 - self.paddingLeft
        y = self.paddingTop
        self.setGeometry(x, y, 100, 200)
    
    def paintEvent(self, event):
        QtGui.QPlainTextEdit.paintEvent(self, event)
