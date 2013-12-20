#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""Snippte's module"""
from ..regexp import Snippet as SnippetObject
from ..regexp import SnippetHandler
from .base import BundleItem

class Snippet(BundleItem, SnippetHandler):
    KEYS = ( 'content', 'disableAutoIndent', 'inputPattern' )
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
        for key in Snippet.KEYS:
            if key in dataHash or initialize:
                setattr(self, key, dataHash.get(key, None))
    
    def load(self, dataHash):
        BundleItem.load(self, dataHash)
        self.__load_update(dataHash, True)
    
    def update(self, dataHash):
        BundleItem.update(self, dataHash)
        self.__load_update(dataHash, False)
        if 'content' in dataHash and hasattr(self, '_snippetNode'):
            delattr(self, '_snippetNode')

    def dump(self, allKeys = False):
        dataHash = super(Snippet, self).dump(allKeys)
        for key in Snippet.KEYS:
            value = getattr(self, key)
            if value is not None:
                dataHash[key] = value
        return dataHash
      
    def execute(self, processor):
        if not hasattr(self, 'snippet'):
            self.setSnippet(SnippetObject(self.content))
        processor.beginExecution(self)
        SnippetHandler.execute(self, processor)
        if not processor.managed():
            processor.endExecution(self)
        else:
            # TODO: Solo si tiene holders sino un end esta bien tambien
            processor.selectHolder()
        
