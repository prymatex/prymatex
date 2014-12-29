#!/usr/bin/env python
from __future__ import unicode_literals

from prymatex.qt import QtCore

class ReplaceMixin(object):
    """docstring for ReplaceMixin"""
    def __init__(self, **kwargs):
        super(ReplaceMixin, self).__init__(**kwargs)

    def initialize(self, *args, **kwargs):
        self.widgetReplace.setVisible(False)
        self.comboBoxReplaceWhat.lineEdit().returnPressed.connect(self.on_lineEditWhat_returnPressed)
        
    # ------- Signals
    def on_pushButtonReplaceFind_pressed(self, backward=False):
        editor, cursor = self._find_context()
        flags = self.flags()
        if backward:
            flags |= self.Backward
        cursor = cursor if flags & self.InSelection else None
        cyclic = bool(flags & self.Wrap)
        match = self.comboBoxFind.lineEdit().text()
        editor.findMatch(match, flags, cursor=cursor, cyclic=cyclic)
        
    def on_pushButtonReplaceFindAll_pressed(self):
        editor, cursor = self._find_context()
        flags = self.flags()
        match = self.comboBoxFind.lineEdit().text()
        editor.findAll(match, flags)

    def on_lineEditWhat_returnPressed(self):
        modifiers = self.application().keyboardModifiers()
        if modifiers & QtCore.Qt.ShiftModifier:
            self.on_pushButtonReplaceFind_pressed(True)
        elif modifiers & QtCore.Qt.AltModifier:
            self.on_pushButtonReplaceFindAll_pressed()
        else:
            self.on_pushButtonReplaceFind_pressed()
            
    # ------- Go to replace
    def replace(self):
        self.hideAll()
        self.widgetReplace.setVisible(True)
