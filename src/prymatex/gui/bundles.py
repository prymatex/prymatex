from PyQt4.Qt import *

import sys
if __name__ == '__main__':
    
    from os.path import *
    pth = abspath(dirname(__file__))
    sys.path.append(abspath(join(pth, '../..')))
    
import prymatex #@UnresolvedImport
from prymatex.core.config import settings
print settings.PMX_BUNDLES_PATH
from prymatex.bundles.base import PMXBundle
from prymatex.bundles import load_prymatex_bundles

class PMXBundleItem(QStandardItem):
    def __init__(self, bundle):
        self.bundle = bundle
        super(PMXBundleItem, self).__init__(self.bundle.name)
        self.appendRow(QStandardItem("Syntax"))
        self.appendRow(QStandardItem("Commands"))
        self.appendRow(QStandardItem("Menu"))
        self.appendRow(QStandardItem("Snippets"))
        
        
class PMXBundleModel(QStandardItemModel):
    #===========================================================================
    # Signals
    #===========================================================================
    bundleCountChanged = pyqtSignal(int)
    bundleInserted = pyqtSignal(PMXBundle) 
    bundleRemoved = pyqtSignal(PMXBundle)
    bundleChanged = pyqtSignal(PMXBundle)
    
    def __init__(self):
        super(PMXBundleModel, self).__init__()
        self.setHeaderData(0, Qt.Vertical, "Name")
    def addBundle(self, bundle = None, **kwargs):
        self.appendRow(PMXBundleItem(bundle))
    
    def loadBundles(self):
        ''' Load bundles '''
        def after_bundle_loaded(bundle = None, **kwargs):
            self.addBundle(bundle)
            QApplication.processEvents()
            
        load_prymatex_bundles(after_bundle_loaded)

def test():
    ap = QApplication([])
    w = QTreeView()
    w.show()
    m = PMXBundleModel()
    m.loadBundles()
    
    w.setModel(m)
    ap.exec_()
    
if __name__ == '__main__':
    sys.exit(test())