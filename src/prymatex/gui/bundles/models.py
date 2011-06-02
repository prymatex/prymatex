from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt, QString
from prymatex.core.exceptions import APIUsageError
from prymatex.models.base import PMXTableBase, PMXTableField
from prymatex.models.delegates import PMXChoiceItemDelegate
#from PyQt4.Qt import *

#====================================================
# Bundle Tree Model
#====================================================
class PMXBundleTreeItem(object):  
    def __init__(self, data, parent=None):
        self.data = data
        self.parentItem = parent
        self.childItems = []
        self.setIcon(self.tipo)
        
    @property
    def name(self):
        return self.data.name
        
    @property
    def tipo(self):
        return self.data.TYPE
    
    def setIcon(self, tipo):
        self.icon = QtGui.QPixmap()
        if tipo == "template":
            self.icon.load(":/bundles/resources/bundles/templates.png")
        elif tipo == "command":
            self.icon.load(":/bundles/resources/bundles/commands.png")
        elif tipo == "syntax":
            self.icon.load(":/bundles/resources/bundles/languages.png")
        elif tipo == "preference":
            self.icon.load(":/bundles/resources/bundles/preferences.png")
        elif tipo == "dragcommand":
            self.icon.load(":/bundles/resources/bundles/drag-commands.png")
        elif tipo == "snippet":
            self.icon.load(":/bundles/resources/bundles/snippets.png")
        elif tipo == "macro":
            self.icon.load(":/bundles/resources/bundles/macros.png")
        elif tipo == "template-file":
            self.icon.load(":/bundles/resources/bundles/template-files.png")
        else:
            self.icon = None

    def appendChild(self, child):
        self.childItems.append(child)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return 1

    def parent(self):  
        return self.parentItem  

    def row(self):  
        if self.parentItem:  
            return self.parentItem.childItems.index(self)  
        return 0
    
    def setData(self, data):  
        self.data = data

class RootItem(object):
    def __init__(self):
        self.name = "root"
        self.TYPE = "root"

class PMXBundleTreeModel(QtCore.QAbstractItemModel):  
    def __init__(self, manager, parent = None):
        super(PMXBundleTreeModel, self).__init__(parent)  
        self.manager = manager
        self.rootItem = PMXBundleTreeItem(RootItem())
        
    def populateFromManager(self):
        for bundle in self.manager.getAllBundles():
            bti = PMXBundleTreeItem(bundle, self.rootItem)
            self.rootItem.appendChild(bti)
            bundle_items = self.manager.findBundleItems(bundle = bundle)
            self.setupModelData(bundle_items, bti)
    
    def addBundle(self, bundle):
        bti = PMXBundleTreeItem(bundle, self.rootItem)
        self.rootItem.appendChild(bti)
        
    def addBundleItem(self, bundleItem):
        bnode = filter(lambda bnode: bnode.data == bundleItem.bundle, self.rootItem.childItems)
        if len(bnode) != 1:
            raise Exception("No bundle node for bundle item: %s", bundleItem.name)
        bnode = bnode[0]
        bti = PMXBundleTreeItem(bundleItem, bnode)
        if bundleItem.TYPE == "template":
            for file in bundleItem.getTemplateFiles():
                tifi = PMXBundleTreeItem(file, bti)
                bti.appendChild(tifi)
        bnode.appendChild(bti)
    
    def setData(self, index, value, role):  
        if not index.isValid():  
            return False
        elif role == QtCore.Qt.EditRole:  
            item = index.internalPointer()  
            item.data.name = unicode(value.toString())
            return True
        return False  
     
    def removeRows(self, position=0, count=1,  parent=QtCore.QModelIndex()):
        node = self.nodeFromIndex(parent)
        self.beginRemoveRows(parent, position, position + count - 1)  
        node.childItems.pop(position)  
        self.endRemoveRows()  

    def nodeFromIndex(self, index):  
        if index.isValid():  
            return index.internalPointer()  
        else:  
            return self.rootItem  

    def columnCount(self, parent):  
        if parent.isValid():  
            return parent.internalPointer().columnCount()  
        else:  
            return self.rootItem.columnCount()  

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
        if row < 0 or column < 0 or row >= self.rowCount(parent) or column >= self.columnCount(parent):  
            return QtCore.QModelIndex()  

        if not parent.isValid():  
            parentItem = self.rootItem  
        else:  
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:  
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):  
        if not index.isValid():  
            return QtCore.QModelIndex()  

        childItem = index.internalPointer()  
        parentItem = childItem.parent()  

        if parentItem == self.rootItem:  
            return QtCore.QModelIndex()  

        return self.createIndex(parentItem.row(), 0, parentItem)  

    def rowCount(self, parent):  
        if parent.column() > 0:  
            return 0  

        if not parent.isValid():  
            parentItem = self.rootItem  
        else:  
            parentItem = parent.internalPointer()  

        return parentItem.childCount()  

    def setupModelData(self, items, parent):
        for item in items:
            biti = PMXBundleTreeItem(item, parent)
            if item.TYPE == "template":
                for file in item.getTemplateFiles():
                    tifi = PMXBundleTreeItem(file, biti)
                    biti.appendChild(tifi)
            parent.appendChild(biti)

class PMXBundleTreeProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self, parent = None):
        super(PMXBundleTreeProxyModel, self).__init__(parent)
        self.bundleItemTypeOrder = ["bundle", "command", "dragcommand", "macro", "snippet", "preference", "template", "template-file", "syntax"]
        
    def filterAcceptsRow(self, sourceRow, sourceParent):
        regexp = self.filterRegExp()
        if regexp.isEmpty():
            return True
        index = self.sourceModel().index(sourceRow, 0, sourceParent)
        item = index.internalPointer()
        if item.tipo == "bundle":
            return True
        else:
            return QtCore.QString(item.tipo).contains(regexp)
        
    def filterAcceptsColumn(self, sourceColumn, sourceParent):
        return True
        
    def lessThan(self, left, right):
        leftData = left.internalPointer()
        rightData = right.internalPointer()
        if leftData.tipo == rightData.tipo:
            return rightData.name > leftData.name
        else:
            return self.bundleItemTypeOrder.index(rightData.tipo) > self.bundleItemTypeOrder.index(leftData.tipo)

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
                              #item = item,
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
    def __init__(self, sourceModel, resultsIfEmpty = False, **filterArguments):
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
    
    def __setitem__(self, key, value):
        self.filters.update(key = value)
    
    def __getitem__(self, key):
        if len(key) == 2:
            row, column = key
            if not isinstance(row, int):
                raise APIUsageError("Indexes must be integers")
            if isinstance(column, (basestring, QString)):
                column = self.sourceModel._meta.colNumber(column)
            elif not isinstance(column, int):
                raise APIUsageError("Indexes must be integers")
            #print "Indexing proxy model with", row, ", ", column
            return self.index(row, column).data().toPyObject()
        raise APIUsageError("Can't use %s as index for model try (row, column), where columns"
                            "can be names")
    
    def getSrcModelField(self, index, fieldName):
        pass
    
    
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