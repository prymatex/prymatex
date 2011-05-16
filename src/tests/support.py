
import os, sys
sys.path.append(os.path.abspath('..'))

def test_snippets():
    #bundle = PMXBundle.getBundleByName('LaTeX')
    bundle = PMXBundle.getBundleByName('HTML')
    errors = 0
    #for bundle in PMXBundle.BUNDLES.values():
    for snippet in bundle.snippets:
        try:
            if snippet.name.startswith("Special:"):
            #if snippet.name.startswith("belongs_to"):
                snippet.compile()
                snippet.resolve(indentation = "",
                                tabreplacement = "----",
                                environment = {"TM_CURRENT_LINE": "  ", "TM_SCOPE": "text.tex.latex string.other.math.block.environment.latex", "TM_SELECTED_TEXT": "uno\tdos\tcuatro\t"})
                print "-" * 10, " Bundle ", bundle.name, " Test ", snippet.name, " (", snippet.tabTrigger, ") ", "-" * 10
                print snippet.path
                print "Origin: ", len(snippet), snippet.next()
                print snippet, snippet.ends
                clon = snippet.clone()
                clon.write(0, "Un Capitulo Nuevo")
                print "Clone: ", len(clon), clon.next()
                print clon, clon.ends
        except Exception, e:
            print bundle.name, snippet.name, e
            errors += 1
            if "'ascii' codec can't encode" not in str(e):
                import sys, traceback
                traceback.print_exc()
                sys.exit(0)
    print errors
    
def test_syntaxes():
    from prymatex.bundles.syntax import PMXSyntax
    from time import time
    from prymatex.bundles.processor import PMXSyntaxProcessor
    syntax = PMXSyntax.getSyntaxesByName("Python")
    print syntax[0].hash
    file = open('../gui/editor/codeedit.py', 'r');
    start = time()
    syntax[0].parse(file.read(), PMXSyntaxProcessor())
    file.close()
    print "Time:", time() - start

def print_commands():
    before = []
    for bundle in PMXBundle.BUNDLES.values():
        for command in bundle.commands:
            if command.beforeRunningCommand != "nop":
                before.append(command.beforeRunningCommand)
    print before

def test_keys():
    from pprint import pprint
    pprint(PMXBundle.KEY_EQUIVALENTS)
    
def test_templates():
    DIRECTORY = os.path.join(os.path.expanduser('~'), 'workspace/')
    for template in PMXBundle.TEMPLATES:
        environment = template.buildEnvironment(directory = DIRECTORY)
        template.resolve(environment)

def test_bundle_elements():
    from pprint import pprint
    pprint(PMXBundle.BUNDLES)
    pprint(PMXBundle.TAB_TRIGGERS)
    pprint(PMXBundle.KEY_EQUIVALENTS)
    pprint(PMXBundle.KEY_SEQUENCE)
    pprint(PMXBundle.PREFERENCES)
    pprint(PMXBundle.TEMPLATES)

def test_preferences():
    settings = PMXBundle.getPreferenceSettings('source.c++')
    for key in settings.KEYS:
        print key, getattr(settings, key)

def test_macros():
    bundles = PMXBundle.BUNDLES.values()
    commands = []
    for bundle in bundles:
        for macro in bundle.macros:
            for command in macro.commands:
                c = command['command']
                if c not in commands:
                    commands.append(c)
    print commands
    
def test_queryItems():
    from prymatex.bundles.qtadapter import Qt
    print PMXBundle.getTabTriggerItem('class', 'source.python')
    print PMXBundle.getKeyEquivalentItem(Qt.CTRL + ord('H'), 'text.html')

def test_saveBundleItems():
    from prymatex.bundles import PMXBundle
    for bundle in PMXBundle.BUNDLES.values():
        bundle.save(base = os.path.join(os.path.expanduser('~'), 'Bundles'))

def test_SupportManager():
    from prymatex.support.manager import PMXSupportManager
    manager = PMXSupportManager()
    manager.addNamespace('prymatex', os.path.abspath('../bundles/prymatex'))
    manager.addNamespace('user', os.path.abspath(os.path.join(os.path.expanduser('~'), '.prymatex')))
    bundle = manager.createBundle('Diego')
    bundle.save()
    item = manager.createBundleItem('MiSnippet', 'snippet', bundle)
    item.save()
    manager.deleteBundle(bundle)
    
    #manager.loadSupport()
    #for bundle in manager.BUNDLES.values():
        #print bundle.buildEnvironment()
        
if __name__ == "__main__":
    test_SupportManager()