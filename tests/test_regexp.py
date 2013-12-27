#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

import unittest
from prymatex.support.regexp import SymbolTransformation, String

class RegexpTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_transformation_parsing(self):
        sources = [
            "class\s+([A-Za-z_][A-Za-z0-9_]*.+?\)?)(\:|$)/$1/g",
            "def\s+([A-Za-z_][A-Za-z0-9_]*\()(?:(.{,40}?\))|((.{40}).+?\)))(\:)/$1(?2:$2)(?3:$4\))/g",
            "[[:alpha:]]+|( )/(?1:_:\L$0)/g",
            "((.+)\..*)?/(?2:$2:Page Title)/",
            "(\A\s*,\s*\Z)|,?\s*([A-Za-z_][a-zA-Z0-9_]*)\s*(=[^,]*)?(,\s*|$)/(?2:\t\tself.$2 = $2\n)/g"
            
        ]
        for s in sources:
            self.assertEqual(s, str(SymbolTransformation(s)))
    
    def test_symbol_transformation(self):
        sources = [
            #"s/class\s+([A-Za-z_][A-Za-z0-9_]*.+?\)?)(\:|$)/$1/g",
            #"s/def\s+([A-Za-z_][A-Za-z0-9_]*\()(?:(.{,40}?\))|((.{40}).+?\)))(\:)/$1(?2:$2)(?3:$4…\))/g",
            #"s/^\\s*/CSS: /; s/\\s+/ /g",
            r's/\/\*\*\s*(.*?)\s*\*\//** $1 **/; s/\/\*.*?\*\*\//./; s/\/\*[^\*].*?[^\*]\*\///'
        ]
        for s in sources:
            trans = SymbolTransformation(s)
            print(u"%s" % trans)
            print(trans.transform("    def apply(self, pattern, text, flags):"))
            
    def test_transformation(self):
        trans = SymbolTransformation("(\A\s*,\s*\Z)|,?\s*([A-Za-z_][a-zA-Z0-9_]*)\s*(=[^,]*)?(,\s*|$)/(?2:\t\tself.$2 = $2\n)/g")
        print(trans.transform("uno, dos, tres"))
        
    def test_string(self):
        s = String("${PATH:+$PATH}/hola")
        print(s)
        