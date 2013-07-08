#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import PMXBundleItem
   
class PMXProxy(PMXBundleItem):
    KEYS = ( 'content', )
    TYPE = 'proxy'
    FOLDER = 'Proxies'
    EXTENSION = 'tmProxy'
    PATTERNS = ('*.tmProxy', '*.plist')
    DEFAULTS = {
        'name': 'untitled'
    }