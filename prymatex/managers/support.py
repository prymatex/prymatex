#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import fnmatch
from bisect import bisect
import uuid as uuidmodule

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.qt.helpers import rgba2color

from prymatex.core import PrymatexComponent
from prymatex.core.settings import ConfigurableItem

from prymatex.support.manager import SupportBaseManager
from prymatex.support.process import RunningContext
from prymatex.support.bundleitem.theme import DEFAULT_THEME_SETTINGS

from prymatex.utils import encoding

from prymatex.models.process import ExternalProcessTableModel
from prymatex.models.support import (BundleItemTreeModel, BundleItemTreeNode,
    ThemeStylesTableModel, ThemeStyleTableRow)
from prymatex.models.support import (BundleItemProxyTreeModel, BundleItemTypeProxyModel, 
    ThemeStyleProxyTableModel, BundleListModel, SyntaxListModel,
    TemplateListModel, ProjectListModel)

class BundleItemMenuGroup(QtCore.QObject):
    def __init__(self, manager):
        QtCore.QObject.__init__(self, manager)
        self.manager = manager
        #The bundle menues
        self.menus = {}
        #The qt menus where a bundle menu is added
        self.containers = []
        self.manager.bundlePopulated.connect(self.on_manager_bundlePopulated)
        self.manager.bundleAdded.connect(self.on_manager_bundleAdded)
        self.manager.bundleItemChanged.connect(self.on_manager_bundleItemChanged)
        self.manager.bundleChanged.connect(self.on_manager_bundleChanged)
        self.manager.bundleRemoved.connect(self.on_manager_bundleRemoved)
        
    def appendMenu(self, menu, offset = None):
        if menu not in [menu_offset[0] for menu_offset in self.containers]:
            self.containers.append((menu, offset is not None and offset or len(menu.actions())))
        #Append all bundle menus in order
        for bundle, bundleMenu in iter(sorted(iter(self.menus.items()), key=lambda bundle_bundleMenu: bundle_bundleMenu[1].title().replace("&","").lower())):
            menu.addMenu(bundleMenu)

    def buildMenu(self, items, menu, submenus, parent = None):
        for uuid in items:
            if uuid.startswith('-'):
                menu.addSeparator()
                continue
            item = self.manager.getBundleItem(uuid)
            if item is not None:
                action = item.triggerItemAction(parent)
                menu.addAction(action)
            elif uuid in submenus:
                submenu = QtWidgets.QMenu(submenus[uuid]['name'], parent)
                
                #Conectamos el about to show para filtar un poco los items cuando se muestra el menu
                submenu.aboutToShow.connect(self.on_bundleMenu_aboutToShow)
                
                menu.addMenu(submenu)
                self.buildMenu(submenus[uuid]['items'], submenu, submenus, parent)

    def buildBundleMenu(self, bundle):
        menu = QtWidgets.QMenu(bundle.buildBundleAccelerator())
        menu.ID = id(bundle.bundleItem().mainMenu)
        
        #Conectamos el about to show para filtar un poco los items cuando se muestra el menu
        menu.aboutToShow.connect(self.on_bundleMenu_aboutToShow)
        return menu

    def addBundle(self, bundle):
        """
            Add bundle to menu collection, all bundle has one QMenu in the collection
        """
        menu = self.buildBundleMenu(bundle)
        menu.menuAction().setVisible(bundle.enabled and bundle.bundleItem().mainMenu is not None)
        # Primero agregarlo a los containers porque estos usan self.menus para ordenar
        self.addToContainers(menu)
        self.menus[bundle.uuid()] = menu

    def menuForBundle(self, bundle):
        return self.menus.get(bundle.uuid())

    def addToContainers(self, menu):
        currentTitles = sorted([menu.title().replace("&","").lower() for menu in list(self.menus.values())])
        index = bisect(currentTitles, menu.title().replace("&","").lower())
        for container, offset in self.containers:
            currentActions = container.actions()
            if index < len(currentActions) - offset:
                container.insertMenu(currentActions[offset + index], menu)
            else:
                container.addMenu(menu)

    def removeFromContainers(self, menu):
        for container, offset in self.containers:
            container.removeAction(menu.menuAction())

    def on_bundleMenu_aboutToShow(self):
        menu = self.sender()
        for action in menu.actions():
            if hasattr(action, "bundleTreeNode"):
                action.setDisabled(action.bundleTreeNode.isEditorNeeded() and not self.manager.editorAvailable)
            
    def on_manager_bundleItemChanged(self, item):
        action = item.triggerItemAction()
        if action is not None:
            text = item.buildMenuTextEntry()
            if text != action.text():
                action.setText(text)
                
    def on_manager_bundleChanged(self, bundle):
        menu = self.menus[bundle.uuid()]
        title = bundle.buildBundleAccelerator()
        if title != menu.title():
            self.removeFromContainers(menu)
            menu.setTitle(title)
            self.addToContainers(menu)
        if bundle.enabled != menu.menuAction().isVisible():
            menu.menuAction().setVisible(bundle.enabled and bundle.bundleItem().mainMenu is not None)
        if id(bundle.bundleItem().mainMenu) != menu.ID:
            # TODO Ver si no tengo que desconectar las señales de los submenues
            menu.clear()
            submenus = bundle.bundleItem().mainMenu['submenus'] if bundle.bundleItem().mainMenu is not None and 'submenus' in bundle.bundleItem().mainMenu else {}
            items = bundle.bundleItem().mainMenu['items'] if 'items' in bundle.bundleItem().mainMenu else []
            self.buildMenu(items, menu, submenus, menu)
            menu.ID = id(bundle.bundleItem().mainMenu)

    def on_manager_bundleAdded(self, bundle):
        assert bundle not in self.menus, "The bundle is in menus"
        self.addBundle(bundle)

    def on_manager_bundlePopulated(self, bundle):
        menu = self.menus[bundle.uuid()]
        menu.clear()
        if bundle.bundleItem().mainMenu is not None:
            submenus = bundle.bundleItem().mainMenu['submenus'] if 'submenus' in bundle.bundleItem().mainMenu else {}
            items = bundle.bundleItem().mainMenu['items'] if 'items' in bundle.bundleItem().mainMenu else []
            self.buildMenu(items, menu, submenus, menu)

    def on_manager_bundleRemoved(self, bundle):
        self.removeFromContainers(self.menus[bundle.uuid()])

class Properties(QtCore.QObject):
    def __init__(self, properties):
        """docstring for __init__"""
        self._properties = properties
    
class SupportManager(PrymatexComponent, SupportBaseManager, QtCore.QObject):
    # Signals for bundle
    bundleAdded = QtCore.Signal(object)
    bundleRemoved = QtCore.Signal(object)
    bundleChanged = QtCore.Signal(object)
    bundlePopulated = QtCore.Signal(object)

    # Signals for bundle items
    bundleItemAdded = QtCore.Signal(object)
    bundleItemRemoved = QtCore.Signal(object)
    bundleItemChanged = QtCore.Signal(object)
    bundleItemTriggered = QtCore.Signal(object)
    
    # Signals for themes
    themeAdded = QtCore.Signal(object)
    themeRemoved = QtCore.Signal(object)
    themeChanged = QtCore.Signal(object)
    
    # Signals for properties
    propertiesChanged = QtCore.Signal(str)
    
    # ------------- Settings
    shell_variables = ConfigurableItem(default=[], tm_name='OakShelVariables')
    
    # TODO: Mejores nombres por aca
    @ConfigurableItem(default=[], tm_name='OakBundleManagerDeletedBundles')
    def deleted(self, deleted):
        self.deletedObjects = [uuidmodule.UUID(uuid) for uuid in deleted]
        
    @ConfigurableItem(default=[], tm_name='OakBundleManagerDeletedBundles')
    def disabled(self, disabled):
        self.disabledObjects = [uuidmodule.UUID(uuid) for uuid in disabled]
    
    #http://manual.macromates.com/en/expert_preferences.html
    #When you create a new item in the bundle editor without having selected a bundle first, then the bundle with the UUID held by this defaults key is used as the target
    default_bundle_for_new_bundle_items = ConfigurableItem(default = 'B7BC3FFD-6E4B-11D9-91AF-000D93589AF6', tm_name = 'OakDefaultBundleForNewBundleItems')
    
    def __init__(self, **kwargs):
        super(SupportManager, self).__init__(**kwargs)

        self.bundleTreeModel = BundleItemTreeModel(self)
        self.themeStylesTableModel = ThemeStylesTableModel(self)
        self.processTableModel = ExternalProcessTableModel(self)

        #STYLE PROXY
        self.themeStyleProxyModel = ThemeStyleProxyTableModel(self)
        self.themeStyleProxyModel.setSourceModel(self.themeStylesTableModel)

        #TREE PROXY
        self.bundleProxyTreeModel = BundleItemProxyTreeModel(self)
        self.bundleProxyTreeModel.setSourceModel(self.bundleTreeModel)

        #BUNDLES
        self.bundleProxyModel = BundleListModel(self)
        self.bundleProxyModel.setSourceModel(self.bundleTreeModel)
        
        #TEMPLATES
        self.templateProxyModel = TemplateListModel(self)
        self.templateProxyModel.setSourceModel(self.bundleTreeModel)
        
        #PROJECTS
        self.projectProxyModel = ProjectListModel(self)
        self.projectProxyModel.setSourceModel(self.bundleTreeModel)

        #SYNTAX
        self.syntaxProxyModel = SyntaxListModel(self)
        self.syntaxProxyModel.setSourceModel(self.bundleTreeModel)
        
        #INTERACTIVEITEMS
        self.actionItemsProxyModel = BundleItemTypeProxyModel(["command", "snippet", "macro"], self)
        self.actionItemsProxyModel.setSourceModel(self.bundleTreeModel)
        
        #PREFERENCES
        self.preferenceProxyModel = BundleItemTypeProxyModel("preference", self)
        self.preferenceProxyModel.setSourceModel(self.bundleTreeModel)
        
        #DRAGCOMMANDS
        self.dragcommandProxyModel = BundleItemTypeProxyModel("dragcommand", self)
        self.dragcommandProxyModel.setSourceModel(self.bundleTreeModel)
        
        #THEMES
        self.themeProxyModel = BundleItemTypeProxyModel("theme", self)
        self.themeProxyModel.setSourceModel(self.bundleTreeModel)
        
        #BUNDLEMENUGROUP
        self.bundleMenuGroup = BundleItemMenuGroup(self)
        
        # File System Watcher
        self.fileSystemWatcher = QtCore.QFileSystemWatcher()
        self.fileSystemWatcher.directoryChanged.connect(
            self.on_fileSystemWatcher_pathChanged
        )
        self.fileSystemWatcher.fileChanged.connect(
            self.on_fileSystemWatcher_pathChanged
        )

    @classmethod
    def contributeToSettings(cls):
        from prymatex.gui.settings.environment import VariablesSettingsWidget
        return [ VariablesSettingsWidget ]

    def setEditorAvailable(self, available):
        self.editorAvailable = available

    def appendMenuToBundleMenuGroup(self, menu, offset = None):
        self.bundleMenuGroup.appendMenu(menu, offset)

    def menuForBundle(self, bundle):
        return self.bundleMenuGroup.menuForBundle(bundle)

    # OVERRIDE: SupportManager.namespace
    def namespace(self, name):
        return self.application().namespace(name)

    # OVERRIDE: SupportManager.namespaces
    def namespaces(self):
        return self.application().namespaces()

    # OVERRIDE: SupportManager.protectedNamespace()
    def protectedNamespace(self):
        return self.application().protectedNamespace()

    # Override buildPlistFileStorage for custom storage
    def buildPlistFileStorage(self):
        return self.application().storageManager.singleFileStorage("support-plist")
        
    def buildBundleItemStorage(self):
        return SupportBaseManager.buildBundleItemStorage(self)
    
    # ------------------- Signals
    def on_fileSystemWatcher_pathChanged(self, path):
        directory = path if os.path.isdir(path) else os.path.dirname(path)
        if self.propertiesHasChanged(directory):
            self.logger().debug("Properties in %s has changed" % directory)
            remove = self.updateProperties(directory)
            self.fileSystemWatcher.removePath(remove)
            self.propertiesChanged.emit(directory)

    #---------------------------------------------------
    # Environment
    #---------------------------------------------------
    def environmentVariables(self):
        environment = SupportBaseManager.environmentVariables(self)
        #Extend wiht the user shell variables
        for var in self.shell_variables:
            if var['enabled']:
                environment[var['variable']] = var['value']
        return environment

    def loadSupport(self, message_handler):
        self.bundleProxyTreeModel.setDynamicSortFilter(True)
        SupportBaseManager.loadSupport(self, message_handler)
        #self.bundleProxyTreeModel.sort(0, QtCore.Qt.AscendingOrder)

    def runSystemCommand(self, **attrs):
        if attrs.get("asynchronous", False):
            return self.runQtProcessCommand(**attrs)
        else:
            return SupportBaseManager.runSystemCommand(self, **attrs)

    #Interface
    def runQtProcessCommand(self, **attrs):
        context = RunningContext(**attrs)
        
        context.process = QtCore.QProcess(self)
        if context.workingDirectory is not None:
            context.process.setWorkingDirectory(context.workingDirectory)
            
        self.processTableModel.appendProcess(context.process, description = context.description())

        environment = QtCore.QProcessEnvironment()
        for key, value in context.scriptFileEnvironment.items():
            environment.insert(key, value)

        context.process.setProcessEnvironment(environment)

        def onQProcessFinished(context):
            def _finished(exitCode, exitStatus):
                self.processTableModel.removeProcess(context.process)
                errorValue = context.process.readAllStandardError().data()
                context.errorValue = encoding.from_fs(
                    context.process.readAllStandardError().data()
                )
                context.outputValue = encoding.from_fs(
                    context.process.readAllStandardOutput().data()
                )
                context.outputType = exitCode
                context.callback(context)
            return _finished

        context.process.finished[int, QtCore.QProcess.ExitStatus].connect(
            onQProcessFinished(context)
        )
        
        def onQProcessStarted(context):
            def _started():
                if context.inputValue is not None:
                    context.process.write(encoding.to_fs(context.inputValue))
                context.process.closeWriteChannel()
            return _started
        
        context.process.started.connect(onQProcessStarted(context))
        
        context.process.start(context.scriptFilePath)
        
        return context

    def buildAdHocCommand(self, *largs, **kwargs):
        return BundleItemTreeNode(SupportBaseManager.buildAdHocCommand(self, *largs, **kwargs))

    def buildAdHocSnippet(self, *largs, **kwargs):
        return BundleItemTreeNode(SupportBaseManager.buildAdHocSnippet(self, *largs, **kwargs))

    #---------------------------------------------------
    # MANAGED OBJECTS OVERRIDE INTERFACE
    #---------------------------------------------------
    def setDeleted(self, uuid):
        """
        Marcar un managed object como eliminado
        """
        self.deletedObjects.append(uuid)
        deleted = [str(uuid).upper() for uuid in self.deletedObjects]
        self.settings().setValue('deleted', deleted)

    def isDeleted(self, uuid):
        return uuid in self.deletedObjects

    def isEnabled(self, uuid):
        return uuid not in self.disabledObjects
    
    def setDisabled(self, uuid):
        self.disabledObjects.append(uuid)
        disabled = [str(uuid).upper() for uuid in self.disabledObjects]
        self.settings().setValue('disabled', disabled)
        
    def setEnabled(self, uuid):
        self.disabledObjects.remove(uuid)
        disabled = [str(uuid).upper() for uuid in self.disabledObjects]
        self.settings().setValue('disabled', disabled)
    
    #---------------------------------------------------
    # BUNDLE OVERRIDE INTERFACE 
    #---------------------------------------------------
    def getBundle(self, uuid):
        indexes = self.bundleTreeModel.match(self.bundleTreeModel.index(0, 0, QtCore.QModelIndex()), 
            QtCore.Qt.UUIDRole, uuid, 1, QtCore.Qt.MatchFixedString | QtCore.Qt.MatchRecursive)
        if indexes:
            return self.bundleTreeModel.node(indexes[0])

    def addBundle(self, bundle):
        bundle_node = BundleItemTreeNode(bundle)
        icon = self.resources().get_icon("bundle-item-%s" % bundle.type())
        bundle_node.setIcon(icon)
        self.bundleTreeModel.appendBundle(bundle_node)
        self.bundleAdded.emit(bundle_node)
    
    def modifyBundle(self, bundle):
        self.bundleChanged.emit(bundle)
    
    def removeBundle(self, bundle):
        self.bundleTreeModel.removeBundle(bundle)
        self.bundleRemoved.emit(bundle)
    
    def getAllBundles(self):
        return self.bundleProxyModel.nodes()
    
    def getDefaultBundle(self):
        return self.getBundle(self.defaultBundleForNewBundleItems)
    
    def populatedBundle(self, bundle):
        bundle_node = self.getBundle(bundle.uuid)
        if bundle_node is not None:
            self.bundlePopulated.emit(bundle_node)
        
    #---------------------------------------------------
    # BUNDLEITEM OVERRIDE INTERFACE 
    #---------------------------------------------------
    def getBundleItem(self, uuid):
        indexes = self.bundleTreeModel.match(self.bundleTreeModel.index(0, 0, QtCore.QModelIndex()),
            QtCore.Qt.UUIDRole, uuid, 1, QtCore.Qt.MatchFixedString | QtCore.Qt.MatchRecursive)
        if indexes:
            return self.bundleTreeModel.node(indexes[0])

    def addBundleItem(self, bundle_item):
        bundle_item_node = BundleItemTreeNode(bundle_item)
        bundle_node = self.getBundle(bundle_item.bundle.uuid)
        icon = self.resources().get_icon("bundle-item-%s" % bundle_item.type())
        bundle_item_node.setIcon(icon)
        self.bundleTreeModel.appendBundleItem(bundle_item_node, bundle_node)
        self.bundleItemAdded.emit(bundle_item_node)

    def modifyBundleItem(self, bundleItem):
        self.bundleItemChanged.emit(bundleItem)
        
    def removeBundleItem(self, bundleItem):
        self.bundleTreeModel.removeBundleItem(bundleItem)
        self.bundleItemRemoved.emit(bundleItem)
        
    def getAllBundleItems(self):
        nodes = []
        for bundle in self.getAllBundles():
            for node in bundle.children():
                nodes.append(node)
        return nodes

        # ----------------- THEME OVERRIDE INTERFACE
    def getThemePalette(self, theme, scope=None):
        settings = self.getThemeSettings(theme, scope)
        palette = self.application().palette()
        if 'foreground' in settings:
            #QPalette::Foreground	0	This value is obsolete. Use WindowText instead.
            palette.setColor(QtGui.QPalette.Foreground, rgba2color(settings['background']))
            #QPalette::WindowText	0	A general foreground color.
            palette.setColor(QtGui.QPalette.WindowText, rgba2color(settings['foreground']))
            #QPalette::Text	6	The foreground color used with Base. This is usually the same as the WindowText, in which case it must provide good contrast with Window and Base.
            palette.setColor(QtGui.QPalette.Text, rgba2color(settings['foreground']))
            #QPalette::ToolTipText	19	Used as the foreground color for QToolTip and QWhatsThis. Tool tips use the Inactive color group of QPalette, because tool tips are not active windows.
            palette.setColor(QtGui.QPalette.ToolTipText, rgba2color(settings['foreground']))
            #QPalette::ButtonText	    8	A foreground color used with the Button color.
            palette.setColor(QtGui.QPalette.ButtonText, rgba2color(settings['foreground']))
        if 'background' in settings:
            #QPalette::Background	10	This value is obsolete. Use Window instead.
            palette.setColor(QtGui.QPalette.Background, rgba2color(settings['background']))
            #QPalette::Window	10	A general background color.
            palette.setColor(QtGui.QPalette.Window, rgba2color(settings['background']))
            #QPalette::Base	9	Used mostly as the background color for text entry widgets, but can also be used for other painting - such as the background of combobox drop down lists and toolbar handles. It is usually white or another light color.
            palette.setColor(QtGui.QPalette.Base, rgba2color(settings['background']))
            #QPalette::ToolTipBase	18	Used as the background color for QToolTip and QWhatsThis. Tool tips use the Inactive color group of QPalette, because tool tips are not active windows.
            palette.setColor(QtGui.QPalette.ToolTipBase, rgba2color(settings['background']))
            #QPalette::Button	    1	The general button background color. This background can be different from Window as some styles require a different background color for buttons.
            palette.setColor(QtGui.QPalette.Button, rgba2color(settings['background']))
        if 'selection' in settings:
            #QPalette::Highlight	12	A color to indicate a selected item or the current item. By default, the highlight color is Qt::darkBlue.
            palette.setColor(QtGui.QPalette.Highlight, rgba2color(settings['selection']))
        if 'invisibles' in settings:
            #QPalette::LinkVisited	15	A text color used for already visited hyperlinks. By default, the linkvisited color is Qt::magenta.
            palette.setColor(QtGui.QPalette.LinkVisited, rgba2color(settings['invisibles']))
        if 'lineHighlight' in settings:
            #QPalette::AlternateBase	16	Used as the alternate background color in views with alternating row colors (see QAbstractItemView::setAlternatingRowColors()).
            palette.setColor(QtGui.QPalette.AlternateBase, rgba2color(settings['lineHighlight']))
        if 'caret' in settings:
            #QPalette::BrightText	7	A text color that is very different from WindowText, and contrasts well with e.g. Dark. Typically used for text that needs to be drawn where Text or WindowText would give poor contrast, such as on pressed push buttons. Note that text colors can be used for things other than just words; text colors are usually used for text, but it's quite common to use the text color roles for lines, icons, etc.
            palette.setColor(QtGui.QPalette.BrightText, rgba2color(settings['caret']))
            #QPalette::HighlightedText	13	A text color that contrasts with Highlight. By default, the highlighted text color is Qt::white.
            palette.setColor(QtGui.QPalette.HighlightedText, rgba2color(settings['caret']))
        if 'gutterBackground' in settings and settings['gutterBackground'] != DEFAULT_THEME_SETTINGS['gutterBackground']:
            #QPalette::ToolTipBase	18	Used as the background color for QToolTip and QWhatsThis. Tool tips use the Inactive color group of QPalette, because tool tips are not active windows.
            palette.setColor(QtGui.QPalette.ToolTipBase, rgba2color(settings['gutterBackground']))
        if 'gutterForeground' in settings and settings['gutterForeground'] != DEFAULT_THEME_SETTINGS['gutterForeground']:
            #QPalette::ToolTipText	19	Used as the foreground color for QToolTip and QWhatsThis. Tool tips use the Inactive color group of QPalette, because tool tips are not active windows.
            palette.setColor(QtGui.QPalette.ToolTipText, rgba2color(settings['gutterForeground']))
        #QPalette::Link	14	A text color used for unvisited hyperlinks. By default, the link color is Qt::blue.
        return palette
        
    def getThemeTextCharFormat(self, theme, scope=None):
        settings = self.getThemeSettings(theme, scope)
        frmt = QtGui.QTextCharFormat()
        if 'foreground' in settings:
            frmt.setForeground(rgba2color(settings['foreground']))
        if 'background' in settings:
            frmt.setBackground(rgba2color(settings['background']))
        if 'fontStyle' in settings:
            if 'bold' in settings['fontStyle']:
                frmt.setFontWeight(QtGui.QFont.Bold)
            if 'underline' in settings['fontStyle']:
                frmt.setFontUnderline(True)
            if 'italic' in settings['fontStyle']:
                frmt.setFontItalic(True)
        return frmt

    # --------------- PROPERTIES OVERRIDE INTERFACE
    def addProperties(self, properties):
        watch = [ cfg.source.exists() and cfg.source.path or cfg.source.name for cfg in properties.configs]
        self.fileSystemWatcher.addPaths(watch)
        return properties
        
    #---------------------------------------------------
    # STATICFILE OVERRIDE INTERFACE
    #---------------------------------------------------
    def addStaticFile(self, static_file):
        static_file_node = BundleItemTreeNode(static_file)
        bundle_item_node = self.getBundleItem(static_file.parentItem.uuid)
        self.bundleTreeModel.appendStaticFile(static_file_node, bundle_item_node)
    
    def removeStaticFile(self, file):
        pass

    #---------------------------------------------------
    # THEME STYLE OVERRIDE INTERFACE
    #---------------------------------------------------
    def getThemeStyle(self, uuid):
        indexes = self.themeStylesTableModel.match(self.bundleTreeModel.index(0, 0, QtCore.QModelIndex()),
            QtCore.Qt.UUIDRole, uuid, 1, QtCore.Qt.MatchFixedString | QtCore.Qt.MatchRecursive)
        if indexes:
            return self.themeStylesTableModel.style(indexes[0])

    def addThemeStyle(self, style):
        theme_style = ThemeStyleTableRow(style)
        self.themeStylesTableModel.appendStyle(theme_style)
        return style

    def removeThemeStyle(self, style):
        self.themeStylesTableModel.removeStyle(style)

    #---------------------------------------------------
    # PREFERENCES INTERFACE
    #---------------------------------------------------
    def getAllPreferencesNodes(self):
        memoizedKey = ("getAllPreferences", None, None, None)
        if memoizedKey in self.bundleItemCache:
            return self.bundleItemCache.get(memoizedKey)
        return self.bundleItemCache.setdefault(memoizedKey,
            list(self.preferenceProxyModel.nodes()))

    #---------------------------------------------------
    # TABTRIGGERS OVERRIDE INTERFACE
    #---------------------------------------------------
    def getAllTabTriggerItemsNodes(self):
        memoizedKey = ("getAllTabTriggerItems", None, None, None)
        if memoizedKey in self.bundleItemCache:
            return self.bundleItemCache.get(memoizedKey)
        tabTriggers = []
        for item in self.actionItemsProxyModel.nodes():
            if item.tabTrigger is not None:
                tabTriggers.append(item)
        return self.bundleItemCache.setdefault(memoizedKey,
            tabTriggers)
        
    def getAllBundleItemsNodesByTabTrigger(self, tabTrigger):
        memoizedKey = ("getAllBundleItemsByTabTrigger", tabTrigger, None, None)
        if memoizedKey in self.bundleItemCache:
            return self.bundleItemCache.get(memoizedKey)
        items = []
        for item in self.actionItemsProxyModel.nodes():
            if item.tabTrigger == tabTrigger:
                items.append(item)
        return self.bundleItemCache.setdefault(memoizedKey,
            items)

    #---------------------------------------------------
    # KEYEQUIVALENT OVERRIDE INTERFACE
    #---------------------------------------------------
    def getAllKeyEquivalentItemsNodes(self):
        memoizedKey = ("getAllKeyEquivalentItems", None, None, None)
        if memoizedKey in self.bundleItemCache:
            return self.bundleItemCache[memoizedKey]
        keyCode = []
        for item in self.actionItemsProxyModel.nodes():
            if item.keyCode() is not None:
                keyCode.append(item)
        for item in self.syntaxProxyModel.nodes():
            if item.keyCode() is not None:
                keyCode.append(item)
        return self.bundleItemCache.setdefault(memoizedKey,
            keyCode)
        
    def getAllBundleItemsNodesByKeyEquivalent(self, keyCode):
        memoizedKey = ("getAllBundleItemsByKeyEquivalent", "%s" % keyCode, None, None)
        if memoizedKey in self.bundleItemCache:
            return self.bundleItemCache.get(memoizedKey)
        items = []
        for item in self.actionItemsProxyModel.nodes():
            if item.keyCode() == keyCode:
                items.append(item)
        for syntax in self.syntaxProxyModel.nodes():
            if syntax.keyCode() == keyCode:
                items.append(syntax)
        return self.bundleItemCache.setdefault(memoizedKey,
            items)
    
    #---------------------------------------------------
    # FILE EXTENSION OVERRIDE INTERFACE
    #---------------------------------------------------
    def getAllBundleItemsNodesByFileExtension(self, path):
        items = []
        for item in self.dragcommandProxyModel.nodes():
            if any([fnmatch.fnmatch(path, "*.%s" % extension) for extension in item.draggedFileExtensions]):
                items.append(item)
        return items
    
    #---------------------------------------------------
    # ACTION ITEMS INTERFACE
    #---------------------------------------------------
    def getAllActionItemsNodes(self):
        return self.actionItemsProxyModel.nodes()
    
    #---------------------------------------------------
    # SYNTAXES INTERFACE
    #---------------------------------------------------
    def getAllSyntaxesNodes(self):
        return self.syntaxProxyModel.nodes()

    #---------------------------------------------------
    # CURSOR SCOPE
    #---------------------------------------------------
    def cursorScope(self, cursor):
        left_scope = self.scopeFactory("")
        right_scope = self.scopeFactory("")
        leftCursor = QtGui.QTextCursor(cursor)
        rightCursor = QtGui.QTextCursor(cursor)
        leftCursor.setPosition(cursor.selectionStart())
        rightCursor.setPosition(cursor.selectionEnd())
        if cursor.hasSelection():
            # If there is one or more selections: dyn.selection.
            # TODO If there is a single zero-width selection: dyn.caret.mixed.columnar.
            # TODO If there are multiple carets and/or selections: dyn.caret.mixed.
            left_scope.push_scope("dyn.selection")
            right_scope.push_scope("dyn.selection")
        # When there is only a single caret or a single continuous selection
        # the left scope may contain: dyn.caret.begin.line or dyn.caret.begin.document
        if leftCursor.atBlockStart():
            left_scope.push_scope("dyn.caret.begin.line")
        if leftCursor.atStart():
            left_scope.push_scope("dyn.caret.begin.document")
        # Likewise the right scope may contain: dyn.caret.end.line or dyn.caret.end.document.
        if rightCursor.atBlockEnd():
            right_scope.push_scope("dyn.caret.end.line")
        if rightCursor.atEnd():
            right_scope.push_scope("dyn.caret.end.document")
        return left_scope, right_scope
