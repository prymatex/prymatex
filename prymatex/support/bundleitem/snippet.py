#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""Snippte's module"""
from ..regexp import Snippet, SnippetHandler
from .base import PMXBundleItem

class PMXSnippet(PMXBundleItem, SnippetHandler):
    KEYS = ( 'content', 'disableAutoIndent', 'inputPattern' )
    TYPE = 'snippet'
    FOLDER = 'Snippets'
    EXTENSION = 'tmSnippet'
    PATTERNS = ('*.tmSnippet', '*.plist')
    # ----- Default Snippet content on create action
    DEFAULTS = {
        'name': 'untitled',
        'content': '''Syntax Summary:
Variables        $TM_FILENAME, $TM_SELECTED_TEXT
Fallback Values  ${TM_SELECTED_TEXT:$TM_CURRENT_WORD}'''
    }
    
    def __load_update(self, dataHash, initialize):
        for key in PMXSnippet.KEYS:
            if key in dataHash or initialize:
                setattr(self, key, dataHash.get(key, None))
    
    def load(self, dataHash):
        PMXBundleItem.load(self, dataHash)
        self.__load_update(dataHash, True)
    
    def update(self, dataHash):
        PMXBundleItem.update(self, dataHash)
        self.__load_update(dataHash, False)
        if 'content' in dataHash and hasattr(self, '_snippetNode'):
            delattr(self, '_snippetNode')

    def dump(self, allKeys = False):
        dataHash = super(PMXSnippet, self).dump(allKeys)
        for key in PMXSnippet.KEYS:
            value = getattr(self, key)
            if value is not None:
                dataHash[key] = value
        return dataHash
      
    def execute(self, processor):
        if not hasattr(self, 'snippet'):
            self.setSnippet(Snippet(self.content))
        processor.startSnippet(self)
        SnippetHandler.execute(self, processor)
        if self.lastHolder():
            processor.endSnippet(self)
        else:
            processor.selectHolder()
