#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import sha
import functools

from PyQt4 import QtCore

from prymatex.core.plugin import PMXBaseComponent

class PMXCacheManager(QtCore.QObject, PMXBaseComponent):
    def __init__(self):
        QtCore.QObject.__init__(self)
        self.memoize = {}

    def buildKey(self, content):
        """docstring for buildKey"""
        return sha.sha(content).hexdigest()