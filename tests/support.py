#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
sys.path.append(os.path.abspath('..'))

def test_findPreferences(manager):
    settings = manager.getPreferenceSettings('text.html.textile markup.heading.textile')
    for key in settings.KEYS:
        print key, getattr(settings, key, None)

def test_snippet(manager):
    from prymatex.support.processor import PMXDebugSnippetProcessor
    from time import time
    snippet = manager.getBundleItem('659D189C-EC3E-4C4E-9377-B7F5F5216CBD')
    start = time()
    snippet.execute(PMXDebugSnippetProcessor())
    print "Time:", time() - start

text = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Hola mundo

esto es una preuba
"""
class Persona(object):
    pass'''
    
def test_syntax(manager):
    from prymatex.support.syntax import PMXSyntax
    from time import time
    from prymatex.gui.editor.processors.syntax import PMXProcessor
    from pprint import pprint
    syntax = manager.getSyntaxByScopeName('source.python')
    print syntax.scopeName
    #file = open(os.path.abspath('prymatex/gui/editor/codeedit.py'), 'r')
    start = time()
    processor = PMXProcessor()
    syntax.parse(text, processor)
    #syntax.parse(file.read(), processor)
    #file.close()
    pprint(processor.lines)
    print "Time:", time() - start

def test_creationAndDeleteBundle(manager):
    bundle = manager.createBundle('Diego')
    bundle.save()
    item = manager.createBundleItem('MiSnippet', 'snippet', bundle)
    item.save()
    manager.deleteBundle(bundle)

def test_bundleItemsCRUD(manager):
    items = manager.findBundleItems(name = "thon")
    for item in items:
        item = manager.updateBundleItem(item, tabTrigger = "cacho")
        print item.tabTrigger

def test_bundleItemsTemplates(manager):
    items = manager.findBundleItems(TYPE = "template")
    for item in items:
        for name in item.getFileNames():
            data = item.getFileContent(name)
            print name, data

def test_template(manager):
    for template in manager.TEMPLATES:
        manager.updateBundleItem(template)

def test_themes(manager):
    for theme in manager.getAllThemes():
        print theme.namespaces
    themes = manager.findThemes( name = 'Diego')
    theme = themes.pop()
    manager.updateTheme(theme, name = "Cacho")
        
def loadCallback(message):
    print message
    
if __name__ == "__main__":
    from prymatex.support.manager import PMXSupportPythonManager
    manager = PMXSupportPythonManager()
    manager.addNamespace('prymatex', os.path.abspath('../prymatex/share'))
    manager.addNamespace('user', os.path.abspath(os.path.join(os.path.expanduser('~'), '.prymatex')))
    manager.loadSupport(loadCallback)
    test_syntax(manager)
