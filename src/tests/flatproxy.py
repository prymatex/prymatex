from PyQt4 import QtCore, QtGui

class PMXFlatBaseProxyModel(QtGui.QAbstractProxyModel):
    '''
        Proxy for create flat models from tree models
    '''
    def __init__(self, model = None, parent = None):
        super(FlatProxyModel, self).__init__(parent)
        self.mModelIndexMap = {}
        self.mModel = None
        if model is not None:
            self.setModel(model)

    def mapToSource(self, proxyIndex):
        return self.mModelIndexMap[proxyIndex.row()]
        
    def mapFromSource(self, sourceIndex):
        return self.mModelIndexMap.values().index(sourceIndex)
        
    def columnCount(self, parent):
        return 1

    def data(self, index, role):
        if self.mModel is None:
            return QtCore.QVariant()
        if role != QtCore.Qt.DisplayRole and role != QtCore.Qt.EditRole:
            return QtCore.QVariant()

        mIndex = self.modelIndex(index)
        row = mIndex.row()
        parent = mIndex.parent()

        return self.mModel.data(self.mModel.index(row, i, parent), role)

    def flags(self, index):
        if self.mModel is None or not index.isValid():  
            return QtCore.Qt.NoItemFlags
        flags = self.mModel.flags(self.modelIndex(index))
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

    def setModel(self, model):
        if model == self.mModel:
            return

        if self.mModel is not None:
            self.mModel.disconnect(self)

        self.mModelIndexMap = {}

        self.mModel = model
        self.remap()

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
        if self.mModel is not None:
            position = 0;
            self.mapModel(position, QtCore.QModelIndex())

            self.mModel.dataChanged.connect(self.slotDataChanged)
            self.mModel.layoutChanged.connect(self.slotLayoutChanged)

        #self.dataChanged.emit()
        self.layoutChanged.emit()

    def mapModel(self, pos, parent):
        childCount = self.mModel.rowCount(parent)
        for i in xrange(childCount):
            #First, map this one
            index = self.mModel.index(i, 0, parent)
            self.mModelIndexMap[pos] = index;
            pos += 1
            #Map it's children
            self.mapModel(pos, index);
