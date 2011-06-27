#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from prymatex.gui.support.qtadapter import buildKeySequence, buildKeyEquivalent, buildQColor
#from PyQt4.Qt import *

#====================================================
# Bundle Tree Model
#====================================================
class PMXBundleTreeNode(object):
    ''' 
        Bundle and bundle item decorator
    '''
    ICONS = {
             "template": QtGui.QPixmap(":/bundles/resources/bundles/templates.png"),
             "command": QtGui.QPixmap(":/bundles/resources/bundles/commands.png"),
             "syntax": QtGui.QPixmap(":/bundles/resources/bundles/languages.png"),
             "preference": QtGui.QPixmap(":/bundles/resources/bundles/preferences.png"),
             "dragcommand": QtGui.QPixmap(":/bundles/resources/bundles/drag-commands.png"),
             "snippet": QtGui.QPixmap(":/bundles/resources/bundles/snippets.png"),
             "macro": QtGui.QPixmap(":/bundles/resources/bundles/macros.png"),
             "templatefile": QtGui.QPixmap(":/bundles/resources/bundles/template-files.png") 
    }
    
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
        icon = self.ICONS[self.TYPE] if self.TYPE in self.ICONS else None
        return icon
    
    @property
    def trigger(self):
        trigger = []
        if self.tabTrigger != None:
            trigger.append(u"%s⇥" % (self.tabTrigger))
        if self.keyEquivalent != None:
            trigger.append(u"%s" % QtGui.QKeySequence(self.keyEquivalent).toString())
        return ", ".join(trigger)
    
    def buildMenuTextEntry(self, nemonic = ''):
        text = unicode(self.name)
        if nemonic:
            return text.replace('&', '&&') + u"\t" + nemonic
        else:
            text += u"\t%s" % (self.trigger)
        return text.replace('&', '&&')
    
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

    def child(self, row):
        if len(self.children) > row:
            return self.children[row]

    def childCount(self):
        return len(self.children)

    def row(self):  
        if self.parent is not None:  
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
            name = unicode(value.toString())
            if item.TYPE == "bundle":
                self.manager.updateBundle(item, name = name)
            elif item.TYPE == "templatefile":
                pass
            else:
                self.manager.updateBundleItem(item, name = name)
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
            return QtCore.QVariant(item.name)
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

        if parent == self.root:  
            return QtCore.QModelIndex()

        return self.createIndex(parent.row(), 0, parent)
    
    #========================================================================
    # Functions
    #========================================================================
    def appendBundle(self, bundle):
        self.beginInsertRows(QtCore.QModelIndex(), self.root.childCount(), self.root.childCount())
        self.root.appendChild(bundle)
        self.endInsertRows()
    
    def appendBundleItem(self, bundleItem):
        bnode = bundleItem.bundle
        self.beginInsertRows(self.index(bnode.row(), 0, QtCore.QModelIndex()), bnode.childCount(), bnode.childCount())
        bundleItem.bundle.appendChild(bundleItem)
        self.endInsertRows()
    
    def getAllBundles(self):
        return self.root.children
    
    def getBundle(self, uuid):
        for child in self.root.children:
            if child.uuid == uuid:
                return child
        
#====================================================
# Themes Styles
#====================================================

class PMXThemeStyleRow(object):
    ''' 
        Theme and Style decorator
    '''
    STYLES_CACHE = {}
    def __init__(self, item, scores = None):
        self.item = item
        self.scores = scores
    
    def __getattr__(self, name):
        return getattr(self.item, name)
    
    @property
    def settings(self):
        settings = {}
        settings.update(self.item.settings)
        for color_key in ['foreground', 'background', 'selection', 'invisibles', 'lineHighlight', 'caret', 'gutter']:
            if color_key in settings:
                color = buildQColor(settings[color_key])
                settings[color_key] = color
        if 'fontStyle' in settings:
            settings['fontStyle'] = settings['fontStyle'].split()
        return settings
    
    def setForeground(self, value):
        self.item.settings['foreground'] = value
        
    def setBackground(self, value):
        self.item.settings['background'] = value
    
    def clearCache(self):
        PMXThemeStyleRow.STYLES_CACHE = {}
        
    def getStyle(self, scope = None):
        if scope in PMXThemeStyleRow.STYLES_CACHE:
            return PMXThemeStyleRow.STYLES_CACHE[scope]
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
        PMXThemeStyleRow.STYLES_CACHE[scope] = base
        return base

class PMXThemeStylesTableModel(QtCore.QAbstractTableModel):
    def __init__(self, manager, parent = None):
        super(PMXThemeStylesTableModel, self).__init__(parent)
        self.manager = manager
        self.styles = []
        self.headers = ['Element', 'Foreground', 'Background', 'Font Style']
        
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
            if column == 0:
                style = self.styles[row]
                return QtCore.QVariant(style.scope)
            elif column == 1:
                settings = self.styles[row].settings
                return QtCore.QVariant(settings['foreground'])
            elif column == 2:
                settings = self.styles[row].settings
                return QtCore.QVariant(settings['background'])
            elif column == 3:
                settings = self.styles[row].settings
                return QtCore.QVariant(", ".join(settings['fontStyle']))
        elif role == QtCore.Qt.DecorationRole:
            row = index.row()
            column = index.column()
            if column == 1:
                settings = self.styles[row].settings
                pixmap = QtGui.QPixmap(26, 26)
                pixmap.fill(settings['foreground'])
                return pixmap
            elif column == 2:
                settings = self.styles[row].settings
                pixmap = QtGui.QPixmap(26, 26)
                pixmap.fill(settings['background'])
                return pixmap

    def setData(self, index, value, role):
        '''
            Retornar verdadero si se puedo hacer el camio, falso en caso contratio
        '''
        if not index.isValid: return False

        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()
            if column == 0:
                style = self.styles[row]
                style.setScope(unicode(value))
            elif column == 1:
                self.styles[row].setForeground(unicode(value))
            elif column == 2:
                self.styles[row].setBackground(unicode(value))
            self.dataChanged.emit(index, index)
            return True
        elif role == QtCore.Qt.CheckStateRole:
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
    
    #========================================================================
    # Functions
    #========================================================================
    def appendStyle(self, style):
        self.beginInsertRows(QtCore.QModelIndex(), len(self.styles), len(self.styles))
        self.styles.append(style)
        self.endInsertRows()
        