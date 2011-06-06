from PyQt4 import QtCore, QtGui

class PMXFlatBaseProxyModel(QtGui.QAbstractProxyModel):
    '''
        Proxy for create flat models from tree models
    '''
    def __init__(self, model = None, parent = None):
        super(PMXFlatBaseProxyModel, self).__init__(parent)
        self.mModelIndexMap = {}
        self.__sourceModel = None
        if model is not None:
            self.setSourceModel(model)

    def sourceModel(self):
        return self.__sourceModel
        
    def setSourceModel(self, model):
        if model == self.__sourceModel:
            return
        if self.__sourceModel is not None:
            self.__sourceModel.disconnect(self)
        self.mModelIndexMap = {}
        self.__sourceModel = model
        self.remap()

    def mapToSource(self, proxyIndex):
        return self.mModelIndexMap[proxyIndex.row()]
        
    def mapFromSource(self, sourceIndex):
        return self.mModelIndexMap.values().index(sourceIndex)
        
    def sort(self, column, order = QtCore.Qt.AscendingOrder):
        pass
        
    def lessThan(self, left, right):
        return True
        
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
        return len(self.mModelIndexMap)

    def modelIndex(self, proxyIndex):
        if proxyIndex.isValid():
            row = proxyIndex.row()
            if row in self.mModelIndexMap:
                return self.mModelIndexMap[row]
        return QtCore.QModelIndex()
        
    def slotDataChanged(self, row, index):
        self.remap()

    def slotLayoutChanged(self):
        self.remap();

    def remap(self):
        if self.__sourceModel is not None:
            position = 0;
            self.mapModel(position, QtCore.QModelIndex())

            self.__sourceModel.dataChanged.connect(self.slotDataChanged)
            self.__sourceModel.layoutChanged.connect(self.slotLayoutChanged)

        #self.emit("modelChanged()")
        #self.layoutChanged.emit()

    def mapModel(self, pos, parent):
        childCount = self.__sourceModel.rowCount(parent)
        for i in xrange(childCount):
            #First, map this one
            index = self.__sourceModel.index(i, 0, parent)
            self.mModelIndexMap[pos] = index;
            pos += 1
            #Map it's children
            self.mapModel(pos, index);
