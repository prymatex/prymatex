# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui

from prymatex.core.base import PMXObject
from prymatex.gui.bundles.ui_editor import Ui_bundleEditor
from prymatex.gui.bundles.models import PMXBundleTreeProxyModel, PMXBundleTreeModel

class PMXBundleEditor(Ui_bundleEditor, QtGui.QWidget, PMXObject):
    '''
        Prymatex Bundle Editor
    '''
    def __init__(self, manager = None):
        super(PMXBundleEditor, self).__init__()
        self.setupUi(self)
        self.stackLayout = QtGui.QStackedLayout()
        self.configSelectTop()
        self.configTreeView(manager)
        self.select_top.currentIndexChanged[int].connect(self.selectTopChange)
        self.setWindowTitle(QtGui.QApplication.translate("bundleEditor", "Bundle Editor", None, QtGui.QApplication.UnicodeUTF8))

    def selectTopChange(self, index):
        value = self.select_top.itemData(index).toString()
        print value
        self.proxyTreeModel.setFilterRegExp(value)
        
    def configSelectTop(self):
        self.select_top.addItem("Show all", QtCore.QVariant(""))
        self.select_top.addItem("Syntaxs", QtCore.QVariant("syntax"))
        self.select_top.addItem("Snippets", QtCore.QVariant("snippet"))
        self.select_top.addItem("Macros", QtCore.QVariant("macro"))
        self.select_top.addItem("Commands", QtCore.QVariant("command"))
        self.select_top.addItem("DragCommands", QtCore.QVariant("dragcommand"))
        self.select_top.addItem("Preferences", QtCore.QVariant("preference"))
        self.select_top.addItem("Templates", QtCore.QVariant("template*"))
    
    def configTreeView(self, manager = None):
        if manager is None:
            self.treeModel = PMXBundleTreeModel(self.pmxApp.supportManager)
        else:
            self.treeModel = PMXBundleTreeModel(manager)
        self.proxyTreeModel = PMXBundleTreeProxyModel()
        self.proxyTreeModel.setSourceModel(self.treeModel)
        self.proxyTreeModel.sort(0)
        self.treeView.setModel(self.proxyTreeModel)
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
