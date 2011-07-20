#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import uuid as uuidmodule
from prymatex.support.manager import PMXSupportBaseManager
from prymatex.core.base import PMXObject
from prymatex.core.config import pmxConfigPorperty
from prymatex.gui.support.models import PMXBundleTreeModel, PMXBundleTreeNode, PMXThemeStylesTableModel, PMXThemeStyleRow
from prymatex.gui.support.proxies import PMXBundleTreeProxyModel, PMXBundleTypeFilterProxyModel, PMXThemeStyleTableProxyModel, PMXBundleProxyModel
from prymatex.mvc.proxies import bisect

class PMXSupportModelManager(PMXSupportBaseManager, PMXObject):
    #Signals
    bundleItemTriggered = QtCore.pyqtSignal(object)
    
    #Settings
    shellVariables = pmxConfigPorperty(default = [], tm_name = u'OakShelVariables')
    
    @pmxConfigPorperty(default = [], tm_name = u'OakBundleManagerDeletedBundles')
    def deleted(self, deleted):
        self.deletedObjects = map(lambda uuid: uuidmodule.UUID(uuid), deleted)
        
    @pmxConfigPorperty(default = [], tm_name = u'OakBundleManagerDeletedBundles')
    def disabled(self, disabled):
        self.disabledObjects = map(lambda uuid: uuidmodule.UUID(uuid), disabled)
        
    class Meta:
        settings = 'Manager'
    
    def __init__(self):
        PMXObject.__init__(self)
        PMXSupportBaseManager.__init__(self)
        self.bundleTreeModel = PMXBundleTreeModel(self)
        self.themeStylesTableModel = PMXThemeStylesTableModel(self)
        self.themeListModel = []
        
        #STYLE PROXY
        self.themeStyleProxyModel = PMXThemeStyleTableProxyModel()
        self.themeStyleProxyModel.setSourceModel(self.themeStylesTableModel)

        #TREE PROXY
        self.bundleProxyTreeModel = PMXBundleTreeProxyModel()
        self.bundleProxyTreeModel.setSourceModel(self.bundleTreeModel)

        #BUNDLES
        self.bundleProxyModel = PMXBundleProxyModel()
        self.bundleProxyModel.setSourceModel(self.bundleTreeModel)
        
        #TEMPLATES
        self.templateProxyModel = PMXBundleTypeFilterProxyModel("template")
        self.templateProxyModel.setSourceModel(self.bundleTreeModel)
        
        #SYNTAX
        self.syntaxProxyModel = PMXBundleTypeFilterProxyModel("syntax")
        self.syntaxProxyModel.setSourceModel(self.bundleTreeModel)
        def syntaxDisplayFormater(index):
            if not index.isValid():
                return None
            item = index.internalPointer()
            return item.buildMenuTextEntry()
        self.syntaxProxyModel.setFormater(syntaxDisplayFormater, QtCore.Qt.DisplayRole)
        
        #INTERACTIVEITEMS
        self.actionItemsProxyModel = PMXBundleTypeFilterProxyModel(["command", "snippet", "macro"])
        self.actionItemsProxyModel.setSourceModel(self.bundleTreeModel)
        
        #PREFERENCES
        self.preferenceProxyModel = PMXBundleTypeFilterProxyModel("preference")
        self.preferenceProxyModel.setSourceModel(self.bundleTreeModel)
        
        #DRAGCOMMANDS
        self.dragProxyModel = PMXBundleTypeFilterProxyModel("dragcommand")
        self.dragProxyModel.setSourceModel(self.bundleTreeModel)
        self.configure()

    def buildMenu(self, items, menu, submenus, parent = None):
        for uuid in items:
            if uuid.startswith('-'):
                menu.addSeparator()
                continue
            item = self.getBundleItem(uuid)
            if item != None:
                action = item.action(parent)
                receiver = lambda item = item: self.bundleItemTriggered.emit(item)
                self.connect(action, QtCore.SIGNAL('triggered()'), receiver)
                menu.addAction(action)
            elif uuid in submenus:
                submenu = QtGui.QMenu(submenus[uuid]['name'], parent)
                menu.addMenu(submenu)
                self.buildMenu(submenus[uuid]['items'], submenu, submenus, parent)
                
    def buildBundleMenu(self, bundle, parent):
        if bundle.mainMenu != None:
            menu = bundle.menu(parent)
            submenus = bundle.mainMenu['submenus'] if 'submenus' in bundle.mainMenu else {}
            items = bundle.mainMenu['items'] if 'items' in bundle.mainMenu else []
            self.buildMenu(items, menu, submenus, parent)
            return menu
    
    def buildEnvironment(self):
        env = {}
        for var in self.shellVariables:
            if var['enabled']:
                env[var['variable']] = var['value']
        env.update(self.environment)
        return env

    #---------------------------------------------------
    # MANAGED OBJECTS OVERRIDE INTERFACE
    #---------------------------------------------------
    def setDeleted(self, uuid):
        '''
            Marcar un managed object como eliminado
        '''
        self.deletedObjects.append(uuid)
        deleted = map(lambda uuid: unicode(uuid).upper(), self.deletedObjects)
        self._meta.settings.setValue('deleted', deleted)

    def isDeleted(self, uuid):
        '''
            Marcar un managed object como eliminado
        '''
        return uuid in self.deletedObjects

    def isDisabled(self, uuid):
        return uuid in self.disabledObjects

    #---------------------------------------------------
    # BUNDLE OVERRIDE INTERFACE 
    #---------------------------------------------------
    def addBundle(self, bundle):
        bundleNode = PMXBundleTreeNode(bundle)
        self.bundleTreeModel.appendBundle(bundleNode)
        return bundleNode
    
    def removeBundle(self, bundle):
        self.bundleTreeModel.removeBundle(bundle)
    
    def getAllBundles(self):
        return self.bundleProxyModel.getAllItems()
    
    #---------------------------------------------------
    # BUNDLEITEM OVERRIDE INTERFACE 
    #---------------------------------------------------
    def addBundleItem(self, bundleItem):
        bundleItemNode = PMXBundleTreeNode(bundleItem)
        self.bundleTreeModel.appendBundleItem(bundleItemNode)
        super(PMXSupportModelManager, self).addBundleItem(bundleItemNode)
        return bundleItemNode
    
    def removeBundleItem(self, bundleItem):
        self.bundleTreeModel.removeBundleItem(bundleItem)
    
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
    
    def getAllThemes(self):
        return self.themeListModel
    
    def addThemeStyle(self, style):
        themeStyle = PMXThemeStyleRow(style)
        self.themeStylesTableModel.appendStyle(themeStyle)
        return themeStyle
    
    def removeThemeStyle(self, style):
        self.themeStylesTableModel.removeStyle(style)

    #---------------------------------------------------
    # PREFERENCES OVERRIDE INTERFACE
    #---------------------------------------------------
    def getAllPreferences(self):
        return self.preferenceProxyModel.getAllItems()
    
    #---------------------------------------------------
    # TABTRIGGERS OVERRIDE INTERFACE
    #---------------------------------------------------
    def getAllTabTriggersMnemonics(self):
        for item in self.actionItemsProxyModel.getAllItems():
            if item.tabTrigger != None:
                yield item.tabTrigger
        else:
            raise StopIteration()
            
    def getAllBundleItemsByTabTrigger(self, tabTrigger):
        for item in self.actionItemsProxyModel.getAllItems():
            if item.tabTrigger == tabTrigger:
                yield item
        else:
            raise StopIteration()
            
    #---------------------------------------------------
    # KEYEQUIVALENT OVERRIDE INTERFACE
    #---------------------------------------------------
    def getAllBundleItemsByKeyEquivalent(self, keyEquivalent):
        for item in self.actionItemsProxyModel.getAllItems():
            if item.keyEquivalent == keyEquivalent:
                yield item
        for syntax in self.syntaxProxyModel.getAllItems():
            if syntax.keyEquivalent == keyEquivalent:
                yield syntax
        else:
            raise StopIteration()
    
    #---------------------------------------------------
    # ACTION ITEMS OVERRIDE INTERFACE
    #---------------------------------------------------
    def getAllActionItems(self):
        return self.actionItemsProxyModel.getAllItems()
    
    #---------------------------------------------------
    # SYNTAXES OVERRIDE INTERFACE
    #---------------------------------------------------
    def getAllSyntaxes(self):
        return self.syntaxProxyModel.getAllItems()