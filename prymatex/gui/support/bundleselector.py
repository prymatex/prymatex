from PyQt4 import QtCore, QtGui
from prymatex.core.base import PMXObject
from prymatex.ui.bundleselector import Ui_BundleSelector

class PMXFilterBundleItem(QtGui.QSortFilterProxyModel):
    def filterAcceptsRow(self, sourceRow, sourceParent):
        regexp = self.filterRegExp()
        if regexp.isEmpty():
            return True
        index = self.sourceModel().index(sourceRow, 0, sourceParent)
        index = self.sourceModel().modelIndex(index)
        item = index.internalPointer()
        return QtCore.QString(item.name).contains(regexp)

    def filterAcceptsColumn(self, sourceColumn, sourceParent):
        return True

    def data(self, index, role):
        if self.sourceModel() is None:
            return QtCore.QVariant()
        
        if role == QtCore.Qt.DisplayRole:
            index = self.sourceModel().modelIndex(index)
            item = index.internalPointer()
            return item.buildMenuTextEntry()
        else:
            return self.sourceModel().data(index, role)
            
class PMXBundleItemSelector(Ui_BundleSelector, QtGui.QDialog, PMXObject):
    '''
    This dialog allow the user to search through commands, snippets and macros in the current scope easily.
    An instance is hold in the main window and triggered with an action.
    '''
    def __init__(self, parent = None):
        super(PMXBundleItemSelector, self).__init__(parent)
        self.setupUi(self)
        self.proxyFilteringModel = PMXFilterBundleItem()
        self.proxyFilteringModel.setSourceModel(self.pmxApp.supportManager.itemsProxyModel)
        self.listBundleItems.setModel(self.proxyFilteringModel)
    
    def on_lineFilter_textChanged(self, text):
        self.proxyFilteringModel.setFilterRegExp(QtCore.QRegExp(text))