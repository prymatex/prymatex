#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .styles import loadStylesheets
from .media import load_media

def loadResources(resourcesPath):
    resources = {}
    # Load Media
    resources.update(load_media(resourcesPath))
    # Load Stylesheets
    resources.update(loadStylesheets(resourcesPath))
    return resources
