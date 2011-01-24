#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Snippte's module
'''

from prymatex.bundles.base import PMXBundleItem
from prymatex.bundles.processor import PMXSyntaxProcessor, PMXDebugSyntaxProcessor

class PMXSnippetProcessor(PMXSyntaxProcessor):
    def __init__(self, snippet):
        self.snippet = snippet
        self.lines = []
        
    def open_tag(self, name, start):
        self.stack.append((name, start))

    def close_tag(self, name, end):
        start = 0
        for index in range(len(self.stack))[::-1]:
            if name == self.stack[index][0]:
                _, start = self.stack.pop(index)
                break
        self.elements.append((name, start, end))

    def new_line(self, line):
        self.lines.append([])
        self.elements = self.lines[-1]
        self.stack = []

    def start_parsing(self, name):
        print "start", name

    def end_parsing(self, name):
        self.snippet.lines = self.lines
        print "end", name
        
class PMXSnippet(PMXBundleItem):
    parser = None
    def __init__(self, hash, name_space = "default"):
        super(PMXSnippet, self).__init__(hash, name_space)
        for key in [    'content', 'disableAutoIndent', 'inputPattern', 'bundlePath' ]:
            setattr(self, key, hash.pop(key, None))
    
    def compile(self):
        if self.parser == None:
            #FIXME: obtenerlo de una forma mas limpia
            self.__class__.parser = self.bundle.getBundleByName('Bundle Development').syntaxes[1]
        self.parser.parse(self.content, PMXSnippetProcessor(self))
        self.text = self.content
        text = self.content.splitlines()
        for index in xrange(text):
            self.lines[index]
            