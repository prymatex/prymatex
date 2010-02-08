#!/usr/bin/env python
#-*- encoding: utf-8 -*-
# Created: 08/02/2010 by defo
from PyQt4.Qt import *

from ui_configdialog import Ui_ConfigDialog

class PMXConfigDialog(QDialog, Ui_ConfigDialog):
    def __init__(self, parent):
        QDialog.__init__(self)
        self.setupUi(self)
        self.setupTree()
        
    def setupTree(self):
        model = QStandardItemModel(self)
        
        self.treeView.setModel(model)