#!/usr/bin/env python
# -*- coding: utf-8 -*-

def test_font_strategy(font, strategy):
    return bool(font.styleStrategy() & strategy)