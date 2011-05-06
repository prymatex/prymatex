import os

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

def load_prymatex_bundles(bundles_path, namespace, env = {}, after_load_callback = None):
    paths = glob(os.path.join(bundles_path, '*.tmbundle'))
    counter = 0
    total = len(paths)
    PMXBundle.BASE_ENVIRONMENT.update(env)
    for path in paths:
        bundle = PMXBundle.loadBundle(path, BUNDLEITEM_CLASSES, namespace)
        if bundle and callable(after_load_callback):
            after_load_callback(counter = counter, 
                                total = total, 
                                name = bundle.name,
                                bundle = bundle)

        counter += 1
    return counter

def load_prymatex_themes(themes_path, namespace, after_load_callback = None):
    paths = glob(os.path.join(themes_path, '*.tmTheme'))
    counter = 0
    total = len(paths)
    for path in paths:
        if callable(after_load_callback):
            after_load_callback(counter = counter, total = total, name = os.path.basename(path).split('.')[0])
        theme = PMXTheme.loadTheme(path, namespace)
        counter += 1
    return counter