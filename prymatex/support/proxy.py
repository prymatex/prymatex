#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.support.bundle import PMXBundleItem
from prymatex.utils import plist
   
class PMXProxy(PMXBundleItem):
    KEYS = ( 'content' )
    TYPE = 'proxy'
    FOLDER = 'Proxies'
    EXTENSION = 'tmProxy'
    PATTERNS = ('*.tmProxy', '*.plist')
