#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from prymatex.support.manager import PMXSupportManager
from prymatex.core.base import PMXObject
from prymatex.core.config import pmxConfigPorperty
from prymatex.gui.support.models import PMXBundleTreeModel, PMXBundleTreeNode, PMXThemeStylesTableModel, PMXThemeStyleRow
from prymatex.gui.support.proxies import PMXBundleTreeProxyModel, PMXBundleTypeFilterProxyModel, PMXThemeStyleTableProxyModel
from prymatex.mvc.proxies import bisect

class PMXSupportModelManager(PMXSupportManager, PMXObject):
    #Settings
    shellVariables = pmxConfigPorperty(default = [], tm_name = u'OakShelVariables')
    deletedBundles = pmxConfigPorperty(default = [], tm_name = u'OakBundleManagerDeletedBundles')
    disabledBundles = pmxConfigPorperty(default = [], tm_name = u'OakBundleManagerDisabledBundles')
    
    class Meta:
        settings = 'Manager'
    
    def __init__(self):
        self.configure()
        super(PMXSupportModelManager, self).__init__(self.disabledBundles, self.deletedBundles)
        self.bundleTreeModel = PMXBundleTreeModel(self)
        self.themeStylesTableModel = PMXThemeStylesTableModel(self)
        self.themeListModel = []
        
        #STYLE PROXY
        self.themeStyleProxyModel = PMXThemeStyleTableProxyModel()
        self.themeStyleProxyModel.setSourceModel(self.themeStylesTableModel)
        
        #TREE PROXY
        self.bundleProxyTreeModel = PMXBundleTreeProxyModel()
        self.bundleProxyTreeModel.setSourceModel(self.bundleTreeModel)
        
        #TEMPLATES
        self.templateProxyModel = PMXBundleTypeFilterProxyModel("template")
        self.templateProxyModel.setSourceModel(self.bundleTreeModel)
        
        #SYNTAX
        self.syntaxProxyModel = PMXBundleTypeFilterProxyModel("syntax")
        self.syntaxProxyModel.setSourceModel(self.bundleTreeModel)
        
        #INTERACTIVEITEMS
        self.itemsProxyModel = PMXBundleTypeFilterProxyModel(["command", "snippet", "macro"])
        self.itemsProxyModel.setSourceModel(self.bundleTreeModel)
        
        #PREFERENCES
        self.preferenceProxyModel = PMXBundleTypeFilterProxyModel("preference")
        self.preferenceProxyModel.setSourceModel(self.bundleTreeModel)
        
        #DRAGCOMMANDS
        self.dragProxyModel = PMXBundleTypeFilterProxyModel("dragcommand")
        self.dragProxyModel.setSourceModel(self.bundleTreeModel) 
        
    def buildEnvironment(self):
        env = {}
        for var in self.shellVariables:
            if var['enabled']:
                env[var['variable']] = var['value']
        env.update(self.environment)
        return env

    #---------------------------------------------------
    # BUNDLE OVERRIDE INTERFACE 
    #---------------------------------------------------
    def addBundle(self, bundle):
        bundleNode = PMXBundleTreeNode(bundle)
        self.bundleTreeModel.appendBundle(bundleNode)
        return bundleNode

    def getBundle(self, uuid):
        return self.bundleTreeModel.getBundle(uuid)
    
    def getAllBundles(self):
        return self.bundleTreeModel.getAllBundles()
    
    #---------------------------------------------------
    # BUNDLEITEM OVERRIDE INTERFACE 
    #---------------------------------------------------
    def addBundleItem(self, bundleItem):
        bundleItemNode = PMXBundleTreeNode(bundleItem)
        self.bundleTreeModel.appendBundleItem(bundleItemNode)
        super(PMXSupportModelManager, self).addBundleItem(bundleItemNode)
        return bundleItemNode
    
    #---------------------------------------------------
    # TEMPLATEFILE OVERRIDE INTERFACE
    #---------------------------------------------------
    def addTemplateFile(self, file):
        bundleTemplateFileNode = PMXBundleTreeNode(file)
        file.template.appendChild(bundleTemplateFileNode)
        return bundleTemplateFileNode
    
    #---------------------------------------------------
    # THEME OVERRIDE INTERFACE
    #---------------------------------------------------
    def addTheme(self, theme):
        themeRow = PMXThemeStyleRow(theme, self.scores)
        index = bisect(self.themeListModel, themeRow, lambda t1, t2: cmp(t1.name, t2.name))
        self.themeListModel.insert(index, themeRow)
        return themeRow
    
    def addThemeStyle(self, style):
        themeStyle = PMXThemeStyleRow(style)
        self.themeStylesTableModel.appendStyle(themeStyle)
        return themeStyle
    
    def getAllThemes(self):
        return self.themeListModel