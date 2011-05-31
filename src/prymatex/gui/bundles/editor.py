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
        self.comboBoxItemFilter.currentIndexChanged[int].connect(self.selectTopChange)
        self.setWindowTitle(QtGui.QApplication.translate("bundleEditor", "Bundle Editor", None, QtGui.QApplication.UnicodeUTF8))

    def selectTopChange(self, index):
        value = self.comboBoxItemFilter.itemData(index).toString()
        self.proxyTreeModel.setFilterRegExp(value)
        
    def configSelectTop(self):
        self.comboBoxItemFilter.addItem("Show all", QtCore.QVariant(""))
        self.comboBoxItemFilter.addItem("Syntaxs", QtCore.QVariant("syntax"))
        self.comboBoxItemFilter.addItem("Snippets", QtCore.QVariant("snippet"))
        self.comboBoxItemFilter.addItem("Macros", QtCore.QVariant("macro"))
        self.comboBoxItemFilter.addItem("Commands", QtCore.QVariant("command"))
        self.comboBoxItemFilter.addItem("DragCommands", QtCore.QVariant("dragcommand"))
        self.comboBoxItemFilter.addItem("Preferences", QtCore.QVariant("preference"))
        self.comboBoxItemFilter.addItem("Templates", QtCore.QVariant("template*"))
    
    def configTreeView(self, manager = None):
        if manager is None:
            print "sin manager tomo de la tabla ya armada"
            self.treeModel = self.pmxApp.supportManager.bundleModel
        else:
            self.treeModel = PMXBundleTreeModel(manager)
            self.treeModel.populateFromManager()
        self.proxyTreeModel = PMXBundleTreeProxyModel()
        self.proxyTreeModel.setSourceModel(self.treeModel)
        self.proxyTreeModel.sort(0)
        self.treeView.setModel(self.proxyTreeModel)
        self.treeView.setHeaderHidden(True)
        self.treeView.setAnimated(True)
        self.treeView.pressed.connect(self.itemSelected)
        
    def itemSelected(self, index):
        print index, "hola"
        
    def setCentralWidget(self, objeto):
        pass
    
    def setStatusBar(self, objeto):
        pass

    
