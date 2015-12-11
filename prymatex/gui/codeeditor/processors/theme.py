#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui
from .base import CodeEditorBaseProcessor

from prymatex.support.processor import ThemeProcessorMixin

class CodeEditorThemeProcessor(CodeEditorBaseProcessor, ThemeProcessorMixin):
    def managed(self):
        return True

    def beginExecution(self, bundleItem):
        if self.bundleItem is not None and self.bundleItem == bundleItem:
            return

        self.editor.syntaxHighlighter.stop()

        super().beginExecution(bundleItem)
        
        char_format = self.editor.application().supportManager.getThemeTextCharFormat(bundleItem)
        palette = self.editor.application().supportManager.getThemePalette(bundleItem)

        self.editor.setCurrentCharFormat(char_format)
        self.editor.setPalette(palette)
        self.editor.syntaxHighlighter.start()
        self.editor.syntaxHighlighter.rehighlight()
        self.editor.themeChanged.emit(bundleItem)

    def endExecution(self, bundleItem):
        CodeEditorBaseProcessor.endExecution(self, bundleItem)

    def textCharFormat(self, scope):
        if self.isReady():
            return self.editor.application().supportManager.getThemeTextCharFormat(self.bundleItem, scope)
        else:
            return QtGui.QTextCharFormat()

    def textCharFormats(self, user_data):
        formats = []
        for token in user_data.tokens:
            frange = QtGui.QTextLayout.FormatRange()
            frange.start = token.start
            frange.length = token.end - token.start
            frange.format = self.textCharFormat(token.scope)
            formats.append(frange)
        return formats
