#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import BundleItem
   
class Proxy(BundleItem):
    KEYS = ( 'content', )
    FOLDER = 'Proxies'
    EXTENSION = 'tmProxy'
    PATTERNS = ('*.tmProxy', '*.plist')
    DEFAULTS = {
        'name': 'untitled'
    }