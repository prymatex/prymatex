#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex import resources
from prymatex.models.tree import TreeNode, TreeModel
from prymatex.models.mimes import PyMimeData
from prymatex.gui.support import qtadapter

#====================================================
# Bundle Tree Node
#====================================================
class PMXBundleTreeNode(TreeNode):
    """Bundle and bundle item decorator"""
    USED = []
    BANNED_ACCEL = ' \t'
    
    def __init__(self, item, parent = None):
        TreeNode.__init__(self, item.name, parent)
        self.item = item

    def __getattr__(self, name):
        return getattr(self.item, name)
    
    #==================================================
    # Item decoration
    #==================================================
    @property
    def keyEquivalent(self):
        if self.item.keyEquivalent is not None:
            return qtadapter.buildKeySequence(self.item.keyEquivalent)
    
    @property
    def icon(self):
        return resources.getIcon(self.TYPE)
    
    @property
    def trigger(self):
        trigger = []
        if self.tabTrigger != None:
            trigger.append(u"%s⇥" % (self.tabTrigger))
        if self.keyEquivalent != None:
            trigger.append(u"%s" % QtGui.QKeySequence(self.keyEquivalent).toString())
        return ", ".join(trigger)
    
    def buildBundleAccelerator(self):
        name = unicode(self.name)
        for index, char in enumerate(name):
            if char in self.BANNED_ACCEL:
                continue
            char = char.lower()
            if not char in self.USED:
                self.USED.append(char)
                return name[0:index] + '&' + name[index:]
        return name
    
    def buildMenuTextEntry(self, mnemonic = True):
        text = unicode(self.name)
        if mnemonic:
            text += u"\t%s" % (self.trigger)
        return text.replace('&', '&&')
    
    def triggerItemAction(self, parent = None):
        """
        Build and return de QAction related to this bundle item.
        if bundle item haven't action is created whit the given parent, otherwise return None
        """
        if parent is not None:
            receiver = lambda item = self: item.manager.bundleItemTriggered.emit(item)
            self.action = self.buildTriggerItemAction(parent, receiver)
            return self.action
        elif hasattr(self, "action"):
            return self.action
    
    def buildTriggerItemAction(self, parent, receiver):
        action = QtGui.QAction(self.icon, self.buildMenuTextEntry(), parent)
        parent.connect(action, QtCore.SIGNAL('triggered()'), receiver)
        return action
    
    def update(self, hash):
        if 'keyEquivalent' in hash:
            hash['keyEquivalent'] = qtadapter.buildKeyEquivalent(hash['keyEquivalent'])
        self.item.update(hash)

#====================================================
# Bundle Tree Model
#====================================================
class PMXBundleTreeModel(TreeModel): 
    def __init__(self, manager, parent = None):
        TreeModel.__init__(self, parent)
        self.manager = manager
        self.manager.bundleChanged.connect(self.on_manager_bundleItemChanged)
        self.manager.bundleItemChanged.connect(self.on_manager_bundleItemChanged)
    
    def on_manager_bundleItemChanged(self, treeNode):
        treeNode.name = treeNode.item.name
        index = self.createIndex(treeNode.row(), 0, treeNode)
        self.dataChanged.emit(index, index)
    
    def setData(self, index, value, role):  
        if not index.isValid():  
            return False
        elif role == QtCore.Qt.CheckStateRole:
            node = self.node(index)
            if node.TYPE == "bundle":
                self.manager.disableBundle(node, not value)
            self.dataChanged.emit(index, index)
            return True
        return False
    
    def data(self, index, role):  
        if not index.isValid():  
            return None
        elif role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            node = self.node(index)
            return node.name
        elif role == QtCore.Qt.DecorationRole:
            node = self.node(index)
            return node.icon

    def flags(self, index):
        if not index.isValid():  
            return QtCore.Qt.NoItemFlags  
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    def removeRows(self, position = 0, count = 1,  parent=QtCore.QModelIndex()):
        node = self.node(parent)
        self.beginRemoveRows(parent, position, position + count - 1)  
        node.childrenNodes.pop(position)  
        self.endRemoveRows()

    #========================================================================
    # Functions
    #========================================================================
    def appendBundle(self, bundle):
        self.beginInsertRows(QtCore.QModelIndex(), self.rootNode.childCount(), self.rootNode.childCount())
        self.rootNode.appendChild(bundle)
        self.endInsertRows()
    
    def removeBundle(self, bundle):
        self.beginRemoveRows(QtCore.QModelIndex(), bundle.row(), bundle.row())
        self.rootNode.removeChild(bundle)
        self.endRemoveRows()
    
    def appendBundleItem(self, bundleItem):
        bundle = bundleItem.bundle
        pindex = self.createIndex(bundle.row(), 0, bundle)
        self.beginInsertRows(pindex, bundle.childCount(), bundle.childCount())
        bundle.appendChild(bundleItem)
        self.endInsertRows()
    
    def removeBundleItem(self, bundleItem):
        bundle = bundleItem.bundle
        pindex = self.createIndex(bundle.row(), 0, bundle)
        self.beginRemoveRows(pindex, bundle.row(), bundle.row())
        bundle.removeChild(bundleItem)
        self.endRemoveRows()
    
    def appendTemplateFile(self, templateFile):
        template = templateFile.template
        pindex = self.createIndex(template.row(), 0, template)
        self.beginInsertRows(pindex, template.childCount(), template.childCount())
        template.appendChild(templateFile)
        self.endInsertRows()

    def removeTemplateFile(self, templateFile):
        template = templateFile.template
        pindex = self.createIndex(template.row(), 0, template)
        self.beginRemoveRows(pindex, template.row(), template.row())
        template.removeChild(templateFile)
        self.endRemoveRows()
        
#====================================================
# Themes Styles Row
#====================================================
class PMXThemeStyleRow(object):
    """Theme and Style decorator"""
    def __init__(self, item, scores = None):
        self.item = item
        self.scores = scores
        self.STYLES_CACHE = {}
    
    def __getattr__(self, name):
        return getattr(self.item, name)
    
    @property
    def settings(self):
        settings = {}
        for color_key in ['foreground', 'background', 'selection', 'invisibles', 'lineHighlight', 'caret', 'gutter']:
            if color_key in self.item.settings and self.item.settings[color_key]:
                color = qtadapter.RGBA2QColor(self.item.settings[color_key])
                settings[color_key] = color
        settings['fontStyle'] = self.item.settings['fontStyle'].split() if 'fontStyle' in self.item.settings else []
        return settings
    
    def update(self, hash):
        if 'settings' in hash:
            settings = {}
            for key in hash['settings'].keys():
                if key in ['foreground', 'background', 'selection', 'invisibles', 'lineHighlight', 'caret', 'gutter']:
                    settings[key] = qtadapter.QColor2RGBA(hash['settings'][key])
            if 'fontStyle' in hash['settings']:
                settings['fontStyle'] = " ".join(hash['settings']['fontStyle'])
            hash['settings'] = settings
        self.item.update(hash)
    
    def clearCache(self):
        self.STYLES_CACHE = {}

    def getStyle(self, scope = None):
        if scope in self.STYLES_CACHE:
            return self.STYLES_CACHE[scope]
        base = {}
        base.update(self.settings)
        if scope == None:
            return base
        styles = []
        for style in self.styles:
            if style.scope != None:
                score = self.scores.score(style.scope, scope)
                if score != 0:
                    styles.append((score, style))
        styles.sort(key = lambda t: t[0])
        for score, style in styles:
            base.update(style.settings)
        self.STYLES_CACHE[scope] = base
        return base

#====================================================
# Themes Style Table Model
#====================================================
class PMXThemeStylesTableModel(QtCore.QAbstractTableModel):
    def __init__(self, manager, parent = None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.manager = manager
        self.styles = []
        self.headers = ['Element', 'Fg', 'Bg', 'Font Style']
        
    def rowCount(self, parent):
        return len(self.styles)
    
    def columnCount(self, parent):
        return 4
    
    def data(self, index, role):
        if not index.isValid(): 
            return QtCore.QVariant() 
        if role in [ QtCore.Qt.DisplayRole, QtCore.Qt.EditRole ]:
            row = index.row()
            column = index.column()
            style = self.styles[row]
            settings = self.styles[row].settings
            if column == 0:
                return style.name
            elif column == 1 and 'foreground' in settings:
                return settings['foreground']
            elif column == 2 and 'background' in settings:
                return settings['background']
            elif column == 3 and 'fontStyle' in settings:
                return settings['fontStyle']
        elif role == QtCore.Qt.FontRole:
            row = index.row()
            column = index.column()
            style = self.styles[row]
            settings = self.styles[row].settings
            if column == 0:
                font = QtGui.QFont()
                if 'bold' in settings['fontStyle']:
                    font.setBold(True)
                if 'underline' in settings['fontStyle']:
                    font.setUnderline(True)
                if 'italic' in settings['fontStyle']:
                    font.setItalic(True)
                return font
        elif role == QtCore.Qt.ForegroundRole:
            row = index.row()
            column = index.column()
            style = self.styles[row]
            settings = self.styles[row].settings
            if column == 0 and 'foreground' in settings:
                return settings['foreground']
        elif role == QtCore.Qt.BackgroundColorRole:
            row = index.row()
            column = index.column()
            style = self.styles[row]
            settings = self.styles[row].settings
            if column == 0 and 'background' in settings:
                return settings['background']
            elif column == 1 and 'foreground' in settings:
                return settings['foreground']
            elif column == 2 and 'background' in settings:
                return settings['background']

    def setData(self, index, value, role):
        """
        Retornar verdadero si se puedo hacer el camio, falso en caso contratio
        """
        if not index.isValid: return False

        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()
            style = self.styles[row]
            if column == 0:
                self.manager.updateThemeStyle(style, name = value)
            elif column == 1 and value.canConvert(QtCore.QVariant.Color):
                self.manager.updateThemeStyle(style, settings = {'foreground' : QtGui.QColor(value) })
            elif column == 2 and value.canConvert(QtCore.QVariant.Color):
                self.manager.updateThemeStyle(style, settings = {'background' : QtGui.QColor(value) })
            elif column == 3:
                self.manager.updateThemeStyle(style, settings = {'fontStyle' : value })
            self.dataChanged.emit(index, index)
            return True
        return False
    
    def flags(self, index):
        if not index.isValid():  
            return QtCore.Qt.NoItemFlags  
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.headers[section]
    
    def index(self, row, column, parent = QtCore.QModelIndex()):
        style = self.styles[row]
        if style:
            return self.createIndex(row, column, style)
        else:
            return QtCore.QModelIndex()
    
    #========================================================================
    # Functions
    #========================================================================
    def appendStyle(self, style):
        self.beginInsertRows(QtCore.QModelIndex(), len(self.styles), len(self.styles))
        self.styles.append(style)
        self.endInsertRows()

    def removeStyle(self, style):
        index = self.styles.index(style)
        self.beginRemoveRows(QtCore.QModelIndex(), index, index)
        self.styles.remove(style)
        self.endRemoveRows()

#===============================================
# Bundle Menu Node
#===============================================
class PMXBundleMenuTreeNode(TreeNode):
    ITEM = 0
    SUBMENU = 1
    SEPARATOR = 2
    def __init__(self, name, nodeType, data = None, parent = None):
        TreeNode.__init__(self, name, parent)
        self.data = data
        self.nodeType = nodeType

#===============================================
# Bundle Menu Tree Model
#===============================================
class PMXMenuTreeModel(TreeModel):
    menuChanged = QtCore.pyqtSignal()
    
    def __init__(self, manager, parent = None):
        TreeModel.__init__(self, parent)
        self.excludedModel = PMXExcludedListModel(manager, self)
        self.manager = manager
    
    def excludedListModel(self):
        return self.excludedModel
    
    def _build_menu(self, items, parent, submenus = {}, allActionItems = []):
        for uuid in items:
            if uuid.startswith("-"):
                separatorNode = PMXBundleMenuTreeNode(uuid, PMXBundleMenuTreeNode.SEPARATOR, parent = parent)
                parent.appendChild(separatorNode)
            else:
                item = self.manager.getBundleItem(uuid)
                if item != None:
                    if item in allActionItems:
                        allActionItems.remove(item)
                    bundleItemNode = PMXBundleMenuTreeNode(item.name, PMXBundleMenuTreeNode.ITEM, item, parent)
                    parent.appendChild(bundleItemNode)
                elif uuid in submenus:
                    submenuNode = PMXBundleMenuTreeNode(submenus[uuid]['name'], PMXBundleMenuTreeNode.SUBMENU, uuid, parent)
                    parent.appendChild(submenuNode)
                    self._build_menu(submenus[uuid]['items'], submenuNode, submenus, allActionItems)

    def setBundle(self, bundle):
        self.clear()
        # allActionItems is a list with all bundleItems in te bundle
        allActionItems = self.manager.findBundleItems(bundle = bundle, TYPE = "command")
        allActionItems += self.manager.findBundleItems(bundle = bundle, TYPE = "snippet")
        allActionItems += self.manager.findBundleItems(bundle = bundle, TYPE = "macro")
        if bundle.mainMenu is not None:
            self._build_menu(bundle.mainMenu['items'], self.rootNode, bundle.mainMenu['submenus'], allActionItems)
            # allActionItems tiene los items que no estan el menu
            if 'excludedItems' in bundle.mainMenu:
                for uuid in bundle.mainMenu['excludedItems']:
                    item = self.manager.getBundleItem(uuid)
                    if item != None:
                        if item in allActionItems:
                            allActionItems.remove(item)
                        self.excludedModel.appendExcludedItem(item)
        # allActionItems tiene los items que no estan en el menu ni en la lista de excluidos
        for item in allActionItems:
            self.excludedModel.appendExcludedItem(item)
        self.layoutChanged.emit()
    
    def clear(self):
        self.excludedModel.clear()
        TreeModel.clear(self)

    def add_submenu(self, submenuNode, submenus):
        items = []
        for node in submenuNode.childrenNodes:
            if node.nodeType == PMXBundleMenuTreeNode.ITEM:
                items.append(str(node.data.uuid).upper())
            elif node.nodeType == PMXBundleMenuTreeNode.SUBMENU:
                self.add_submenu(node, submenus)
            elif node.nodeType == PMXBundleMenuTreeNode.SEPARATOR:
                items.append(node.name)
        submenus[submenuNode.data] = { "items": items, "name": submenuNode.name }
        
    def getMainMenu(self):
        items = []
        submenus = {}
        for node in self.rootNode.childrenNodes:
            if node.nodeType == PMXBundleMenuTreeNode.ITEM:
                items.append(str(node.data.uuid).upper())
            elif node.nodeType == PMXBundleMenuTreeNode.SUBMENU:
                items.append(node.data)
                self.add_submenu(node, submenus)
            elif node.nodeType == PMXBundleMenuTreeNode.SEPARATOR:
                items.append(node.name)
        mainMenu = {"items": items, "submenus": submenus }
        excludedItems = self.excludedModel.getExcludedItems()
        if excludedItems:
            mainMenu['excludedItems'] = excludedItems
        return mainMenu

    def data(self, index, role):
        if role in [ QtCore.Qt.DisplayRole, QtCore.Qt.EditRole ]:
            node = self.node(index)
            return node.name
        else:
            return None

    def setData(self, index, value, role):  
        if not index.isValid():  
            return False
        if role == QtCore.Qt.EditRole:  
            node = self.node(index)
            if node.nodeType == PMXBundleMenuTreeNode.SUBMENU:
                node.name = value
                self.menuChanged.emit()
            elif node.nodeType == PMXBundleMenuTreeNode.ITEM:
                self.manager.updateBundleItem(node.data, name = value)
                node.name = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def flags(self, index):
        defaultFlags = QtCore.QAbstractItemModel.flags(self, index)
        if index.isValid():
            node = self.node(index)
            if node.nodeType == PMXBundleMenuTreeNode.SUBMENU:
                return defaultFlags | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsEditable
            elif node.nodeType == PMXBundleMenuTreeNode.SEPARATOR:
                return defaultFlags | QtCore.Qt.ItemIsDragEnabled
            elif node.nodeType == PMXBundleMenuTreeNode.ITEM:
                return defaultFlags | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsEditable
        else:
            return QtCore.Qt.ItemIsDropEnabled | defaultFlags
    
    def mimeTypes(self):
        return [ 'application/x-ets-qt4-instance' ]

    def mimeData(self, index):
        node = self.node(index[0])
        mimeData = PyMimeData(node)
        return mimeData

    def dropMimeData(self, mimedata, action, row, column, parentIndex):
        if action == QtCore.Qt.IgnoreAction:
            return True
        
        if not mimedata.hasFormat("application/x-ets-qt4-instance"):
            return False
        
        dragNode = mimedata.instance()
        
        parentNode = self.node(parentIndex)
        
        if dragNode.parentNode == None:
            #The node belongs to a exludeListModel
            if dragNode.nodeType == PMXBundleMenuTreeNode.SEPARATOR:
                #Make a copy of separator
                separatorNode = PMXBundleMenuTreeNode(dragNode.name, PMXBundleMenuTreeNode.SEPARATOR)
                parentNode.insertChild(row, separatorNode)
            elif dragNode.nodeType == PMXBundleMenuTreeNode.SUBMENU:
                #Make a copy of submenu
                uuid = str(self.manager.uuidgen()).upper()
                submenuNode = PMXBundleMenuTreeNode(dragNode.name, PMXBundleMenuTreeNode.SUBMENU, uuid)
                parentNode.insertChild(row, submenuNode)
            elif dragNode.nodeType == PMXBundleMenuTreeNode.ITEM:
                self.excludedModel.removeMenuItem(dragNode)
                parentNode.insertChild(row, dragNode)
        elif dragNode.parentNode == parentNode:
            #Reparent
            currentRow = dragNode.row()
            row = row if currentRow >= row else row - 1
            parentNode.removeChild(dragNode)
            parentNode.insertChild(row, dragNode)
        else:
            #Reparent
            dragNode.parentNode.removeChild(dragNode)
            parentNode.insertChild(row, dragNode)
        self.menuChanged.emit()
        self.layoutChanged.emit()
        return True
        
    def removeMenuItem(self, item):
        index = self.createIndex(item.row(), 0, item)
        parentIndex = self.parent(index)
        parentNode = self.node(parentIndex)
        self.beginRemoveRows(parentIndex, item.row(), item.row())
        parentNode.removeChild(item)
        self.endRemoveRows()
        self.menuChanged.emit()

#===============================================
# Bundle Excluded Menu List Model
#===============================================
class PMXExcludedListModel(QtCore.QAbstractListModel):
    def __init__(self, manager, menuModel):
        QtCore.QAbstractListModel.__init__(self, menuModel)
        self.manager = manager
        self.menuModel = menuModel
        self.submenuNode = PMXBundleMenuTreeNode("New Group", PMXBundleMenuTreeNode.SUBMENU)
        self.separatorNode = PMXBundleMenuTreeNode("-" * 36, PMXBundleMenuTreeNode.SEPARATOR)
        self.nodes = [ self.submenuNode, self.separatorNode ]
    
    def appendExcludedItem(self, item):
        bundleItemNode = PMXBundleMenuTreeNode(item.name, PMXBundleMenuTreeNode.ITEM, item)
        self.nodes.append(bundleItemNode)
        self.layoutChanged.emit()
    
    def clear(self):
        self.nodes = self.nodes[:2]
        self.layoutChanged.emit()
    
    def getExcludedItems(self):
        items = []
        for node in self.nodes[2:]:
            items.append(str(node.data.uuid).upper())
        return items
    
    def index(self, row, column, parent):
        return self.createIndex(row, column, self.nodes[row])
    
    def rowCount(self, parent):
        return len(self.nodes)
    
    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            node = self.nodes[index.row()]
            return node.name
        else:
            return None
    
    def columnCount(self, parent):  
        return 1

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDropEnabled
        defaultFlags = QtCore.QAbstractItemModel.flags(self, index)
        node = index.internalPointer()
        if node.nodeType == PMXBundleMenuTreeNode.SUBMENU:
            return defaultFlags | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled
        return defaultFlags | QtCore.Qt.ItemIsDragEnabled
    
    def mimeTypes(self):
        return [ 'application/x-ets-qt4-instance' ]

    def mimeData(self, index):
        node = index[0].internalPointer()
        mimeData = PyMimeData(node)
        return mimeData

    def appendMenuNode(self, node):
        if node.nodeType == PMXBundleMenuTreeNode.SEPARATOR:
            self.menuModel.removeMenuItem(node)
        elif node.nodeType == PMXBundleMenuTreeNode.SUBMENU:
            for child in node.childrenNodes[:]:
                self.appendMenuNode(child)
            self.menuModel.removeMenuItem(node)
        elif node.nodeType == PMXBundleMenuTreeNode.ITEM and node not in self.nodes:
            self.menuModel.removeMenuItem(node)
            self.nodes.append(node)
        
    def dropMimeData(self, mimedata, action, row, column, parentIndex):
        if action == QtCore.Qt.IgnoreAction:
            return True
        
        if not mimedata.hasFormat("application/x-ets-qt4-instance"):
            return False
        
        dragNode = mimedata.instance()
        if dragNode not in self.nodes:
            self.appendMenuNode(dragNode)
            self.layoutChanged.emit()
            return True
        return False
        
    def removeMenuItem(self, node):
        index = self.nodes.index(node) - 1 
        self.beginRemoveRows(QtCore.QModelIndex(), index, index)
        self.nodes.remove(node)
        self.endRemoveRows()