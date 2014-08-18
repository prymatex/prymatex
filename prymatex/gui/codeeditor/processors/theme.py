#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import CodeEditorBaseProcessor

from prymatex.support.processor import ThemeProcessorMixin

class CodeEditorThemeProcessor(CodeEditorBaseProcessor, ThemeProcessorMixin):
    def beginExecution(self, bundleItem):
        if self.bundleItem == bundleItem:
            return

        self.editor.syntaxHighlighter.stop()
        CodeEditorBaseProcessor.beginExecution(self, bundleItem)

        theme = self.editor.application().supportManager.getBundleItem(bundleItem.uuid)        

        self.editor.setCurrentCharFormat(theme.textCharFormat())
        self.editor.setPalette(theme.palette())
        self.editor.syntaxHighlighter.setTheme(theme)
        self.editor.syntaxHighlighter.start()
        self.editor.themeChanged.emit(theme)

    def endExecution(self, bundleItem):
        CodeEditorBaseProcessor.endExecution(self, bundleItem)
