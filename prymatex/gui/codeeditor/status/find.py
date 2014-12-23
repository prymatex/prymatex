#!/usr/bin/env python
from __future__ import unicode_literals

class FindMixin(object):
    """docstring for FindMixin"""
    def __init__(self, **kwargs):
        super(FindMixin, self).__init__(**kwargs)

    def initialize(self, *args, **kwargs):
        self.widgetFind.setVisible(False)
        self.comboBoxFind.lineEdit().textEdited.connect(self.on_lineEditFind_textEdited)

    # ------- Signals
    def on_lineEditFind_textEdited(self, text):
        print(text)
         
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
