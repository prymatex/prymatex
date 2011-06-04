'''
'''
from PyQt4.Qt import *
from prymatex.support.manager import PMXSupportManager
from prymatex.core.base import PMXObject
from prymatex.core.config import pmxConfigPorperty
from prymatex.gui.bundles.models import PMXBundleTreeModel, PMXBundleItemModel
from prymatex.gui.bundles.proxies import PMXBundleTreeProxyModel, PMXTemplateProxyModel

class PMXSupportModelManager(PMXSupportManager, PMXObject):
    #Settings
    shellVariables = pmxConfigPorperty(default = [], tm_name = u'OakShelVariables')
    deletedBundles = pmxConfigPorperty(default = [], tm_name = u'OakBundleManagerDeletedBundles')
    disabledBundles = pmxConfigPorperty(default = [], tm_name = u'OakBundleManagerDisabledBundles')
    
    class Meta:
        settings = 'Manager'
    
    def __init__(self):
        super(PMXSupportModelManager, self).__init__()
        self.configure()
        self.bundleTableModel = PMXBundleItemModel()
        self.bundleTreeModel = PMXBundleTreeModel(self)
        
        #Proxy
        self.bundleProxyTreeModel = PMXBundleTreeProxyModel()
        self.bundleProxyTreeModel.setSourceModel(self.bundleTreeModel)
        
        self.templateProxyModel = PMXTemplateProxyModel()
        self.templateProxyModel.setSourceModel(self.bundleTreeModel)
        
    def buildEnvironment(self):
        env = {}
        for var in self.shellVariables:
            if var['enabled']:
                env[var['variable']] = var['value']
        env.update(self.environment)
        return env

    #---------------------------------------------------
    # BUNDLE OVERRIDE INTERFACE 
    #---------------------------------------------------
    def addBundle(self, bundle):
        self.bundleTreeModel.addBundle(bundle)
        return PMXSupportManager.addBundle(self, bundle)

    #---------------------------------------------------
    # BUNDLEITEM OVERRIDE INTERFACE 
    #---------------------------------------------------
    def addBundleItem(self, item):
        self.bundleTreeModel.addBundleItem(item)
        self.bundleTableModel.appendBundleItemRow(item)
        return PMXSupportManager.addBundleItem(self, item)

    #---------------------------------------------------
    # THEME OVERRIDE INTERFACE
    #---------------------------------------------------
    def hasTheme(self, uuid):
        return PMXSupportManager.hasTheme(self, uuid)

    def addTheme(self, theme):
        return PMXSupportManager.addTheme(self, theme)

    def getTheme(self, uuid):
        return PMXSupportManager.getTheme(self, uuid)


    def getAllThemes(self):
        return PMXSupportManager.getAllThemes(self)


    def getAllTemplates(self):
        return PMXSupportManager.getAllTemplates(self)


    def getPreferences(self, scope):
        return PMXSupportManager.getPreferences(self, scope)

