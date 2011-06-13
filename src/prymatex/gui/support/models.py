#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt, QString
from prymatex.core.exceptions import APIUsageError
from prymatex.gui.support.qtadapter import buildKeySequence, buildKeyEquivalent
from prymatex.mvc.models import PMXTableBase, PMXTableField
from prymatex.mvc.delegates import PMXChoiceItemDelegate
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
            return int(buildKeySequence(self.item.keyEquivalent))
    
    @keyEquivalent.setter
    def keyEquivalent(self, key):
        self.item.keyEquivalent = buildKeyEquivalent(key)
    
    @property
    def icon(self):
        icon = self.ICONS[self.TYPE] if self.TYPE in self.ICONS else None
        return icon
    
    @property
    def trigger(self):
        trigger = []
        if self.tabTrigger != None:
            trigger.append(u"%s?" % (self.tabTrigger))
        if self.keyEquivalent != None:
            trigger.append(u"%s" % buildKeySequence(self.keyEquivalent).toString())
        return ", ".join(trigger)
    
    def buildMenuTextEntry(self, nemonic = ''):
        text = unicode(self.name)
        if nemonic:
            return text.replace('&', '&&') + u"\t" + nemonic
        else:
            text += u"\t%s" % (self.trigger)
        return text.replace('&', '&&')
    
    #==================================================
    # Tree Node interface
    #==================================================
    def appendChild(self, child):
        self.children.append(child)

    def child(self, row):
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
        
    def _populateFromManager(self):
        for bundle in self.manager.getAllBundles():
            bti = PMXBundleTreeNode(bundle, self.root)
            self.root.appendChild(bti)
            bundle_items = self.manager.findBundleItems(bundle = bundle)
            self.setupModelData(bundle_items, bti)
    
    def populateToBundleNode(self, bundle):
        bti = PMXBundleTreeNode(bundle, self.root)
        self.root.appendChild(bti)
        return bti
        
    def populateToBundleItemNode(self, bundleItem):
        bti = PMXBundleTreeNode(bundleItem, bundleItem.bundle)
        if bundleItem.TYPE == "template":
            for file in bundleItem.getTemplateFiles():
                tifi = PMXBundleTreeNode(file, bti)
                bti.appendChild(tifi)
        bundleItem.bundle.appendChild(bti)
        return bti
    
    def setData(self, index, value, role):  
        if not index.isValid():  
            return False
        elif role == QtCore.Qt.EditRole:  
            item = index.internalPointer()  
            item.name = unicode(value.toString())
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

    def setupModelData(self, items, parent):
        for item in items:
            biti = PMXBundleTreeNode(item, parent)
            if item.TYPE == "template":
                for file in item.getTemplateFiles():
                    tifi = PMXBundleTreeNode(file, biti)
                    biti.appendChild(tifi)
            parent.appendChild(biti)

#====================================================
# Themes Styles
#====================================================
class PMXThemeStylesTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent = None):
        super(PMXThemeStylesTableModel, self).__init__(parent)
        self.styles = []
        self.headers = ['Element', 'Foreground', 'Background', 'Font Style']
        
    def rowCount(self, parent):
        return len(self.styles)
    
    def columnCount(self, parent):
        return 4
    
    def data(self, index, role):
        if not index.isValid: return QtCore.QVariant()
        return QtCore.QVariant()

    def setData(self, index, value, role):
        '''
            Retornar verdadero si se puedo hacer el camio, falso en caso contratio
        '''
        if not index.isValid: return False

        if role == QtCore.Qt.EditRole:
            self.dataChanged.emit(index, index)
            return True;
        elif role == QtCore.Qt.CheckStateRole:
            self.dataChanged.emit(index, index)
            return True
        return False
        
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.headers[section]

    def insertRows(self, position, rows, parent = QtCore.QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)
        self.endInsertRows()
        return True

    def removeRows(self, position, rows, parent = QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1);
        self.endRemoveRows()
        return True

    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled

#====================================================
# Bundle Item Table Model
#====================================================
class PMXBundleItemInstanceItem(QtGui.QStandardItem):
    '''
    Create a superclass?
    '''
    def __init__(self, pmx_bundle_item):
        super(PMXBundleItemInstanceItem, self).__init__()
        from prymatex.support.bundle import PMXBundleItem
        if isinstance(pmx_bundle_item, PMXBundleItem):
            self.setData(pmx_bundle_item, QtCore.Qt.EditRole)
            self.setData(unicode(pmx_bundle_item), QtCore.Qt.DisplayRole)
        
    def setData(self, value, role):
        '''
        Display something, but store data
        http://doc.trolltech.com/latest/qstandarditem.html#setData
        '''
        if role == Qt.EditRole:
            self._item = value
        elif role == Qt.DisplayRole:
            super(PMXBundleItemInstanceItem, self).setData(value, role)
        else:
            raise TypeError("setData called with unsupported role")
    
    def data(self, role = Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return super(PMXBundleItemInstanceItem, self).data(role)
        elif role == Qt.EditRole:
            return self._item
    
    @property
    def item(self):
        return self._item
    
class PMXBundleModel(PMXTableBase):
    '''
    Store xxx.tmBundle/info.plist data
    '''
    
    uuid = PMXTableField(title = "UUID")
    name = PMXTableField()
    namespace = PMXTableField()
    description = PMXTableField()
    contactName = PMXTableField( title = "Contact Name")
    contactMailRot13 = PMXTableField(title = "Conatact E-Mail")
    disabled = PMXTableField()
    item = PMXTableField()
    
    def appendBundleRow(self, bundle):
        self.addRowFromKwargs(
                    uuid = bundle.uuid,
                    name = bundle.name,
                    namespace = bundle.namespace,
                    description = bundle.description,
                    contactName = bundle.contactName,
                    contactMailRot13 = bundle.contactMailRot13,
                    disabled = bundle.disabled,
                    item = bundle,
                    )
        
        

class PMXBundleTypeDelegate(PMXChoiceItemDelegate):
    CHOICES = [('Command', 1),
               ('Snippet', 2),
               ('Macro', 3),
               ('Syntax', 5),
               ]

class PMXBundleItemDelegate(QtGui.QItemDelegate):
    # Just to try
    def createEditor(self, *largs):
        return QtGui.QTextEdit()

class PMXBundleItemModel(PMXTableBase):
    '''
    Stores Command, Syntax, Snippets, etc. information
    '''
    
    bundleUUID = PMXTableField(editable = False, title = "Bundle UUID")
    path = PMXTableField(editable = False, )
    namespace = PMXTableField(editable = False)
    
    uuid = PMXTableField(title = "UUID")
    type_ = PMXTableField(title = "Item Type", 
                          delegate_class = PMXBundleTypeDelegate)
    name = PMXTableField()
    tabTrigger = PMXTableField(title = "Tab Trigger")
    keyEquivalent = PMXTableField(title = "Key Equivalent")
    scope = PMXTableField()
    item = PMXTableField(item_class = PMXBundleItemInstanceItem, delegate_class=PMXBundleItemDelegate)
   
    def appendBundleItemRow(self, instance):
        '''
        Appends a new row based on an instance
        @param instance A PMXCommand, PMXSnippet, PMXMacro instance
        '''
        self.addRowFromKwargs(bundleUUID = instance.bundle.uuid,
                          path = instance.path,
                          namespace = instance.namespace,
                          uuid = instance.uuid,
                          type_ = instance.TYPE,
                          name = instance.name,
                          tabTrigger = instance.tabTrigger,
                          keyEquivalent = instance.keyEquivalent,
                          scope = instance.scope,
                          item = instance,
        )
    
    def getProxyFilteringModel(self, **filter_kwargs):
        ''' Returns a list of QStandardItems 
            I.E. get_by(uuid = 'aaa-bb-cc')
        ''' 
        proxy = PMXTableFilterProxyModel(self, **filter_kwargs)
        return proxy 
        

class PMXTableFilterProxyModel(QtGui.QSortFilterProxyModel):
    '''
    Filter created through getProxyFilteringModel(setup)
    
    @param sourceModel: A PMXTableBase instance
    @param resultsIfEmpty: Show tables
    @param filterArguments: Filter colName = colValue  
    
    '''
    def __init__(self, sourceModel, resultsIfEmpty = False, order_by = None, **filterArguments):
        '''
        Simple
        '''
        super(PMXTableFilterProxyModel, self).__init__()
        self.sourceModel = sourceModel
        self.setSourceModel(self.sourceModel)
        self.filters = {}
        
        for key in filterArguments:
            if not key in self.sourceModel._meta.fieldNames:
                raise APIUsageError("%s is not a valid field of %s" % (key, self.sourceModel))
            colNumber = self.sourceModel._meta.colNumber(key)
            self.filters[colNumber] = filterArguments[key]
        self.resultsIfEmpty = resultsIfEmpty
        
        if order_by:
            colNumber = self.sourceModel._meta.colNumber(order_by)
            self.order_by = self.setFilterKeyColumn(colNumber)
            
        
        
        
    def filterAcceptsRow(self, row, parent):
        '''
        Stores values 
        '''
        
        if not self.filters: 
            return self.resultsIfEmpty
        # For each key = value
        for colNumber, colValue in self.filters.iteritems():
            #print "Buscando ", row, " con ", self.filters
            data = self.sourceModel.index(row, colNumber).data().toPyObject()
            #print "filter", data
            if data != colValue:
                return False
        return True
    
    _resultsIfEmpty = True
    @property
    def resultsIfEmpty(self):
        return self._resultsIfEmpty
    
    @resultsIfEmpty.setter
    def resultsIfEmpty(self, value):
        ''' Populate model when no filter criteria has been 
        defined yet'''
        self._resultsIfEmpty = value
    
    def __getitem__(self, key): 
        '''
        A simple shortcut for row, column access
        @todo Implement data
        '''
        
        if len(key) == 2:
            row, column = key
            if not isinstance(row, int):
                raise APIUsageError("Row indexes must be integers")
            if isinstance(column, (basestring, QString)):
                column = self.sourceModel._meta.colNumber(column)
            elif not isinstance(column, int):
                raise APIUsageError("Indexes must be integers")
            #print "Indexing proxy model with", row, ", ", column
            return self.index(row, column).data().toPyObject()
        raise APIUsageError("Can't use %s as index for model try (row, column), where columns"
                            "can be names")
    
    def findItems(self, query, flags, column):
        '''
        Find items based on
        ''' 
        if isinstance(column, (QString, basestring)):
            column = self.sourceModel._meta.colNumber(column)
        items = self.sourceModel.findItems(query, flags, column)
        print "Query: (%s)" % map(unicode, (query, flags, column))
        print items
        for item in items:
            print item
    
    
if __name__ == "__main__":
    import sys
    a = QtGui.QApplication(sys.argv)
    w = QtGui.QTableView()
    model = PMXBundleItemModel()
    w.setModel(model)
    w.setGeometry(400, 100, 600, 480)
    w.resizeColumnsToContents()
    w.show()
    sys.exit(a.exec_())