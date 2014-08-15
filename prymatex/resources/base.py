#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex.utils import osextra

RESOURCES = {}
RESOURCES_READY = False

LICENSES = [
    'Apache License 2.0',
    'Artistic License/GPL',
    'Eclipse Public License 1.0',
    'GNU General Public License v2',
    'GNU General Public License v3',
    'GNU Lesser General Public License',
    'MIT License',
    'Mozilla Public License 1.1',
    'New BSD License',
    'Other Open Source',
    'Other'
]

def buildResourceKey(path):
    return "/".join(osextra.path.fullsplit(path))

def loadPrymatexResources(resourcesPath):
    global RESOURCES, RESOURCES_READY
    from .loader import loadResources
    from .media import get_icon
    if not RESOURCES_READY:
        RESOURCES = loadResources(resourcesPath)

        # Install
        QtGui.QIcon._fromTheme = QtGui.QIcon.fromTheme
        QtGui.QIcon.fromTheme = staticmethod(get_icon)
        RESOURCES_READY = True

def getResource(name, sections = None):
    global RESOURCES
    if sections is not None:
        sections = sections if isinstance(sections, (list, tuple)) else (sections, )
    else:
        sections = list(RESOURCES.keys())
    for section in sections:
        if section in RESOURCES and name in RESOURCES[section]:
            return RESOURCES[section].get(name)

def setResource(section, name, value):
    global RESOURCES
    RESOURCES.setdefault(section, {})[name] = value

def removeSection(name):
    global RESOURCES
    if name in RESOURCES:
        del RESOURCES[name]

def getSection(name):
    global RESOURCES
    return RESOURCES.setdefault(name, {})

# New names
find_resource = getResource
set_resource = setResource
get_section = getSection
del_section = removeSection

