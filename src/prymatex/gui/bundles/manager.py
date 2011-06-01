'''
'''
from PyQt4.Qt import *
from prymatex.support.manager import PMXSupportManager
from prymatex.core.base import PMXObject
from prymatex.core.config import pmxConfigPorperty
from prymatex.gui.bundles.models import PMXBundleTreeModel, PMXBundleItemModel

class PMXTableSupportManager(PMXSupportManager, PMXObject):
    '''
    
    '''
    bundleLoaded = pyqtSignal()
    bundleItemLoaded = pyqtSignal()
    class Meta:
        settings = 'Manager'
    
    shellVariables = pmxConfigPorperty(default = [], tm_name = u'OakShelVariables')
    deletedBundles = pmxConfigPorperty(default = [], tm_name = u'OakBundleManagerDeletedBundles')
    disabledBundles = pmxConfigPorperty(default = [], tm_name = u'OakBundleManagerDisabledBundles')
    
    def __init__(self):
        super(PMXTableSupportManager, self).__init__()
        self.configure()
        self.bundleItemModel = PMXBundleItemModel()
        self.bundleModel = PMXBundleTreeModel(self)

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
        self.bundleModel.addBundle(bundle)
        return PMXSupportManager.addBundle(self, bundle)

    #---------------------------------------------------
    # BUNDLEITEM OVERRIDE INTERFACE 
    #---------------------------------------------------
    def addBundleItem(self, item):
        self.bundleModel.addBundleItem(item)
        self.bundleItemModel.appendBundleItemRow(item)
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

