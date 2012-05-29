#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtGui

from prymatex.core.plugin.dialog import PMXBaseDialog

from ProgressDialog.ui_progress import Ui_ProgressDialog

# {   'title': 'Progress', 
#     'summary': u'Creating HTML version of document\u2026', 
#     'details': '', 
#     'isIndeterminate': True, 
#     'progressAnimate': True
# }

class ProgressDialog(QtGui.QDialog, Ui_ProgressDialog, PMXBaseDialog):
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        PMXBaseDialog.__init__(self)
        self.setupUi(self)
        
    def setParameters(self, parameters):
        print parameters
        
dialogClass = ProgressDialog