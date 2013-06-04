#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import hashlib

from prymatex.qt import QtCore, QtGui

from prymatex.core import PMXBaseComponent

class PersistenceManager(QtCore.QObject, PMXBaseComponent):
    def __init__(self, application):
        QtCore.QObject.__init__(self, application)
        PMXBaseComponent.__init__(self)
        self.memoize = {}

    def buildKey(self, content):
        """docstring for buildKey"""
        return hashlib.sha1(content.encode("utf-8")).hexdigest()