#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from prymatex.support.manager import PMXSupportManager
from prymatex.core.base import PMXObject
from prymatex.core.config import pmxConfigPorperty
from prymatex.gui.support.models import PMXBundleTreeModel, PMXBundleTreeNode
from prymatex.gui.support.proxies import PMXBundleTreeProxyModel, PMXBundleTypeFilterProxyModel

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
        
        #Proxy
        self.bundleProxyTreeModel = PMXBundleTreeProxyModel()
        self.bundleProxyTreeModel.setSourceModel(self.bundleTreeModel)
        
        self.templateProxyModel = PMXBundleTypeFilterProxyModel("template")
        self.templateProxyModel.setSourceModel(self.bundleTreeModel)
        
        self.syntaxProxyModel = PMXBundleTypeFilterProxyModel("syntax")
        self.syntaxProxyModel.setSourceModel(self.bundleTreeModel)
        
        self.preferenceProxyModel = PMXBundleTypeFilterProxyModel("preference")
        self.preferenceProxyModel.setSourceModel(self.bundleTreeModel)
        
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

    def getAllBundles(self):
        return self.bundleTreeModel.getAllBundles()
    
    #---------------------------------------------------
    # BUNDLEITEM OVERRIDE INTERFACE 
    #---------------------------------------------------
    def addBundleItem(self, bundleItem):
        bundleItemNode = PMXBundleTreeNode(bundleItem)
        if bundleItem.TYPE == "template":
            for file in bundleItem.getTemplateFiles():
                bundleTemplateFileNode = PMXBundleTreeNode(file)
                bundleItemNode.appendChild(bundleTemplateFileNode)
        bundleItem.bundle.appendChild(bundleItemNode)
        return bundleItemNode

    #---------------------------------------------------
    # THEME OVERRIDE INTERFACE
    #---------------------------------------------------
    def hasTheme(self, uuid):
        return PMXSupportManager.hasTheme(self, uuid)

    def addTheme(self, theme):
        return PMXSupportManager.addTheme(self, theme)

    def getTheme(self, uuid):
        return PMXSupportManager.getTheme(self, uuid)

    def getAllThemes(self):
        return PMXSupportManager.getAllThemes(self)

    def getAllTemplates(self):
        return PMXSupportManager.getAllTemplates(self)

    def getPreferences(self, scope):
        return PMXSupportManager.getPreferences(self, scope)

