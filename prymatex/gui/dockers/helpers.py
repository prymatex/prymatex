#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.core.plugin.dock import PMXBaseDockKeyHelper

class RefreshHelper(PMXBaseDockKeyHelper):
    KEY = QtCore.Qt.Key_F5
    def execute(self, event):
        print "actualizar"