#!/usr/bin/env python

class CodeEditorCommandsMixin(object):
    def command_insert(self, characters):
        self.textCursor().insertText(characters)
        