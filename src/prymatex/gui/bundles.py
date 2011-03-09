#!/usr/bin/env python
# coding: utf-8

from PyQt4.Qt import *

import sys
if __name__ == '__main__':
    
    from os.path import *
    pth = abspath(dirname(__file__))
    sys.path.append(abspath(join(pth, '../..')))
    sys.path.append(abspath(join(pth, '..')))
    
import prymatex #@UnresolvedImport
from prymatex.core.config import settings
print settings.PMX_BUNDLES_PATH
from prymatex.bundles.base import PMXBundle
from prymatex.bundles import load_prymatex_bundles
import res_rc

SYNTAX_ICON = ":/bundles/resources/icons/language.png"
SNIPPET_ICON = ":/bundles/resources/icons/snippet.png"
COMMAND_ICON = ":/bundles/resources/icons/command.png"
PREFERENCE_ICON = ":/bundles/resources/icons/preference.png"
DRAG_ICON = ":/bundles/resources/icons/drag.png"
MENU_ICON = ":/bundles/resources/icons/menu.png"
BUNDLE_ICON = ":/bundles/resources/icons/bundle.png"
TEMPLATE_ICON = ":/bundles/resources/icons/template.png"

class PMXSyntaxItem(QStandardItem):
    def __init__(self, syntax):
        self.syntax = syntax
        super(PMXSyntaxItem, self).__init__(self.syntax.name)
        self.setIcon(QIcon(SYNTAX_ICON))
        
class PMXSnippetItem(QStandardItem):
    def __init__(self, snippet):
        self.snippet = snippet
        super(PMXSnippetItem, self).__init__(self.snippet.name)
        self.setIcon(QIcon(SNIPPET_ICON))
        
class PMXCommandItem(QStandardItem):
    def __init__(self, command):
        self.command = command
        super(PMXCommandItem, self).__init__(self.command.name)
        self.setIcon(QIcon(COMMAND_ICON))

class PMXTemplateItem(QStandardItem):
    def __init__(self, template):
        self.template = template
        super(PMXTemplateItem, self).__init__(self.template.name)
        self.setIcon(QIcon(TEMPLATE_ICON))

class PMXBundleItem(QStandardItem):
    def __init__(self, bundle):
        self.bundle = bundle
        super(PMXBundleItem, self).__init__(self.bundle.name)
        #if bundle.name == "Makefile":
        #    import ipdb; ipdb.set_trace()
        self.setIcon(QIcon(BUNDLE_ICON))
        self.populateChilds()
        
        
    def populateChilds(self):
        for syntax in self.bundle.syntaxes:
            self.appendRow(PMXSyntaxItem(syntax))
        
        for snippet in self.bundle.snippets:
            self.appendRow(PMXSnippetItem(snippet))
        
        for command in self.bundle.commands:
            self.appendRow(PMXCommandItem(command))
            
        for template in self.bundle.templates:
            self.appendRow(PMXTemplateItem(template))
                
        
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
        self.bundleInserted.emit(bundle)
    
    def loadBundles(self):
        ''' Load bundles '''
        def after_bundle_loaded(bundle = None, **kwargs):
            self.addBundle(bundle)
            QApplication.processEvents()
            
        load_prymatex_bundles(after_bundle_loaded)

def test():
    ''' 
    Popullate the model from prymatex bundle paths
    '''
    ap = QApplication([])
    w = QTreeView()
    #i = QPixmap(":/bundles/resources/icons/language.png")
    #print i.isNull()
    #w.setWindowIcon(QIcon(":/bundles/resources/icons/syntax.png"))
    w.show()
    m = PMXBundleModel()
    m.loadBundles()
    
    w.setModel(m)
    ap.exec_()


    
if __name__ == '__main__':
    sys.exit(test())
    
