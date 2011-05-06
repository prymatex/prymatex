# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui_bundle_editor import Ui_bundleEditor
import os, sys, re, plistlib
from glob import glob
from copy import copy, deepcopy
from xml.parsers.expat import ExpatError

from prymatex.gui.editor import center
from prymatex.gui.mixins.common import CenterWidget


try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class PMXBundleEditor(Ui_bundleEditor, QWidget):
    '''
        Primatex Bundle Editor
    '''
    def __init__(self):
        super(PMXBundleEditor, self).__init__()
        self.setupUi(self)
        self.stackLayout = QStackedLayout()
        self.configSelectTop()
        self.configTreeView()
        self.connect(self.btn_apply, SIGNAL("clicked()"),self.onApply)
        self.connect(self.select_top, SIGNAL("currentIndexChanged(int)"), self.selectTopChange)
        self.setWindowTitle(QApplication.translate("bundleEditor", "Bundle Editor", None, QApplication.UnicodeUTF8))
        #qApp.instance().
        

    def selectTopChange(self, index):
        pass
            
    def configSelectTop(self):
        self.select_top.removeItem(0)
        self.select_top.removeItem(0)
        
        self.select_top.addItem(_fromUtf8("Show all"))
        self.select_top.addItem(_fromUtf8("  Syntaxs"))
        self.select_top.addItem(_fromUtf8("  Snippets"))
        self.select_top.addItem(_fromUtf8("  Macros"))
        self.select_top.addItem(_fromUtf8("  Command"))
        self.select_top.addItem(_fromUtf8("  Preference"))
        self.select_top.addItem(_fromUtf8("  Template"))
    
    def configTreeView(self):
        pass
        
    def setCentralWidget(self, objeto):
        pass
    
    def setStatusBar(self, objeto):
        pass

    def onApply(self):
        #self.proxyModel.setFilterRegExp(QRegExp("Bundle|(b)|(s)|Syntax"))
        #self.proxyModel.setFilterKeyColumn(0)
        print "Apply!!"
        


    

    
    

    