#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

from collections import namedtuple

from prymatex.qt import QtGui

from prymatex.utils import encoding
from prymatex.widgets import glyph

from .utils import build_resource_key

__all__ = ["load_media", "default_media_mapper"]

IconTheme = namedtuple("IconTheme", "name type path")

def load_media(resourcesPath):
    resources = { "Images": {}, "Icons": {}, "Themes": {}, "Mapping": {}, "Glyphs": {}, "External": {} }
    # Load Icons
    iconsPath = os.path.join(resourcesPath, "Media", "Icons")
    if os.path.exists(iconsPath):
        for dirpath, dirnames, filenames in os.walk(iconsPath):
            for filename in filenames:
                iconPath = os.path.join(dirpath, filename)
                name = build_resource_key(iconPath[len(iconsPath):])
                resources["Icons"][name] = iconPath

    # Load Images
    imagesPath = os.path.join(resourcesPath, "Media", "Images")
    if os.path.exists(imagesPath):
        for dirpath, dirnames, filenames in os.walk(imagesPath):
            for filename in filenames:
                imagePath = os.path.join(dirpath, filename)
                name = build_resource_key(imagePath[len(imagesPath):])
                resources["Images"][name] = imagePath
                
    # Load Themes
    themesPaths = [ os.path.join(resourcesPath, "Media", "Themes") ] + QtGui.QIcon.themeSearchPaths()
    for themesPath in themesPaths:
        if not os.path.exists(themesPath):
            continue
        for name in os.listdir(themesPath):
            descriptor = os.path.join(themesPath, name, "index.theme")
            if os.path.exists(descriptor):
                resources["Themes"][name] = IconTheme(name, "pix", os.path.join(themesPath, name))
    
    # Load Glyphs
    glyphsNames = ["FontAwesome", "WebHostingHub-Glyphs"]
    for glyphNames in glyphsNames:
        gly = glyph.QtGlyph(glyphNames)
        resources["Glyphs"][gly.name()] = gly
        resources["Themes"][gly.name()] = IconTheme(gly.name(), "glyph", glyphNames)
    
    # Load Mapping
    mappingsPath = os.path.join(resourcesPath, "Media", "Mapping")
    if os.path.exists(mappingsPath):
        for mappingFileName in os.listdir(mappingsPath):
            name = os.path.splitext(mappingFileName)[0]
            file_content, _ = encoding.read(os.path.join(mappingsPath, mappingFileName))
            resources["Mapping"][name] = json.loads(file_content)

    return resources

default_media_mapper = {
    "copy": "edit-copy",
    "cut": "edit-cut",
    "paste": "edit-paste",
    "delete": "edit-delete",
    "close": "window-close",
    "save": "document-save",
    "save-as": "document-save-as",
    "open": "document-open",
    "next-tab": "go-next",
    "previous-tab": "go-previous",
    "bookmarks": "user-bookmarks",
    "jump-to-tab": "go-jump",
    "full-screen": "view-fullscreen",
    "last-edit-location": "go-last",
    "options": "preferences-other",
    "settings": "preferences-system",
    "selection": "edit-select-all",
    "settings-addons": "libpeas-plugin",
    "settings-edit": "document-page-setup",
    "settings-editor": "accessories-text-editor",
    "settings-files": "system-file-manager",
    "settings-general": "start-here",
    "settings-main-window": "start-here",
    "settings-network": "preferences-system-network",
    "settings-plugins": "system-software-install",
    "settings-project": "package-x-generic",
    "settings-shortcuts": "accessories-character-map",
    "settings-terminal": "utilities-terminal",
    "settings-theme": "preferences-desktop-theme",
    "settings-variables": "accessories-dictionary",
    "project": "package-x-generic",
    "sync": "reload",
    "custom-filters": "format-justify-left",
    "collapse-all": "zoom-out",
    "prymatex": ":/prymatex.png",
    "bundle-item-bundle": ":/bundles/bundle.png",
    "bundle-item-command": ":/bundles/commands.png",
    "bundle-item-dragcommand": ":/bundles/drag-commands.png",
    "bundle-item-macro": ":/bundles/macros.png",
    "bundle-item-preference": ":/bundles/preferences.png",
    "bundle-item-project": ":/bundles/project.png",
    "bundle-item-proxy": ":/bundles/template-files.png",
    "bundle-item-snippet": ":/bundles/snippets.png",
    "bundle-item-syntax": ":/bundles/languages.png",
    "bundle-item-template": ":/bundles/templates.png",
    "bundle-item-staticfile": ":/bundles/template-files.png",
    "editor-mode": ":/bullets/red.png",
    "porcess-not-running": ":/bullets/red.png",
    "porcess-running": ":/bullets/green.png",
    "porcess-starting": ":/bullets/yellow.png",
    "symbol-block": ":/bullets/violet.png",
    "symbol-class": ":/bullets/red.png",
    "symbol-context": ":/bullets/yellow.png",
    "symbol-function": ":/bullets/ligthblue.png",
    "symbol-typedef": ":/bullets/brown.png",
    "symbol-variable": ":/bullets/green.png",
    "read-documentation": "help-contents",
    "replace": "edit-find-replace",
    "about-prymatex": ":/prymatex.png",
    "about-qt": "help-about",
    "new-from-template": "text-x-generic-template"
}
