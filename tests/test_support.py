#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest
from time import time
from pprint import pprint

from prymatex.support.manager import PMXSupportPythonManager
from prymatex.support.processor import PMXDebugSnippetProcessor, PMXDebugSyntaxProcessor
from prymatex.support.syntax import PMXSyntax
from prymatex.support.snippet import PMXSnippet

TEXT = """#!/usr/bin/env python

import pepe
#Comment
class Persona(object):
    pass
"""

#https://github.com/textmate/textmate/blob/master/Applications/TextMate/about/Changes.md
class TestSupportFunctions(unittest.TestCase):

    def setUp(self):
        self.manager = PMXSupportPythonManager()
        self.manager.addNamespace('prymatex', os.path.abspath('./prymatex/share'))
        self.manager.addNamespace('user', os.path.abspath(os.path.join(os.path.expanduser('~'), '.prymatex')))
        def loadCallback(message):
            pass
            #print message
        self.manager.loadSupport(loadCallback)

    def _test_snippet(self):
        pythonClassSnippet = self.manager.getBundleItem('659D189C-EC3E-4C4E-9377-B7F5F5216CBD')
        htmlInputSnippet = self.manager.getBundleItem('D8DCCC81-749A-4E2A-B4BC-D109D5799CAA')
        htmlBodySnippet = self.manager.getBundleItem('4905D47B-A08B-11D9-A5A2-000D93C8BE28')
        start = time()
        processor = PMXDebugSnippetProcessor()
        processor.env['TM_FILENAME'] = "cacho.html"
        pythonClassSnippet.execute(processor)
        htmlInputSnippet.execute(processor)
        htmlBodySnippet.execute(processor)
        print(processor.text)
        print("Time:", time() - start)
        
    def _test_syntax(self):
        syntax = self.manager.getSyntaxByScopeName('source.python')
        file = open(os.path.abspath('./prymatex/gui/codeeditor/editor.py'), 'r')
        processor = PMXDebugSyntaxProcessor(showOutput = False)
        #syntax.parse(TEXT, processor)
        text = file.read().decode('utf-8')
        file.close()
        for _ in range(10):
            start = time()
            syntax.parse(text, processor)
            tiempo = time() - start
            print("Tiempo: ", tiempo)
            
    def _test_preferences(self):
        settings = self.manager.getPreferenceSettings('text.html.textile markup.heading.textile')
        for attr in dir(settings):
            print(attr, getattr(settings, attr, None))

    def test_adhoc_snippet(self):
        snippet = 'def pepe(${3:self${2/([^,])?.*/(?1:, )/}${2:arg}}):\n\t${4/.+/"""/}${4:docstring for pepe}${4/.+/"""\n/}${4/.+/\t/}${0:pass}'
        bundle = self.manager.getBundleItem('659D189C-EC3E-4C4E-9377-B7F5F5216CBD').bundle
        snippet = self.manager.buildAdHocSnippet(snippet, bundle = bundle)
        processor = PMXDebugSnippetProcessor()
        snippet.execute(processor)
        print(processor.text)
        
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
        print(item.tabTrigger)

def test_bundleItemsTemplates(manager):
    items = manager.findBundleItems(TYPE = "template")
    for item in items:
        for name in item.getFileNames():
            data = item.getFileContent(name)
            print(name, data)

def test_template(manager):
    for template in manager.TEMPLATES:
        manager.updateBundleItem(template)

def test_themes(manager):
    for theme in manager.getAllThemes():
        print(theme.namespaces)
    themes = manager.findThemes( name = 'Diego')
    theme = themes.pop()
    manager.updateTheme(theme, name = "Cacho")

