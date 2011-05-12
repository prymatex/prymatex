# encoding: utf-8

'''
Models and proxies for bundle data
'''

from prymatex.support.bundle import PMXBundle
from PyQt4.Qt import *
from prymatex.models.base import PMXTableBase, PMXTableField
from prymatex.models.delegates import PMXChoiceItemDelegate
from prymatex.gui.bundles.items import PMXBundleItemInstanceItem
from prymatex.core.exceptions import APIUsageError


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
                              type_ = instance.TYPE,
                              name = instance.name,
                              tabTrigger = instance.tabTrigger,
                              keyEquivalent = instance.keyEquivalent,
                              scope = instance.scope,
                              #item = item,
                              )
    
    def _appendRowFromBundle(self, pmx_bundle):
        '''
        PMXBundle
        @param pmx_bundle: A prymatex.budnles.PMXBundle instance
        '''
        print "deperecated"
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
    
    def getProxyFilteringModel(self, **filter_kwargs):
        ''' Returns a list of QStandardItems 
            I.E. get_by(uuid = 'aaa-bb-cc')
        ''' 
        proxy = PMXBundeItemSimpleFilterProxyModel(self, **filter_kwargs)
        return proxy 
        

class PMXBundeItemSimpleFilterProxyModel(QSortFilterProxyModel):
    '''
    Filters
    '''
    def __init__(self, model, **filter_arguments):
        super(PMXBundeItemSimpleFilterProxyModel, self).__init__(self)
        self.sourceModel = model
        self.setSourceModel(self.sourceModel)
        self.filters = {}
        for key in filter_arguments:
            if not key in self.sourceModel._meta.field_names:
                raise APIUsageError("%s is not a valid field of %s" % (key, self.sourceModel))
            col_number = self.sourceModel._meta.col_number(key)
            self.filters[col_number] = filter_arguments[key]
        
    def filterAcceptsRow(self, row, parent):
        if not self.filters: 
            return self.resultsIfEmpty
            
        for col, value in self.filters:
            if self.data(self.index(row, col)).toPyObject() != value:
                return False
        return True
    
    _resultsIfEmpty = True
    @property
    def resultsIfEmpty(self):
        return self._resultsIfEmpty
    
    @resultsIfEmpty.setter
    def resultsIfEmpty(self, value):
        self._resultsIfEmpty = value
    
    def __setitem__(self, key, value):
        self.filters.update(key = value)
    
    def __getitem__(self, key):
        return self.filters.__getitem__(key)
    
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