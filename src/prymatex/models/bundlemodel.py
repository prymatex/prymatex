# encoding: utf-8

from PyQt4.Qt import *

class PMXBundleModel(QStandardItemModel):
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
    
    def __init__(self, parent = None):
        super(PMXBundleModel, self).__init__(0, #Rows
                                                 len(self.ELEMENTS), # Columns
                                                 parent
                                                 )
        for i, element_name in enumerate(self.ELEMENTS):
            self.setHeaderData(i, Qt.Horizontal, element_name.title())
    

class PMXBundleItemModel(QStandardItemModel):
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
    
    def __init__(self, parent = None):
        super(PMXBundleItemModel, self).__init__(0, #Rows
                                                 len(self.ELEMENTS), # Columns
                                                 parent
                                                 )
        for i, element_name in enumerate(self.ELEMENTS):
            self.setHeaderData(i, Qt.Horizontal, element_name.title())
    
    def appendBundleRow(self, data, instance):
        '''
        Add
        '''
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
        elements = map(QStandardItem, elements)
        
        self.appendRow(elements)
              
            
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