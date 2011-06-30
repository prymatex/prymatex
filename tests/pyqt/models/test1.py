from PyQt4.QtCore import *
from PyQt4.QtGui import *

class GeneralItem(object):
    def __init__(self,  name = str(),  parent = None,  index=None,  size = int(),  time = QDateTime(),  permission = str()):
        
        self.setName(name)
        self.setParent(parent)
        self.setModelIndex(index)
        self.setSize(size)
        self.setTime(time)
        self.setPermission(permission)
    
    def setName(self,  name):
        self.__name = name
    
    def setParent(self,  parent):
        self.__parent = parent
    
    def setModelIndex(self,  index):
        self.__index = index
    
    def setSize(self,  size):
        self.__size = size
    
    def setTime(self,  time):
        self.__time = time
    
    def setPermission(self,  permission):
        self.__permission = permission
    
    def name(self):
        return self.__name
    
    def parent(self):
        return self.__parent
    
    def modelIndex(self):
        return self.__index
    
    def row(self):
        if self.parent():
            return self.parent().children().index(self)
        return 0
    
    def size(self):
        return self.__size
    
    def time(self):
        return self.__time
    
    def permission(self):
        return self.__permission

class DirectoryItem(GeneralItem):
    def __init__(self,  name = str(),  parent = None,  size = int(),  time = QDateTime(),  permission = str()):
        GeneralItem.__init__(self,  name,  parent,  size,  time,  permission)
        
        self.clearChildren()

    def children(self):
        return self.__children
    
    def hasChildren(self):
        return bool(self.children())

    def appendChild(self,  child):
        child.setParent(self)
        self.__children.append(child)

    def clearChildren(self):
        self.__children = list()

    def __len__(self):
        return len(self.children())

def FileItem(GeneralItem):
    def hasChildren(self):
        return False

class ObexDirectoryView(QAbstractItemModel):
    def __init__(self):
        QAbstractItemModel.__init__(self)

        self.__rootItem = DirectoryItem()

    def rowCount(self,  parent=QModelIndex()):
        if parent.isValid():
            #print "rowCount, parent is valid -> internalPointer"
            parentItem = parent.internalPointer()
            #print "parentItem",  parentItem,  parentItem.name(),  parentItem.children(),  parentItem.children()[0].name()
        else:
            #print "rowCount, parent is NOT valid -> rootItem"
            parentItem = self.__rootItem
        #print "rowCount",  len(parentItem)
        return len(parentItem)

    def hasChildren(self,  index=QModelIndex()):
        parentItem = index.internalPointer()
        if parentItem is not None:
            #print "hasChildren",  parentItem,  parentItem.hasChildren()
            return parentItem.hasChildren()
        else:
            #print "hasChildren",  parentItem,  "True"
            return True

    def columnCount(self,  parent=QModelIndex()):
        #print "columnCount",  1
        return 1

    def index(self, row, column, parent=QModelIndex()):
        if not self.hasIndex(row, column, parent):
            #print "index -> not self.hasIndex"
            return QModelIndex()

        if parent.isValid():
            #print "index parent is valid -> interalPointer"
            parentItem = parent.internalPointer()
        else:
            #print "index parent is not valid -> rootItem"
            parentItem = self.__rootItem

        child = parentItem.children()[row]
        #print "index parent",  parentItem
        #print "index child", child
        #print "index",  row,  column,  child
        #print "index child name",  child.name()
        #print "index parent name",  parentItem.name()
        index = self.createIndex(row, column, child)
        print "create index",  index,  index.row(),  index.column(),  "for",  child.name()
        if index.column() == 0:
            child.setModelIndex(index)
        return index

    def parent(self, index):
        if not index.isValid():
            #print "parent -> not index.isvalid()"
            return QModelIndex()

        parent = index.internalPointer().parent()
        if parent == self.__rootItem or parent is None:
            #print "parent -> parent == self.__rootItem or parent is None"
            return QModelIndex()
        #print "parent",  parent.row(), 0, parent
        return self.createIndex(parent.row(), 0, parent)

    def data(self,  index,  role = Qt.DisplayRole):
        if index.isValid() and role == Qt.DisplayRole and index.column() == 0:
            item = index.internalPointer()
            #print "data",  index,  role,  item.name()
            return QVariant(item.name())
        #print "data -> else branch"
        return QVariant()

    def appendChild(self,  child,  parent=None):
        #print "appendChild, child"
        if parent == None:
            parent = self.__rootItem
        
        index = parent.modelIndex() or QModelIndex()
        print "append to",  index,  index.row(),  index.column(),  "for",  parent.name()
        self.insertRow(-1,  index)

        parent.appendChild(child)

class ColumnView(QTreeView):
    def __init__(self):
        super(ColumnView,  self).__init__()

        self.model = ObexDirectoryView()
        
        item1 = DirectoryItem("Root Item 1")
        item2 = DirectoryItem("Root Item 2")
        item3 = DirectoryItem("Child 1 of Root 1")
        item4 = DirectoryItem("Child 1 of Root 2")
        
        self.model.appendChild(item1)
        self.model.appendChild(item2)
        self.model.appendChild(item3,  item1)
        self.model.appendChild(item4,  item2)
        
        self.setModel(self.model)
        

        self.resize(700,  700)
        self.show()
        
        item5 = DirectoryItem("Root Item 3")
        item6 = DirectoryItem("Child 1 of Root 3")
        
        self.model.appendChild(item5)
        self.model.appendChild(item6,  item5)
        

app = QApplication([])
m = ColumnView()
app.exec_()