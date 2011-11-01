#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from prymatex.resources import IMAGES
from prymatex.gui.support.qtadapter import buildKeySequence, buildKeyEquivalent, RGBA2QColor, QColor2RGBA

#====================================================
# Bundle Tree Model
#====================================================
class PMXBundleTreeNode(object):
    ''' 
        Bundle and bundle item decorator
    '''
    USED = []
    BANNED_ACCEL = ' \t'
    
    def __init__(self, item, parent = None):
        self.item = item
        self.parent = parent
        self.children = []
    
    def __getattr__(self, name):
        return getattr(self.item, name)
    
    #==================================================
    # Item decoration
    #==================================================
    @property
    def keyEquivalent(self):
        if self.item.keyEquivalent is not None:
            return buildKeySequence(self.item.keyEquivalent)
    
    @property
    def icon(self):
        icon = IMAGES[self.TYPE] if self.TYPE in IMAGES else None
        return icon
    
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
    
    def buildMenuTextEntry(self, mnemonic = ''):
        text = unicode(self.name)
        if mnemonic:
            return text.replace('&', '&&') + u"\t" + mnemonic
        else:
            text += u"\t%s" % (self.trigger)
        return text.replace('&', '&&')
    
    def triggerItemAction(self, parent = None):
        if not hasattr(self, "action"):
            assert parent is not None, "Parent of action mustn't be None"
            self.action = self.buildTriggerItemAction(parent)
        return self.action
    
    def buildTriggerItemAction(self, parent, mnemonic = '', receiver = None):
        action = QtGui.QAction(QtGui.QIcon(self.icon), self.buildMenuTextEntry(mnemonic), parent)
        #If receiver is none set the default 
        if receiver is None:
            receiver = lambda item = self: item.manager.bundleItemTriggered.emit(item)
        parent.connect(action, QtCore.SIGNAL('triggered()'), receiver)
        return action
    
    def update(self, hash):
        if 'keyEquivalent' in hash:
            hash['keyEquivalent'] = buildKeyEquivalent(hash['keyEquivalent'])
        self.item.update(hash)
    
    #==================================================
    # Tree Node interface
    #==================================================
    def appendChild(self, child):
        self.children.append(child)
        child.parent = self

    def removeChild(self, child):
        self.children.remove(child)
        
    def child(self, row):
        if len(self.children) > row:
            return self.children[row]

    def childCount(self):
        return len(self.children)

    def row(self):  
        if self.parent is not None and self in self.parent.children:  
            return self.parent.children.index(self)

class RootNode(object):
    def __init__(self):
        self.name = "root"
        self.TYPE = "root"

class PMXBundleTreeModel(QtCore.QAbstractItemModel):  
    def __init__(self, manager, parent = None):
        super(PMXBundleTreeModel, self).__init__(parent)
        self.manager = manager
        self.root = PMXBundleTreeNode(RootNode())
    
    def setData(self, index, value, role):  
        if not index.isValid():  
            return False
        elif role == QtCore.Qt.EditRole:  
            item = index.internalPointer()
            if item.TYPE == "bundle":
                self.manager.updateBundle(item, name = value)
            elif item.TYPE == "templatefile":
                pass
            else:
                self.manager.updateBundleItem(item, name = value)
            self.dataChanged.emit(index, index)
            return True
        elif role == QtCore.Qt.CheckStateRole:
            item = index.internalPointer()
            if item.TYPE == "bundle":
                self.manager.disableBundle(item, not value)
            self.dataChanged.emit(index, index)
            return True
        return False
     
    def removeRows(self, position = 0, count = 1,  parent=QtCore.QModelIndex()):
        node = self.nodeFromIndex(parent)
        self.beginRemoveRows(parent, position, position + count - 1)  
        node.children.pop(position)  
        self.endRemoveRows()  

    def nodeFromIndex(self, index):  
        if index.isValid():  
            return index.internalPointer()  
        else:
            return self.root  

    def rowCount(self, parent):
        if parent.column() > 0:  
            return 0  

        if not parent.isValid():  
            parent = self.root  
        else:  
            parent = parent.internalPointer()  

        return parent.childCount()
    
    def columnCount(self, parent):  
        return 1  

    def data(self, index, role):  
        if not index.isValid():  
            return None
        elif role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            item = index.internalPointer()
            return item.name
        elif role == QtCore.Qt.DecorationRole:
            item = index.internalPointer()
            return item.icon

    def flags(self, index):
        if not index.isValid():  
            return QtCore.Qt.NoItemFlags  
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    def headerData(self, section, orientation, role):  
        return None

    def index(self, row, column, parent):
        if not parent.isValid():
            parent = self.root
        else:
            parent = parent.internalPointer()
        
        child = parent.child(row)
        if child:
            return self.createIndex(row, column, child)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():  
            return QtCore.QModelIndex()  

        child = index.internalPointer()  
        parent = child.parent
        row = parent.row()
        
        if parent == self.root or row is None:  
            return QtCore.QModelIndex()

        return self.createIndex(row, 0, parent)
    
    #========================================================================
    # Functions
    #========================================================================
    def appendBundle(self, bundle):
        self.beginInsertRows(QtCore.QModelIndex(), self.root.childCount(), self.root.childCount())
        self.root.appendChild(bundle)
        self.endInsertRows()
    
    def removeBundle(self, bundle):
        self.beginRemoveRows(QtCore.QModelIndex(), bundle.row(), bundle.row())
        self.root.removeChild(bundle)
        self.endRemoveRows()
    
    def appendBundleItem(self, bundleItem):
        bnode = bundleItem.bundle
        self.beginInsertRows(self.index(bnode.row(), 0, QtCore.QModelIndex()), bnode.childCount(), bnode.childCount())
        bundleItem.bundle.appendChild(bundleItem)
        self.endInsertRows()
    
    def removeBundleItem(self, bundleItem):
        pindex = self.index(bundleItem.bundle.row(), 0, QtCore.QModelIndex())
        index = self.index(bundleItem.row(), 0, pindex)
        self.beginRemoveRows(pindex, index.row(), index.row())
        bundleItem.bundle.removeChild(bundleItem)
        self.endRemoveRows()
    
#====================================================
# Themes Styles
#====================================================

class PMXThemeStyleRow(object):
    ''' 
        Theme and Style decorator
    '''
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
                color = RGBA2QColor(self.item.settings[color_key])
                settings[color_key] = color
        settings['fontStyle'] = self.item.settings['fontStyle'].split() if 'fontStyle' in self.item.settings else []
        return settings
    
    def update(self, hash):
        if 'settings' in hash:
            settings = {}
            for key in hash['settings'].keys():
                if key in ['foreground', 'background', 'selection', 'invisibles', 'lineHighlight', 'caret', 'gutter']:
                    settings[key] = QColor2RGBA(hash['settings'][key])
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

class PMXThemeStylesTableModel(QtCore.QAbstractTableModel):
    def __init__(self, manager, parent = None):
        super(PMXThemeStylesTableModel, self).__init__(parent)
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
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
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
        '''
            Retornar verdadero si se puedo hacer el camio, falso en caso contratio
        '''
        if not index.isValid: return False

        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()
            style = self.styles[row]
            if column == 0:
                self.manager.updateThemeStyle(style, name = unicode(value.toString()))
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
        