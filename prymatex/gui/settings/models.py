#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex.gui.configure.models import PMXConfigureTreeNode

class PMXSettingTreeNode(PMXConfigureTreeNode):
    def __init__(self, name, settingGroup = None, parent = None):
        PMXConfigureTreeNode.__init__(self, name, parent)
        self.settingGroup = settingGroup

    def loadSettings(self):
        pass
