#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fnmatch
import uuid as uuidmodule
from PyQt4 import QtCore, QtGui
from prymatex.support.manager import PMXSupportBaseManager
from prymatex.core.base import PMXObject
from prymatex.core.settings import pmxConfigPorperty
from prymatex.gui.support.models import PMXBundleTreeModel, PMXBundleTreeNode, PMXThemeStylesTableModel, PMXThemeStyleRow
from prymatex.gui.support.proxies import PMXBundleTreeProxyModel, PMXBundleTypeFilterProxyModel, PMXThemeStyleTableProxyModel, PMXBundleProxyModel, PMXSyntaxProxyModel
from prymatex.mvc.proxies import bisect_key

class PMXBundleMenuGroup(QtCore.QObject):
    def __init__(self, manager):
        QtCore.QObject.__init__(self, manager)
        self.manager = manager
        #TODO: No conectar al modelo preferir manager sobre modelo
        self.bundleTreeModel = self.manager.bundleTreeModel
        #The bundle menues
        self.menus = {}
        #The qt menus where a bundle menu is added
        self.containers = []
        self.manager.bundlePopulated.connect(self.on_manager_bundlePopulated)
        self.bundleTreeModel.dataChanged.connect(self.on_bundleTreeModel_dataChanged)
    
    def appendMenu(self, menu):
        if menu not in self.containers:
            self.containers.append(menu)
        #Append all bundle menus
        for m in self.menus.values():
            menu.addMenu(m)
        
    def buildMenu(self, items, menu, submenus, parent = None):
        for uuid in items:
            if uuid.startswith('-'):
                menu.addSeparator()
                continue
            item = self.manager.getBundleItem(uuid)
            if item != None:
                action = item.triggerItemAction(parent)
                menu.addAction(action)
            elif uuid in submenus:
                submenu = QtGui.QMenu(submenus[uuid]['name'], parent)
                menu.addMenu(submenu)
                self.buildMenu(submenus[uuid]['items'], submenu, submenus, parent)

    def buildBundleMenu(self, bundle):
        menu = QtGui.QMenu(bundle.buildBundleAccelerator())
        menu.ID = id(bundle.mainMenu)
        if bundle.mainMenu is not None:
            submenus = bundle.mainMenu['submenus'] if 'submenus' in bundle.mainMenu else {}
            items = bundle.mainMenu['items'] if 'items' in bundle.mainMenu else []
            self.buildMenu(items, menu, submenus, menu)
        return menu

    def addBundle(self, bundle):
        menu = self.buildBundleMenu(bundle)
        self.menus[bundle] = menu
        menu.menuAction().setVisible(bundle.enabled and bundle.mainMenu is not None)
        self.addToContainers(menu)
    
    def addToContainers(self, menu):
        for containter in self.containers:
            containter.addMenu(menu)

    def on_bundleTreeModel_dataChanged(self, topLeft, bottomRight):
        #TODO: ver que pasa con el bottomRight
        item = topLeft.internalPointer()
        if item.TYPE == "bundle":
            menu = self.menus.get(item, None)
            if menu is not None:
                title = item.buildBundleAccelerator()
                if title != menu.title():
                    menu.setTitle(title)
                if item.enabled != menu.menuAction().isVisible():
                    menu.menuAction().setVisible(item.enabled and item.mainMenu is not None)
                if id(item.mainMenu) != menu.ID:
                    menu.clear()
                    submenus = bundle.mainMenu['submenus'] if 'submenus' in bundle.mainMenu else {}
                    items = bundle.mainMenu['items'] if 'items' in bundle.mainMenu else []
                    self.buildMenu(items, menu, submenus, menu)
                    menu.ID = id(item.mainMenu)
        else:
            action = item.triggerItemAction()
            if action is not None:
                text = item.buildMenuTextEntry()
                if text != action.text():
                    action.setText(text)

    def on_manager_bundlePopulated(self, bundle):
        if bundle not in self.menus:
            self.addBundle(bundle)

class PMXSupportManager(PMXSupportBaseManager, PMXObject):
    #Signals
    bundleItemTriggered = QtCore.pyqtSignal(object)
    bundlePopulated = QtCore.pyqtSignal(object)
    
    #Settings
    shellVariables = pmxConfigPorperty(default = [], tm_name = u'OakShelVariables')
    
    @pmxConfigPorperty(default = [], tm_name = u'OakBundleManagerDeletedBundles')
    def deleted(self, deleted):
        self.deletedObjects = map(lambda uuid: uuidmodule.UUID(uuid), deleted)
        
    @pmxConfigPorperty(default = [], tm_name = u'OakBundleManagerDeletedBundles')
    def disabled(self, disabled):
        self.disabledObjects = map(lambda uuid: uuidmodule.UUID(uuid), disabled)
    
    #http://manual.macromates.com/en/expert_preferences.html
    #When you create a new item in the bundle editor without having selected a bundle first, then the bundle with the UUID held by this defaults key is used as the target
    defaultBundleForNewBundleItems = pmxConfigPorperty(default = u'B7BC3FFD-6E4B-11D9-91AF-000D93589AF6', tm_name = u'OakDefaultBundleForNewBundleItems')
        
    SETTINGS_GROUP = 'SupportManager'
    
    def __init__(self, parent = None):
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
        self.dragcommandProxyModel = PMXBundleTypeFilterProxyModel("dragcommand", self)
        self.dragcommandProxyModel.setSourceModel(self.bundleTreeModel)
        
        #BUNDLEMENUGROUP
        self.bundleMenuGroup = PMXBundleMenuGroup(self)
        self.configure()

    def appendMenuToBundleMenuGroup(self, menu):
        self.bundleMenuGroup.appendMenu(menu)

    def buildEnvironment(self):
        env = {}
        for var in self.shellVariables:
            if var['enabled']:
                env[var['variable']] = var['value']
        env.update(self.environment)
        return env
    
    # Override populate bundle for emit signal
    def populateBundle(self, bundle):
        PMXSupportBaseManager.populateBundle(self, bundle)
        self.bundlePopulated.emit(bundle)
    
    #---------------------------------------------------
    # MANAGED OBJECTS OVERRIDE INTERFACE
    #---------------------------------------------------
    def setDeleted(self, uuid):
        """
        Marcar un managed object como eliminado
        """
        self.deletedObjects.append(uuid)
        deleted = map(lambda uuid: unicode(uuid).upper(), self.deletedObjects)
        self.settings.setValue('deleted', deleted)

    def isDeleted(self, uuid):
        return uuid in self.deletedObjects

    def isEnabled(self, uuid):
        return uuid not in self.disabledObjects
    
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
    
    def getDefaultBundle(self):
        return self.getBundle(self.defaultBundleForNewBundleItems)
    
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
        items = []
        for bundle in self.getAllBundles():
            for item in bundle.children:
                items.append(item)
        return items
        
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
        tabTriggers = []
        for item in self.actionItemsProxyModel.getAllItems():
            if item.tabTrigger != None:
                tabTriggers.append(item.tabTrigger)
        return tabTriggers
            
    def getAllBundleItemsByTabTrigger(self, tabTrigger):
        items = []
        for item in self.actionItemsProxyModel.getAllItems():
            if item.tabTrigger == tabTrigger:
                items.append(item)
        return items
            
    #---------------------------------------------------
    # KEYEQUIVALENT OVERRIDE INTERFACE
    #---------------------------------------------------
    def getAllBundleItemsByKeyEquivalent(self, keyEquivalent):
        items = []
        for item in self.actionItemsProxyModel.getAllItems():
            if item.keyEquivalent == keyEquivalent:
                items.append(item)
        for syntax in self.syntaxProxyModel.getAllItems():
            if syntax.keyEquivalent == keyEquivalent:
                items.append(syntax)
        return items
    
    #---------------------------------------------------
    # FILE EXTENSION OVERRIDE INTERFACE
    #---------------------------------------------------
    def getAllBundleItemsByFileExtension(self, path):
        items = []
        for item in self.dragcommandProxyModel.getAllItems():
            if any(map(lambda extension: fnmatch.fnmatch(path, "*.%s" % extension), item.draggedFileExtensions)):
                items.append(item)
        return items
    
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