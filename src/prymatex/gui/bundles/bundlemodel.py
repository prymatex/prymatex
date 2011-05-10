# encoding: utf-8

'''
Models and proxies for bundle data
'''

from prymatex.bundles import PMXBundle
from PyQt4.Qt import *
from prymatex.models.base import PMXTableBase, PMXTableField
from prymatex.models.delegates import PMXChoiceItemDelegate
from prymatex.gui.bundles.items import PMXBundleItemInstanceItem


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

class PMXBundleItemDelegate(QItemDelegate):
    # Just to try
    def createEditor(self, *largs):
        return QTextEdit()

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
                              type_ = type(instance).__class__.__name__,
                              name = instance.name,
                              tabTrigger = instance.tabTrigger,
                              keyEquivalent = instance.keyEquivalent,
                              scope = instance.scope,
                              #item = item,
                              )
    
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
    
    def get_by(self, **filter):
        ''' Returns a list of QStandardItems 
            I.E. get_by(uuid = 'aaa-bb-cc')
        ''' 
        f = QSortFilterProxyModel()
        f.setSourceModel(self)
        #f.set

class SortByKeysProxyModel(QSortFilterProxyModel):
    def __init__(self, **kwargs):
        pass
    
        

class PMXBundleManager(object):
    def __init__(self, bundles, bundleItems, themes):
        self.bundles = bundles
        self.bundleItems = bundleItems
        self.themes = themes
        
    def addBundle(self, bundle):
        self.bundles.appendBundleRow(bundle)
        
    def getBundle(self, uuid):
        return PMXBundleManager.BUNDLES[uuid]
    
    def addBundleItem(self, item):
        self.bundleItems.appendBundleItemRow(item)
    
    def getBundleItem(self, uuid):
        return PMXBundleManager.BUNDLES[uuid]
    
    def addTheme(self, theme):
        self.themes.appendBundleItemRow(theme)

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