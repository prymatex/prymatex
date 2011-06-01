# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui

from prymatex.gui.bundles.ui_snippet import Ui_Snippet
from prymatex.gui.bundles.ui_command import Ui_Command

class PMXSnippetWidget(QtGui.QWidget, Ui_Snippet):
    def __init__(self, parent = None):
        super(PMXSnippetWidget, self).__init__(parent)
        self.setupUi(self)

class PMXCommandWidget(QtGui.QWidget, Ui_Command):
    def __init__(self, parent = None):
        super(PMXCommandWidget, self).__init__(parent)
        self.setupUi(self)