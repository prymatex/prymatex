#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.support.processor import PMXSnippetProcessor

class PMXSnippetProcessor(PMXSnippetProcessor):
    def __init__(self, editor):
        super(PMXSnippetProcessor, self).__init__()
        self.editor = editor
        self.snippet = None
        
    @property
    def hasSnippet(self):
        return self.snippet is not None
        
    def startSnippet(self, snippet):
        self.snippet = snippet
        
    def endSnippet(self):
        self.snippet = None