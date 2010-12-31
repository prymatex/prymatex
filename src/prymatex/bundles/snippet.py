#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Snippte's module
        content, name, scope, keyEquivalent, tabTrigger
'''

PMX_SNIPPETS = {}

class PMXSnippet(object):
    def __init__(self, hash, name_space):
        self.name_space = name_space
        PMX_SNIPPETS.setdefault(self.name_space, {})
        #Todo lo que diga scope es en que scope esta, puede ser mas de uno
        if 'scope' in hash:
            scopes = hash['scope'].split(', ')
            for scope in scopes:
                PMX_SNIPPETS[self.name_space][scope] = self 
        self.content = hash.get('content')
        self.name = hash.get('name')
        self.keyEquivalent = hash.get('keyEquivalent')
        self.tabTrigger = hash.get('tabTrigger')
        