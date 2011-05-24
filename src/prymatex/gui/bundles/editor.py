# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui_bundle_editor import Ui_bundleEditor
import os, sys, re, plistlib
from glob import glob
from copy import copy, deepcopy
from xml.parsers.expat import ExpatError

from prymatex.core.base import PMXObject
from prymatex.gui.bundles.models import PMBBundleTreeModel

class PMXBundleEditor(Ui_bundleEditor, QWidget, PMXObject):
    '''
        Primatex Bundle Editor
    '''
    def __init__(self):
        super(PMXBundleEditor, self).__init__()
        self.setupUi(self)
        self.stackLayout = QStackedLayout()
        self.configSelectTop()
        self.configTreeView()
        self.connect(self.btn_apply, SIGNAL("clicked()"), self.onApply)
        self.connect(self.select_top, SIGNAL("currentIndexChanged(int)"), self.selectTopChange)
        self.setWindowTitle(QApplication.translate("bundleEditor", "Bundle Editor", None, QApplication.UnicodeUTF8))

    def selectTopChange(self, index):
        if index == 0:
            self.proxyModel.setFilterRegExp("")
        elif index == 1:
            self.proxyModel.setFilterRegExp(QRegExp("Bundle|(b)|(Sy)|Syntax"))
        elif index == 2:
            self.proxyModel.setFilterRegExp(QRegExp("Bundle|(b)|(Sn)|Snippets"))
        elif index == 3:
            self.proxyModel.setFilterRegExp(QRegExp("Bundle|(b)|(M)|Macros"))
        elif index == 4:
            self.proxyModel.setFilterRegExp(QRegExp("Bundle|(b)|(C)|Command"))
        elif index == 5:
            self.proxyModel.setFilterRegExp(QRegExp("Bundle|(b)|(P)|Preference"))
        elif index == 6:
            self.proxyModel.setFilterRegExp(QRegExp("Bundle|(b)|(T)|Template"))
        #self.proxyModel.setFilterKeyColumn(0)
        
    def configSelectTop(self):
        self.select_top.removeItem(0)
        self.select_top.removeItem(0)
        
        self.select_top.addItem("Show all", QtCore.QVariant("all"))
        self.select_top.addItem("Syntaxs", QtCore.QVariant("syntax"))
        self.select_top.addItem("Snippets", QtCore.QVariant("snippet"))
        self.select_top.addItem("Macros", QtCore.QVariant("macro"))
        self.select_top.addItem("Commands", QtCore.QVariant("command"))
        self.select_top.addItem("DragCommands", QtCore.QVariant("dragcommand"))
        self.select_top.addItem("Preferences", QtCore.QVariant("preference"))
        self.select_top.addItem("Templates", QtCore.QVariant("template"))
    
    def configTreeView(self):
                
        self.treeModel = PMBBundleTreeModel(self.pmxApp.supportManager)
        self.treeView.setModel(self.treeModel)
        self.treeView.setHeaderHidden(True)
        self.treeView.setAnimated(True)
        
    def setCentralWidget(self, objeto):
        pass
    
    def setStatusBar(self, objeto):
        pass

    def onApply(self):
        #self.proxyModel.setFilterRegExp(QRegExp("Bundle|(b)|(s)|Syntax"))
        #self.proxyModel.setFilterKeyColumn(0)
        print "Apply!!"
