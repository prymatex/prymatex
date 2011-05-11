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
    
class PMXBundleManager(object):
    ELEMENTS = ['Bundles', 'Support', 'Themes']
    DEFAULT = 'prymatex'
    VAR_PREFIX = 'PMX'
    BUNDLES = {}
    BUNDLE_ITEMS = {}
    THEMES = {}
    TAB_TRIGGERS = {}
    KEY_EQUIVALENTS = {}
    def __init__(self, disabled = [], deleted = []):
        self.namespaces = {}
        self.environment = {}
        self.disabled = disabled
        self.deleted = deleted
    
    def addNameSpace(self, name, path):
        self.namespaces[name] = {}
        for element in self.ELEMENTS:
            epath = join(path, element)
            if not exists(epath):
                continue
            if name == self.DEFAULT:
                var = "_".join([ self.VAR_PREFIX, element.upper(), 'PATH' ])
            else:
                var = "_".join([ self.VAR_PREFIX, name.upper(), element.upper(), 'PATH' ])
            self.namespaces[name][element] = self.environment[var] = epath
    
    def updateEnvironment(self, env):
        self.environment.update(env)

    @property
    def priority(self):
        ns = self.namespaces.keys()
        ns.remove(self.DEFAULT)
        return ns + [ self.DEFAULT ]
    
    #---------------------------------------------------
    # LOAD ALL SHIT
    #---------------------------------------------------
    def loadShit(self, callback = None):
        for ns in self.priority:
            self.loadThemes(ns)
            self.loadBundles(ns)
        for bundle in self.getAllBundles():
            self.populateBundle(bundle)

    #---------------------------------------------------
    # LOAD THEMES
    #---------------------------------------------------
    def loadThemes(self, namespace):
        if 'Themes' in self.namespaces[namespace]:
            paths = glob(join(self.namespaces[namespace]['Themes'], '*.tmTheme'))
            for path in paths:
                theme = PMXTheme.loadTheme(path, namespace)
                if theme == None:
                    continue
                if not self.hasTheme(theme.uuid):
                    self.addTheme(theme)

    #---------------------------------------------------
    # LOAD BUNDLES
    #---------------------------------------------------
    def loadBundles(self, namespace):
        if 'Bundles' in self.namespaces[namespace]:
            paths = glob(join(self.namespaces[namespace]['Bundles'], '*.tmbundle'))
            for path in paths:
                bundle = PMXBundle.loadBundle(path, namespace)
                if bundle == None:
                    continue
                bundle.disabled = bundle.uuid in self.disabled
                if bundle.uuid not in self.deleted and not self.hasBundle(bundle.uuid):
                    self.addBundle(bundle)

    #---------------------------------------------------
    # POPULATE BUNDLE AND LOAD BUNDLE ITEMS
    #---------------------------------------------------
    def populateBundle(self, bundle):
        bns = bundle.namespace
        nss = self.priority
        index = nss.index(bns)
        bundle.manager = self
        for ns in nss[index:]:
            bpath = join(self.namespaces[ns]['Bundles'], basename(bundle.path))
            # Search for support
            if bundle.support == None and exists(join(bpath, 'Support')):
                bundle.support = join(bpath, 'Support')
            for klass in BUNDLEITEM_CLASSES:
                files = reduce(lambda x, y: x + glob(y), [ join(bpath, klass.FOLDER, file) for file in klass.FILES ], [])
                for sf in files:
                    item = klass.loadBundleItem(sf, ns)
                    if item == None:
                        continue
                    if not self.hasBundleItem(item.uuid):
                        bundle.addBundleItem(item)

    def hasBundle(self, uuid):
        return uuid in self.BUNDLES

    def addBundle(self, bundle):
        self.BUNDLES[bundle.uuid] = bundle

    def getBundle(self, uuid):
        return self.BUNDLES[uuid]

    def getAllBundles(self):
        return self.BUNDLES.values()

    def hasBundleItem(self, uuid):
        return uuid in self.BUNDLE_ITEMS
        
    def addBundleItem(self, item):
        self.BUNDLE_ITEMS[item.uuid] = item
        if item.bundle.mainMenu != None:
            item.bundle.mainMenu[item.uuid] = item
        if item.tabTrigger != None:
            self.TAB_TRIGGERS.setdefault(item.tabTrigger, []).append(item)
        if item.keyEquivalent != None:
            #keyseq = buildKeyEquivalentCode(item.keyEquivalent)
            #self.KEY_EQUIVALENTS.setdefault(keyseq, []).append(item)
            self.KEY_EQUIVALENTS.setdefault(item.keyEquivalent, []).append(item)

    def getBundleItem(self, uuid):
        return self.BUNDLE_ITEMS[uuid]
    
    def hasTheme(self, uuid):
        return uuid in self.THEMES
    
    def addTheme(self, theme):
        self.THEMES[theme.uuid] = theme
        
    def getTheme(self, uuid):
        return self.THEMES[uuid]