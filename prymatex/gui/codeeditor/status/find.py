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
        
    # ------- Go to find
    def find(self):
        self.hideAll()
        editor = self.window().currentEditor() 
        cursor = editor.textCursor() 
        if cursor.hasSelection():
            word = cursor.selectedText()
            self.comboBoxFind.lineEdit().setText(word)        
        self.widgetFind.setVisible(True)
        self.comboBoxFind.lineEdit().selectAll()
        self.comboBoxFind.lineEdit().setFocus()
