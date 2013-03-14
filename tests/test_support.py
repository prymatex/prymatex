#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest
from time import time
from pprint import pprint

from prymatex.support.manager import PMXSupportPythonManager
from prymatex.support.processor import PMXDebugSnippetProcessor, PMXDebugSyntaxProcessor
from prymatex.support.syntax import PMXSyntax

#https://github.com/textmate/textmate/blob/master/Applications/TextMate/about/Changes.md
class TestSupportFunctions(unittest.TestCase):

    def setUp(self):
        self.manager = PMXSupportPythonManager()
        self.manager.addNamespace('prymatex', os.path.abspath('./prymatex/share'))
        #self.manager.addNamespace('user', os.path.abspath(os.path.join(os.path.expanduser('~'), '.prymatex')))
        #self.manager.addNamespace('textmate', os.path.abspath('./textmate'))
        def loadCallback(message):
            pass
            #print message
        self.manager.loadSupport(loadCallback)

    def ttest_snippet(self):
        snippet = self.manager.getBundleItem('659D189C-EC3E-4C4E-9377-B7F5F5216CBD')
        start = time()
        processor = PMXDebugSnippetProcessor()
        snippet.execute(processor)
        print processor.text
        print "Time:", time() - start
        
    def test_syntax(self):
        syntax = self.manager.getSyntaxByScopeName('source.python')
        file = open(os.path.abspath('./prymatex/gui/codeeditor/editor.py'), 'r')
        start = time()
        processor = PMXDebugSyntaxProcessor()
        #syntax.parse("  #!/usr/bin/env python", processor)
        syntax.parse(file.read(), processor)
        file.close()
        tiempo = time() - start
        print "Tiempo: ", tiempo
            
    def ttest_preferences(self):
        settings = self.manager.getPreferenceSettings('text.html.textile markup.heading.textile')
        for attr in dir(settings):
            print attr, getattr(settings, attr, None)


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

