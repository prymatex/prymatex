#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import unittest

from prymatex.utils import text

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        pass
    
    def test_subsearch(self):
        s1 = "foobar"
        s2 = "barfoo bar"
        self.assertEqual(text.subsearch("a", s2), [ (0,1,1,2) ])
        self.assertEqual(text.subsearch(s1, s2), [ (0,3,3,6), (3, 6, 7, 10) ])
        index = None
        slices = []
        for m in text.subsearch(s1, s2):
            slices.append(s2[index:m[2]])
            slices.append(s1[m[0]:m[1]])
            index = m[3]
        self.assertEqual(slices, ['bar', 'foo', ' ', 'bar'])
        self.assertFalse(text.subsearch(s1.upper(), s2))
        self.assertTrue(text.subsearch(s1.upper(), s2, ignoreCase = True))
    
    def test_subsearch2(self):
        s1 = "assertequal"
        s2 = "Assert Not Equal"
        index = None
        slices = []
        for m in text.subsearch(s1, s2, ignoreCase = True):
            slices.append(s2[index:m[2]])
            slices.append(s2[m[2]:m[3]])
            index = m[3]
        self.assertEqual(slices, ['', 'Assert', ' Not ', 'Equal'])
        
    def test_subsearch3(self):
        s1 = "assnqua"
        s2 = "Assert Not Equal"
        index = None
        slices = []
        for m in text.subsearch(s1, s2, ignoreCase = True):
            slices.append(s2[index:m[2]])
            slices.append(s2[m[2]:m[3]])
            index = m[3]
