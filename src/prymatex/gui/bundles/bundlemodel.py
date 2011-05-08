# encoding: utf-8

from PyQt4.Qt import *


class PMXCommonModel(QStandardItemModel):
    ELEMENTS = ()
    
    def __init__(self, parent = None):
        super(PMXCommonModel, self).__init__(0, #Rows
                                                 len(self.ELEMENTS), # Columns
                                                 parent
                                                 )
        self.fillHeaders()        
    
    def fillHeaders(self):
        if not self.ELEMENTS:
            raise Exception("ELEMENTS not defined for %s" % type(self))
        for i, element_name in enumerate(self.ELEMENTS):
            self.setHeaderData(i, Qt.Horizontal, element_name.title())
    
    def loadBundle(self, path):
        pass

class PMXBundleModel(PMXCommonModel):
    '''
    Store xxx.tmBundle/info.plist data
    '''
    ELEMENTS = (
                'uuid',
                'name',
                'description',
                'contactName',
                'contactMailRot13',
                )
    

class PMXBundleItemInstanceItem(QStandardItem):
    '''
    
    Create a superclass?
    '''
    def __init__(self, pmx_bundle_item):
        from prymatex.bundles.base import PMXBundleItem
        assert isinstance(pmx_bundle_item, PMXBundleItem)
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


class PMXBundleItemModel(PMXCommonModel):
    '''
    Stores Command, Syntax, Snippets, etc. information
    '''
    CUSTOM_ELEMENTS = (
                       'bundleUUID', # Reference
                       'path',
                       'namespace',
                       )
     
    PLIST_ELEMENTS = (
                'uuid',
                'type',
                'name',
                'tabTrigger',
                'keyEquivalent',
                'scope',
                'item', # Pointer to the PMXStuff object
                )
    ELEMENTS = CUSTOM_ELEMENTS + PLIST_ELEMENTS
    
   
    def appendBundleItemRow(self, instance):
        '''
        Appends a new row based on an instance
        @param instance A PMXCommand, PMXSnippet, PMXMacro instance
        @todo: Refactor
        '''
        from prymatex.bundles.base import PMXBundleItem
        elements = [
                    instance.bundle.uuid,
                    instance.path,
                    instance.namespace,
                    instance.uuid,
                    type(instance).__class__.__name__,
                    instance.name,
                    instance.tabTrigger,
                    instance.keyEquivalent,
                    instance.scope,
                    instance,
                    ]
        
    
    
        items = []
        for name, element in zip(self.ELEMENTS, elements) :
            #print name, element
            if element is None:
                    # None -> Null String
                items.append(QStandardItem(''))
            elif isinstance(element, PMXBundleItem):
                pass
            else:
                items.append(QStandardItem(element))
        #elements = map(QStandardItem, elements)
        
        
        self.appendRow(items)
    
    def appendRowFromBundle(self, pmx_bundle):
        '''
        PMXBundle
        @param pmx_bundle: A prymatex.budnles.PMXBundle instance
        '''
        from prymatex.bundles import PMXBundle
        assert isinstance(pmx_bundle, PMXBundle), "Unexpected %s argument" % type(pmx_bundle)
        
        for syntax in pmx_bundle.syntaxes:
            self.appendBundleItemRow(syntax)
            
        for snippet in pmx_bundle.snippets:
            self.appendBundleItemRow(snippet)
            
        for macro in pmx_bundle.macros:
            self.appendBundleItemRow(macro)
            
        for command in pmx_bundle.commands:
            self.appendBundleItemRow(command)
            
        for preference in pmx_bundle.preferences:
            self.appendBundleItemRow(preference)
            
        for template in pmx_bundle.templates:
            self.appendBundleItemRow(template)
        
            
if __name__ == "__main__":
    import sys
    a = QApplication(sys.argv)
    w = QTableView()
    model = PMXBundleItemModel()
    w.setModel(model)
    w.setGeometry(400, 100, 600, 480)
    w.resizeColumnsToContents()
    w.show()
    sys.exit(a.exec_()) 