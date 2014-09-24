#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui
from .base import CodeEditorBaseProcessor

from prymatex.support.processor import ThemeProcessorMixin

class CodeEditorThemeProcessor(CodeEditorBaseProcessor, ThemeProcessorMixin):
    def managed(self):
        return True

    def beginExecution(self, bundleItem):
        if self.bundleItem == bundleItem:
            return

        self.editor.syntaxHighlighter.stop()
        # Get Wrapped Theme
        theme = self.editor.application().supportManager.getBundleItem(bundleItem.uuid)

        # ------------ Previous theme
        if self.bundleItem is not None:
            self.endExecution(self.bundleItem)

        CodeEditorBaseProcessor.beginExecution(self, theme)

        self.editor.setCurrentCharFormat(theme.textCharFormat())
        self.editor.setPalette(theme.palette())
        self.editor.syntaxHighlighter.start()
        self.editor.themeChanged.emit(theme)

    def endExecution(self, bundleItem):
        CodeEditorBaseProcessor.endExecution(self, bundleItem)

    def textCharFormat(self, scope):
        return self.bundleItem.textCharFormat(scope)

    def textCharFormats(self, userData):
        formats = []
        for token in userData.tokens():
            frange = QtGui.QTextLayout.FormatRange()
            frange.start = token.start
            frange.length = token.end - token.start
            frange.format = self.textCharFormat(token.scope)
            formats.append(frange)
        return formats
