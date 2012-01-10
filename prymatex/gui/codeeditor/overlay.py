#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.gui.overlays.message import PMXMessageOverlay

class PMXEditorMessageOverlay(PMXMessageOverlay):      
    def __init__(self, editor):
        PMXMessageOverlay.__init__(self, editor)
        editor.themeChanged.connect(self.on_editor_themeChanged)
        
    def on_editor_themeChanged(self):
        # Update Message Colors
        self.setMessageTextColor( self.parent().colours['background'])
        self.setMessageBackgroundColor( self.parent().colours['foreground'] )
        self.setMessageBorderColor(self.parent().colours['selection'])
