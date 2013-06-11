#!/usr/bin/env python
# encoding: utf-8

import unittest
from prymatex.support.regexp import Transformation

class ScopeSelectorTests(unittest.TestCase):
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
            self.assertEqual(s, str(Transformation(s)))
    
    def test_symbol_transformation(self):
        sources = [
            "class\s+([A-Za-z_][A-Za-z0-9_]*.+?\)?)(\:|$)/$1/g",
            "def\s+([A-Za-z_][A-Za-z0-9_]*\()(?:(.{,40}?\))|((.{40}).+?\)))(\:)/$1(?2:$2)(?3:$4…\))/g",
        ]
        for s in sources:
            trans = Transformation(s)
            print(trans.transform("    def apply(self, pattern, text, flags):"))
            
    def test_transformation(self):
        trans = Transformation("(\A\s*,\s*\Z)|,?\s*([A-Za-z_][a-zA-Z0-9_]*)\s*(=[^,]*)?(,\s*|$)/(?2:\t\tself.$2 = $2\n)/g")
        print(trans.transform("uno, dos, tres"))
        