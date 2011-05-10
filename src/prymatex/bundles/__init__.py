from os.path import join, abspath, basename, exists

# for run as main
# https://github.com/textmate
if __name__ == "__main__":
    import sys
    sys.path.append(os.path.abspath('../..'))

from glob import glob
from prymatex.bundles.macro import PMXMacro
from prymatex.bundles.syntax import PMXSyntax
from prymatex.bundles.processor import PMXSyntaxProcessor, PMXCommandProcessor, PMXMacroProcessor
from prymatex.bundles.snippet import PMXSnippet
from prymatex.bundles.preference import PMXPreference, PMXPreferenceSettings
from prymatex.bundles.command import PMXCommand, PMXDragCommand
from prymatex.bundles.template import PMXTemplate
from prymatex.bundles.base import PMXBundle, PMXMenuNode
from prymatex.bundles.theme import PMXTheme, PMXStyle
from prymatex.bundles.qtadapter import buildQTextFormat

BUNDLEITEM_CLASSES = [ PMXSyntax, PMXSnippet, PMXMacro, PMXCommand, PMXPreference, PMXTemplate, PMXDragCommand ]

def load_bundles(bundles_path, namespace, manager, after_load_callback = None):
    paths = glob(join(bundles_path, '*.tmbundle'))
    counter = 0
    total = len(paths)
    for path in paths:
        bundle = PMXBundle.loadBundle(path, namespace)
        if bundle == None:
            continue
        
        # Me fijo si no esta cargado en el  manager
        uuid = bundle.uuid
        if manager.hasBundle(uuid)
            bundle = manager.getBundle(uuid)
        else:
            manager.addBundle(bundle)
            
        # Cargo el support path de existir en esta ruta
        support = join(path, 'Support')
        if exists(support):
            bundle.support = support

        #Disabled?
        if not bundle.disabled:
            load_bundle_items(bundle, namespace)
        
        if bundle and callable(after_load_callback):
            after_load_callback(counter = counter, 
                                total = total, 
                                name = bundle.name,
                                bundle = bundle)

        counter += 1
    return counter

def load_bundle_items(bundles, namespace, after_load_callback = None):
    for klass in BUNDLEITEM_CLASSES:
        files = reduce(lambda x, y: x + glob(y), [ abspath(join(bundle.path, klass.FOLDER, file)) for file in klass.FILES ], [])
        for sf in files:
            try:
                item = klass.loadBundleItem(sf, namespace)
                if item == None:
                    continue
                bundle.addBundleItem(item)
            except Exception, e:
                print "Error in %s for %s (%s)" % (klass.__name__, sf, e)
    
def load_themes(themes_path, namespace, after_load_callback = None):
    paths = glob(join(themes_path, '*.tmTheme'))
    counter = 0
    total = len(paths)
    for path in paths:
        if callable(after_load_callback):
            after_load_callback(counter = counter, total = total, name = basename(path).split('.')[0])
        theme = PMXTheme.loadTheme(path, namespace)
        counter += 1
    return counter
    
class PMXBundleManager(object):
    BUNDLES = {}
    BUNDLE_ITEMS = {}
    THEMES = {}
    TAB_TRIGGERS = {}
    KEY_EQUIVALENTS = {}
    BASE_ENVIRONMENT = {}
    def __init__(self, disabled = [], env = {}):
        self.BASE_ENVIRONMENT = env
        self.disabled = disabled
    
    def updateEnvironment(self, env):
        self.BASE_ENVIRONMENT.update(env)
        
    def addBundle(self, bundle):
        self.BUNDLES[bundle.uuid] = bundle
        bundle.manager = self
        
    def getBundle(self, uuid):
        return self.BUNDLES[uuid]
    
    def hasBundle(self, uuid):
        return uuid in self.BUNDLES
    
    def addBundleItem(self, item):
        self.BUNDLE_ITEMS[item.uuid] = item
        if item.bundle.mainMenu != None:
            item.bundle.mainMenu[item.uuid] = item
        if item.tabTrigger != None:
            self.TAB_TRIGGERS.setdefault(item.tabTrigger, []).append(item)
        if item.keyEquivalent != None:
            keyseq = buildKeyEquivalentCode(item.keyEquivalent)
            self.KEY_EQUIVALENTS.setdefault(keyseq, []).append(item)
    
    def getBundleItem(self, uuid):
        return self.BUNDLE_ITEMS[uuid]
    
    def addTheme(self, theme):
        self.THEMES[theme.uuid] = theme
        
    def getTheme(self, uuid):
        return self.THEMES[uuid]