from PyQt4 import QtCore, QtGui
from prymatex.ui.bundleselector import Ui_BundleSelector

class PMXBundleItemSelector(Ui_BundleSelector, QtGui.QDialog):
    '''
    This dialog allow the user to search through commands, snippets and macros in the current scope easily.
    An instance is hold in the main window and triggered with an action.
    '''
    def __init__(self, parent = None):
        super(PMXBundleItemSelector, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Dialog)
        self.model = QtGui.QStandardItemModel(self)
        self.proxy = QtGui.QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)
        self.tableBundleItems.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.tableBundleItems.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.tableBundleItems.setModel(self.proxy)
        
    def select(self, items):
        self.item = None
        self.items = items
        self.model.clear()
        self.lineFilter.clear()
        self.lineFilter.setFocus()
        for item in items:
            self.model.appendRow([ QtGui.QStandardItem(QtGui.QIcon(item.icon), item.name), QtGui.QStandardItem(item.trigger) ])
        self.exec_()
        return self.item
    
    def on_lineFilter_textChanged(self, text):
        regexp = QtCore.QRegExp("*%s*" % text, QtCore.Qt.CaseInsensitive, QtCore.QRegExp.Wildcard)
        self.proxy.setFilterRegExp(regexp)
    
    def on_tableBundleItems_activated(self, index):
        sIndex = self.proxy.mapToSource(index)
        self.item = self.items[sIndex.row()]
        self.accept()
        
    def on_tableBundleItems_doubleClicked(self, index):
        sIndex = self.proxy.mapToSource(index)
        self.item = self.items[sIndex.row()]
        self.accept()
        
    def on_lineFilter_returnPressed(self):
        index = self.proxy.index(0, 0)
        if index.isValid():
            sIndex = self.proxy.mapToSource(index)
            self.item = self.items[sIndex.row()]
            self.accept()