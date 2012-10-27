#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import sha

from prymatex.qt import QtCore, QtGui

from prymatex.core import PMXBaseComponent

class CacheManager(QtCore.QObject, PMXBaseComponent):
    def __init__(self):
        QtCore.QObject.__init__(self)
        self.memoize = {}

    def buildKey(self, content):
        """docstring for buildKey"""
        return sha.sha(content).hexdigest()