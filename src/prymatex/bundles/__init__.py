import os

# for run as main
# https://github.com/textmate
if __name__ == "__main__":
    import sys
    sys.path.append(os.path.abspath('../..'))

from glob import glob
from prymatex.bundles.macro import PMXMacro
from prymatex.bundles.syntax import PMXSyntax
from prymatex.bundles.snippet import PMXSnippet
from prymatex.bundles.preference import PMXPreference
from prymatex.bundles.command import PMXCommand, PMXDragCommand
from prymatex.bundles.template import PMXTemplate
from prymatex.bundles.base import PMXBundle, PMXMenuNode
from prymatex.bundles.theme import PMXTheme, PMXStyle
from prymatex.bundles.qtadapter import buildQTextFormat
from prymatex.core.config import PMX_THEMES_PATH, PMX_BUNDLES_PATH

#BundleItemName, BundlePattern, BundleItemClass
BUNDLEITEM_CLASSES = [ PMXSyntax, PMXSnippet, PMXMacro, PMXCommand, PMXPreference, PMXTemplate, PMXDragCommand ]

def load_prymatex_bundles(after_load_callback = None):
    paths = glob(os.path.join(PMX_BUNDLES_PATH, '*.tmbundle'))
    counter = 0
    total = len(paths)
    for path in paths:
        bundle = PMXBundle.loadBundle(path, BUNDLEITEM_CLASSES, 'pryamtex')
        if bundle and callable(after_load_callback):
            after_load_callback(counter = counter, 
                                total = total, 
                                name = bundle.name,
                                bundle = bundle)

        counter += 1
    return counter



def load_prymatex_themes(after_load_callback = None):
    paths = glob(os.path.join(PMX_THEMES_PATH, '*.tmTheme'))
    counter = 0
    total = len(paths)
    for path in paths:
        if callable(after_load_callback):
            after_load_callback(counter = counter, total = total, name = os.path.basename(path).split('.')[0])
        PMXTheme.loadTheme(path)
        counter += 1
    return counter