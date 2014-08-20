#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .styles import loadStyleSheets
from .media import load_media

def loadResources(resourcesPath):
    resources = {}
    # Load Media
    resources.update(load_media(resourcesPath))
    # Load StyleSheets
    resources.update(loadStyleSheets(resourcesPath))
    return resources
