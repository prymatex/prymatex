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
        editor, cursor, *cursors = self._find_context()
        flags = self.flags()
        if backward:
            flags |= self.Backward
        cursor = cursor if flags & self.InSelection else None
        cyclic = bool(flags & self.Wrap)
        match = self.comboBoxReplaceWhat.lineEdit().text()
        editor.findMatch(match, flags, cursor=cursor, cyclic=cyclic)
        
    def on_pushButtonReplaceFindAll_pressed(self):
        editor, cursor, *cursors = self._find_context()
        flags = self.flags()
        match = self.comboBoxReplaceWhat.lineEdit().text()
        editor.findAll(match, flags)

    def on_lineEditWhat_returnPressed(self):
        modifiers = self.application().keyboardModifiers()
        if modifiers & QtCore.Qt.ShiftModifier:
            self.on_pushButtonReplaceFind_pressed(True)
        elif modifiers & QtCore.Qt.AltModifier:
            self.on_pushButtonReplaceFindAll_pressed()
        else:
            self.on_pushButtonReplaceFind_pressed()
            
    # ------- Show replace
    def replace(self):
        self.hideAll()
        editor, cursor, *cursors = self._find_context()
        if cursor.hasSelection():
            word = cursor.selectedText()
            self.comboBoxReplaceWhat.lineEdit().setText(word)
        self.widgetReplace.setVisible(True)
        self.comboBoxReplaceWhat.lineEdit().selectAll()
        self.comboBoxReplaceWhat.lineEdit().setFocus()

    def _replace(self, all_text=False):
        editor, cursor, *cursors = self._find_context()
        flags = self.flags()
        match = self.comboBoxReplaceWhat.lineEdit().text()
        replace = self.comboBoxReplaceWith.lineEdit().text()
        if match and replace:
            editor.replaceMatch(match, replace, flags, all_text=all_text)
            
    on_pushButtonReplaceReplace_pressed = _replace
    on_pushButtonReplaceReplaceAll_pressed = lambda self: self._replace(all_text=True)
