#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import CodeEditorBaseProcessor

from prymatex.support.processor import BaseProcessorMixin

class CodeEditorThemeProcessor(CodeEditorBaseProcessor, BaseProcessorMixin):
    def beginExecution(self, bundleItem):
        print("vamos themes")
        CodeEditorBaseProcessor.beginExecution(self, bundleItem)

    def endExecution(self, bundleItem):
        print("no vamos mas")
        CodeEditorBaseProcessor.endExecution(self, bundleItem)
