'''
'''
from PyQt4.Qt import *
from prymatex.support.manager import PMXSupportManager
from prymatex.core.base import PMXObject
from prymatex.core.config import pmxConfigPorperty
from prymatex.gui.bundles.bundlemodel import PMXBundleItemModel



class PMXTableSupportManager(PMXSupportManager, PMXObject):
    '''
    
    '''
    bundleLoaded = pyqtSignal()
    bundleItemLoaded = pyqtSignal()
    class Meta:
        setting = 'Manager'
    
    shellVariables = pmxConfigPorperty(default = [], tm_name = u'OakShelVariables')
    deletedBundles = pmxConfigPorperty(default = [], tm_name = u'OakBundleManagerDeletedBundles')
    disabledBundles = pmxConfigPorperty(default = [], tm_name = u'OakBundleManagerDisabledBundles')
    
    def __init__(self):
        super(PMXTableSupportManager, self).__init__()
        self.configure()
        
        self.model = PMXBundleItemModel()

    def buildEnvironment(self):
        env = {}
        for var in self.shellVariables:
            if var['enabled']:
                env[var['variable']] = var['value']
        env.update(self.environment)
        return env
        
    def hasBundle(self, uuid):
        return PMXSupportManager.hasBundle(self, uuid)


    def addBundle(self, bundle):
        '''
        @todo: Update Bundle Tree hierachy
        '''
        return PMXSupportManager.addBundle(self, bundle)

    def getBundle(self, uuid):
        return PMXSupportManager.getBundle(self, uuid)

    def getAllBundles(self):
        return PMXSupportManager.getAllBundles(self)


    def hasBundleItem(self, uuid):
        
        return PMXSupportManager.hasBundleItem(self, uuid)


    def addBundleItem(self, item):
        self.model.appendBundleItemRow(item)
        return PMXSupportManager.addBundleItem(self, item)


    def getBundleItem(self, uuid):
        
        return PMXSupportManager.getBundleItem(self, uuid)


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

