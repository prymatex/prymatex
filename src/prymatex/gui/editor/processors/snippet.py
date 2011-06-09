#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.support.processor import PMXSnippetProcessor

class PMXSnippetProcessor(PMXSnippetProcessor):
    def __init__(self, editor):
        super(PMXSnippetProcessor, self).__init__()
        self.editor = editor
        self.snippet = None
        self.tabreplacement = "\t"
        self.indentation = ""

    @property
    def hasSnippet(self):
        return self.snippet is not None
    
    def startSnippet(self, snippet):
        self.snippet = snippet
        #Remove Trigger
        cursor = self.editor.textCursor()
        for _ in range(len(snippet.tabTrigger)):
            cursor.deletePreviousChar()

    def beforeInsertText():
        cursor = self.editor.textCursor()
        if cursor.hasSelection():
            self.starts = cursor.selectionStart()
        else:
            self.starts = cursor.position()
            
    def selectHolder(self, holder):
        index = holder.position()
        cursor = self.editor.textCursor()
        cursor.setPosition(index)
        cursor.setPosition(index + len(holder), QTextCursor.KeepAnchor)
        self.editor.setTextCursor(cursor)

    def insertText(self, text):
        self.editor.textCursor().insertText(text)
    
    def afterInsertText():
        self.ends = self.editor.textCursor().position()

    def endSnippet(self):
        self.editor.textCursor().setPosition(self.ends)
        self.snippet = None