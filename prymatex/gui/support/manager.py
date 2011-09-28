#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import uuid as uuidmodule
from prymatex.support.manager import PMXSupportBaseManager
from prymatex.core.base import PMXObject
from prymatex.core.settings import pmxConfigPorperty
from prymatex.gui.support.models import PMXBundleTreeModel, PMXBundleTreeNode, PMXThemeStylesTableModel, PMXThemeStyleRow
from prymatex.gui.support.proxies import PMXBundleTreeProxyModel, PMXBundleTypeFilterProxyModel, PMXThemeStyleTableProxyModel, PMXBundleProxyModel, PMXSyntaxProxyModel
from prymatex.mvc.proxies import bisect_key

class PMXBundleMenuGroup(QtCore.QObject):
    def __init__(self, manager, parent = None):
        QtCore.QObject.__init__(self, parent)
        self.manager = manager
        self.bundleTreeModel = self.manager.bundleTreeModel
        self.menus = {}
        self.bundleTreeModel.dataChanged.connect(self.on_bundleTreeModel_dataChanged)
        self.bundleTreeModel.rowsInserted.connect(self.on_bundleTreeModel_rowsInserted)
        self.bundleTreeModel.rowsRemoved.connect(self.on_bundleTreeModel_rowsRemoved)
        
        
    def buildMenu(self, items, menu, submenus, parent = None):
        for uuid in items:
            if uuid.startswith('-'):
                menu.addSeparator()
                continue
            item = self.manager.getBundleItem(uuid)
            if item != None:
                action = QtGui.QAction(QtGui.QIcon(item.icon), item.buildMenuTextEntry(), parent)
                receiver = lambda item = item: self.manager.bundleItemTriggered.emit(item)
                self.connect(action, QtCore.SIGNAL('triggered()'), receiver)
                menu.addAction(action)
            elif uuid in submenus:
                submenu = QtGui.QMenu(submenus[uuid]['name'], parent)
                menu.addMenu(submenu)
                self.buildMenu(submenus[uuid]['items'], submenu, submenus, parent)

    def buildBundleMenu(self, bundle, parent):
        menu = QtGui.QMenu(bundle.buildBundleAccelerator(), parent)
        if bundle.mainMenu is not None:
            submenus = bundle.mainMenu['submenus'] if 'submenus' in bundle.mainMenu else {}
            items = bundle.mainMenu['items'] if 'items' in bundle.mainMenu else []
            self.buildMenu(items, menu, submenus, parent)
        menu.menuAction().setVisible(not (bundle.disabled or bundle.mainMenu is None))
        return menu

    def addBundle(self, bundle):
        self.menus[bundle] = self.buildBundleMenu(bundle, self.parent())
        self.parent().addMenu(self.menus[bundle])

    def on_bundleTreeModel_dataChanged(self, topLeft, bottomRight):
        #TODO: ver que pasa con el bottomRight
        item = topLeft.internalPointer()
        if item.TYPE == "bundle":
            self.menus[item].setTitle(item.buildBundleAccelerator())
            self.menus[item].menuAction().setVisible(not (item.disabled or item.mainMenu is None))

    def on_bundleTreeModel_rowsInserted(self, parent, start, end):
        for row in range(start, end + 1):
            index = self.bundleTreeModel.index(row, 0, parent)
            item = index.internalPointer()
            if item.TYPE == "bundle":
                if item in self.menus:
                    self.menus[item].menuAction().setVisible(not (item.disabled or item.mainMenu is None))
                else:
                    self.addBundle(item, self.parent())
    
    def on_bundleTreeModel_rowsRemoved(self, parent, start, end):
        print "Remove indexes"

class PMXSupportManager(PMXSupportBaseManager, PMXObject):
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
        
    SETTINGS_GROUP = 'SupportManager'
    
    def __init__(self):
        PMXObject.__init__(self)
        PMXSupportBaseManager.__init__(self)
        self.bundleTreeModel = PMXBundleTreeModel(self)
        self.themeStylesTableModel = PMXThemeStylesTableModel(self)
        self.themeListModel = []
        
        #STYLE PROXY
        self.themeStyleProxyModel = PMXThemeStyleTableProxyModel(self)
        self.themeStyleProxyModel.setSourceModel(self.themeStylesTableModel)

        #TREE PROXY
        self.bundleProxyTreeModel = PMXBundleTreeProxyModel(self)
        self.bundleProxyTreeModel.setSourceModel(self.bundleTreeModel)

        #BUNDLES
        self.bundleProxyModel = PMXBundleProxyModel(self)
        self.bundleProxyModel.setSourceModel(self.bundleTreeModel)
        
        #TEMPLATES
        self.templateProxyModel = PMXBundleTypeFilterProxyModel("template", self)
        self.templateProxyModel.setSourceModel(self.bundleTreeModel)
        
        #SYNTAX
        self.syntaxProxyModel = PMXSyntaxProxyModel(self)
        self.syntaxProxyModel.setSourceModel(self.bundleTreeModel)
        
        #INTERACTIVEITEMS
        self.actionItemsProxyModel = PMXBundleTypeFilterProxyModel(["command", "snippet", "macro"], self)
        self.actionItemsProxyModel.setSourceModel(self.bundleTreeModel)
        
        #PREFERENCES
        self.preferenceProxyModel = PMXBundleTypeFilterProxyModel("preference", self)
        self.preferenceProxyModel.setSourceModel(self.bundleTreeModel)
        
        #DRAGCOMMANDS
        self.dragProxyModel = PMXBundleTypeFilterProxyModel("dragcommand", self)
        self.dragProxyModel.setSourceModel(self.bundleTreeModel)
        self.configure()

    def appendBundleMenuGroup(self, menu):
        group = PMXBundleMenuGroup(self, menu)
        name_order = lambda b1, b2: cmp(b1.name, b2.name)
        for bundle in sorted(self.application.supportManager.getAllBundles(), name_order):
            group.addBundle(bundle)

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
        self.settings.setValue('deleted', deleted)

    def isDeleted(self, uuid):
        return uuid in self.deletedObjects

    def isDisabled(self, uuid):
        return uuid in self.disabledObjects
    
    def setDisabled(self, uuid):
        self.disabledObjects.append(uuid)
        disabled = map(lambda uuid: unicode(uuid).upper(), self.disabledObjects)
        self.settings.setValue('disabled', disabled)
        
    def setEnabled(self, uuid):
        self.disabledObjects.remove(uuid)
        disabled = map(lambda uuid: unicode(uuid).upper(), self.disabledObjects)
        self.settings.setValue('disabled', disabled)
    
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
        super(PMXSupportManager, self).addBundleItem(bundleItemNode)
        return bundleItemNode
    
    def removeBundleItem(self, bundleItem):
        self.bundleTreeModel.removeBundleItem(bundleItem)
        
    def getAllBundleItems(self):
        for bundle in self.getAllBundles():
            for item in bundle.children:
                yield item
    
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
        index = bisect_key(self.themeListModel, themeRow, lambda t: t.name)
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