from PyQt4.Qt import *
class PMXBundleItemInstanceItem(QStandardItem):
    '''
    
    Create a superclass?
    '''
    def __init__(self, pmx_bundle_item):
        super(PMXBundleItemInstanceItem, self).__init__()
        from prymatex.bundles.base import PMXBundleItem
        if isinstance(pmx_bundle_item, PMXBundleItem):
            self.setData(pmx_bundle_item, Qt.EditRole)
            self.setData(unicode(pmx_bundle_item), Qt.DisplayRole)
        
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
