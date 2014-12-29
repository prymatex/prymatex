#!/usr/bin/env python
from __future__ import unicode_literals

from prymatex.qt import QtCore

class FindMixin(object):
    """docstring for FindMixin"""
    def __init__(self, **kwargs):
        super(FindMixin, self).__init__(**kwargs)

    def initialize(self, *args, **kwargs):
        self.widgetFind.setVisible(False)
        self.comboBoxFind.lineEdit().returnPressed.connect(self.on_lineEditFind_returnPressed)

    # ------- Signals
    def on_pushButtonFindFind_pressed(self):
        editor, cursor = self._find_context()
        flags = self.flags()
        cursor = cursor if flags & self.InSelection else None
        match = self.comboBoxFind.lineEdit().text()
        editor.findMatch(match, flags, cursor=cursor, findNext=True, cyclicFind=False)

    def on_pushButtonFindPrev_pressed(self):
        editor, cursor = self._find_context()
        flags = self.flags() | self.Backward
        cursor = cursor if flags & self.InSelection else None
        match = self.comboBoxFind.lineEdit().text()
        editor.findMatch(match, flags, cursor=cursor, findNext=False, cyclicFind=False)

    def on_pushButtonFindAll_pressed(self):
        editor, cursor = self._find_context()
        flags = self.flags()
        match = self.comboBoxFind.lineEdit().text()
        editor.findAll(match, flags)
        
    def on_lineEditFind_returnPressed(self):
        modifiers = self.application().keyboardModifiers()
        if modifiers & QtCore.Qt.ShiftModifier:
            self.on_pushButtonFindPrev_pressed()
        elif modifiers & QtCore.Qt.AltModifier:
            self.on_pushButtonFindAll_pressed()
        else:
            self.on_pushButtonFindFind_pressed()
         
    # ------- Go to quickFind
    def quickFind(self):
        editor, cursor = self._find_context(select=True)
        if cursor.hasSelection():
            editor.findMatch(cursor.selectedText(), self.defaultFlags(), 
                findNext=True, cursor=cursor)
            
    def quickFindAll(self):
        editor, cursor = self._find_context(select=True)
        if cursor.hasSelection():
            cursors = editor.findAll(cursor.selectedText(), self.defaultFlags())
            editor.setTextCursors(cursors)

    # ------- Go to incrementalFind
    def incrementalFind(self):
        self.hideAll()
        self.pushButtonFindFind.setVisible(False)
        self.pushButtonFindPrev.setVisible(False)
        self.pushButtonFindAll.setVisible(False)
        self.widgetFind.setVisible(True)

    # ------- Go to find
    def find(self):
        self.hideAll()
        editor = self.window().currentEditor() 
        cursor = editor.textCursor()
        if cursor.hasSelection():
            word = cursor.selectedText()
            self.comboBoxFind.lineEdit().setText(word)
        self.pushButtonFindFind.setVisible(True)
        self.pushButtonFindPrev.setVisible(True)
        self.pushButtonFindAll.setVisible(True)        
        self.widgetFind.setVisible(True)
        self.comboBoxFind.lineEdit().selectAll()
        self.comboBoxFind.lineEdit().setFocus()
