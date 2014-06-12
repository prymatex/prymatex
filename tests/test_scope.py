#!/usr/bin/env python

import unittest
from prymatex.support.scope import Scope, Context, Selector
from time import time

class ScopeSelectorTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_selector(self):
        self.assertEqual(Selector("source.python meta.function.python, source.python meta.class.python").does_match(Scope.factory("source.python meta.function.python")), True)

    def test_child_selector(self):
        self.assertEqual(Selector("foo fud").does_match(Scope.factory("foo bar fud")), True)
        self.assertEqual(Selector("foo > fud").does_match(Scope.factory("foo bar fud")), False)
        self.assertEqual(Selector("foo > foo > fud").does_match(Scope.factory("foo foo fud")), True)
        self.assertEqual(Selector("foo > foo > fud").does_match(Scope.factory("foo foo fud fud")), True)
        self.assertEqual(Selector("foo > foo > fud").does_match(Scope.factory("foo foo fud baz")), True)
        self.assertEqual(Selector("foo > foo fud > fud").does_match(Scope.factory("foo foo bar fud fud")), True)

    def test_mixed(self):
        self.assertEqual(Selector("^ foo > bar").does_match(Scope.factory("foo bar foo")), True)
        self.assertEqual(Selector("foo > bar $").does_match(Scope.factory("foo bar foo")), False)
        self.assertEqual(Selector("bar > foo $").does_match(Scope.factory("foo bar foo")), True)
        self.assertEqual(Selector("foo > bar > foo $").does_match(Scope.factory("foo bar foo")), True)
        self.assertEqual(Selector("^ foo > bar > foo $").does_match(Scope.factory("foo bar foo")), True)
        self.assertEqual(Selector("bar > foo $").does_match(Scope.factory("foo bar foo")), True)
        self.assertEqual(Selector("^ foo > bar > baz").does_match(Scope.factory("foo bar baz foo bar baz")), True)
        self.assertEqual(Selector("^ foo > bar > baz").does_match(Scope.factory("foo foo bar baz foo bar baz")), False)

    def test_anchor(self):
        self.assertEqual(Selector("^ foo").does_match(Scope.factory("foo bar")), True)
        self.assertEqual(Selector("^ bar").does_match(Scope.factory("foo bar")), False)
        self.assertEqual(Selector("^ foo").does_match(Scope.factory("foo bar foo")), True)
        self.assertEqual(Selector("foo $").does_match(Scope.factory("foo bar")), False)
        self.assertEqual(Selector("bar $").does_match(Scope.factory("foo bar")), True)

    def test_scope_selector(self):
        textScope = Scope("text.html.markdown meta.paragraph.markdown markup.bold.markdown")
        matchingSelectors = [
            Selector("text.* markup.bold"),
            Selector("text markup.bold"),
            Selector("markup.bold"),
            Selector("text.html meta.*.markdown markup"),
            Selector("text.html meta.* markup"),
            Selector("text.html * markup"),
            Selector("text.html markup"),
            Selector("text markup"),
            Selector("markup"),
            Selector("text.html"),
            Selector("text")
        ]
        lastRank = 1
        for selector in matchingSelectors:
            rank = []
            self.assertTrue(selector.does_match(textScope, rank))
            self.assertLessEqual(sum(rank), lastRank)
            lastRank = sum(rank)
        
        print(Selector("source.python.django").does_match(Scope.factory("source.python")))
        
    def test_context(self):
        selector = Selector("source & ((L:punctuation.section.*.begin & R:punctuation.section.*.end) | (L:punctuation.definition.*.begin & R:punctuation.definition.*.end)) - string")
        rank = []
        self.assertTrue(selector.does_match(Context(Scope.factory("source.python punctuation.definition.list.begin.python"), Scope.factory("source.python punctuation.definition.list.end.python")), rank))

    def test_fast_scope(self):
        selector = Selector("source & ((L:punctuation.section.*.begin & R:punctuation.section.*.end) | (L:punctuation.definition.*.begin & R:punctuation.definition.*.end)) - string")
        start = time()
        for _ in range(10000):
            scope = Scope("source.pythonpunctuation.definition.list.end.python")
            selector.does_match(scope)
            scope = Scope("text.html.markdown meta.paragraph.markdown markup.bold.markdown")
            selector.does_match(scope)
        print(time() - start)
        start = time()
        for _ in range(10000):
            scope = Scope.factory("source.pythonpunctuation.definition.list.end.python")
            selector.does_match(scope)
            scope = Scope.factory("text.html.markdown meta.paragraph.markdown markup.bold.markdown")
            selector.does_match(scope)
        print(time() - start)

    def test_none_selector(self):
        selector = Selector("")
        scope = Scope("source.pythonpunctuation.definition.list.end.python")
        print(selector.does_match(scope))

    def test_python_inside_strings(self):
        selector = Selector("source.python string.quoted.*.block - punctuation.definition.string.begin")
        rank = []
        self.assertTrue(selector.does_match(Context(Scope.factory("source.python string.quoted.double.block.python"), Scope.factory("source.python string.quoted.double.block.python")), rank))
        print(rank)