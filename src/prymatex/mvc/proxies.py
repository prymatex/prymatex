from PyQt4 import QtCore, QtGui

class PMXFlatBaseProxyModel(QtCore.QAbstractItemModel):
    '''
        Proxy for create flat models from tree models
    '''
    def __init__(self, parent = None):
        super(PMXFlatBaseProxyModel, self).__init__(parent)
        self.__indexMap = []
        self.__sourceModel = None

    def sourceModel(self):
        return self.__sourceModel
        
    def setSourceModel(self, model):
        if model == self.__sourceModel:
            return
        if self.__sourceModel is not None:
            self.__sourceModel.disconnect(self)
        self.__sourceModel = model
        self.__sourceModel.dataChanged.connect(self.reMapModel)
        self.__sourceModel.layoutChanged.connect(self.reMapModel)
    
    def filterAcceptsRow(self, sourceRow, sourceParent):
        return True
        
    def filterAcceptsColumn(self, sourceColumn, sourceParent):
        return True
    
    def mapToSource(self, proxyIndex):
        return self.__indexMap[proxyIndex.row()]
        
    def mapFromSource(self, sourceIndex):
        return self.__indexMap.index(sourceIndex)
            
    def columnCount(self, parent):
        return 1

    def data(self, index, role):
        if self.__sourceModel is None:
            return QtCore.QVariant()
        
        mIndex = self.modelIndex(index)
        row = mIndex.row()
        parent = mIndex.parent()

        return self.__sourceModel.data(self.__sourceModel.index(row, 0, parent), role)

    def flags(self, index):
        if self.__sourceModel is None or not index.isValid():  
            return QtCore.Qt.NoItemFlags
        flags = self.__sourceModel.flags(self.modelIndex(index))
        #Strip all writable flags and make sure we can select it
        return (flags & ~(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsUserCheckable)) | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
        
    def hasChildren(self, index):
        return False

    def index(self, row, column, parent):
        if self.hasIndex(row, column, parent):
            return self.createIndex(row, column)
        return QtCore.QModelIndex()

    def parent(self, index):
        return QtCore.QModelIndex()

    def rowCount(self, parent):
        return len(self.__indexMap)

    def modelIndex(self, proxyIndex):
        if proxyIndex.isValid():
            row = proxyIndex.row()
            if row < len(self.__indexMap):
                return self.__indexMap[row]
        return QtCore.QModelIndex()

    def reMapModel(self):
        if self.__sourceModel is not None:
            self.__indexMap = []
            self.mapModel(QtCore.QModelIndex())

        #self.emit("modelChanged()")
        self.layoutChanged.emit()

    def mapModel(self, parent):
        childCount = self.__sourceModel.rowCount(parent)
        for i in xrange(childCount):
            #First, map this one
            index = self.__sourceModel.index(i, 0, parent)
            if self.filterAcceptsRow(i, parent):
                self.__indexMap.append(index)
            #Map it's children
            self.mapModel(index)
