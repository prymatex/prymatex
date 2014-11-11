#!/usr/bin/env python

#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

# List of Settings

## I/O

#* `binary` — If set for a file, file browser will open it with external program
# when double clicked. Mainly makes sense when targetting specific globs.

# * `encoding` — Set to the file’s encoding. This will be used during save but
# is also fallback during load (when file is not UTF-8). Load encodinng heuristic
# is likely going to change.

# * `fileType` — The file type given as scope, e.g. `text.plain`.

# * `useBOM` — Used during save to add BOM (for those who insist on putting BOMs
# in their UTF-8 files).

## Display

# * `theme` — UUID of theme, presently unused but will be back, and should allow
# name of theme as well (use _View → Themes_ to change theme — remember to install
# the Themes bundle).

# * `fontName`, `fontSize` — Name and size of font, e.g. `Menlo` and `13`.
# Presently these two keys are required to override font, but there will be a
# font option in the _View_ menu, so this is only for special requirements.

# * `showInvisibles` — Sets the initial value. Can also be changed via View menu.

# * `softTabs`, `tabSize` — Presently can only be changed this way, but there
# should be some memory added to Avian.

# * `spellChecking`, `spellingLanguage` — Enable/disable spelling and set language.
# The language is defined by Apple, I can extract a list (but depends on installed
# spell checkers).

## Projects

# * `projectDirectory` — the project directory, generally set to `$CWD` in a
# `.tm_properties` file at the root of the project. This affects
# `TM_PROJECT_DIRECTORY` and default folder for ⇧⌘F.
# * `windowTitle` — override the window title. The default is `$TM_DISPLAYNAME`
# but could e.g. be changed to `$TM_FIEPATH`. Should add a `$TM_SCM_BRANCH`.

## Other

# * `scopeAttributes` — The value is added to the scope of the current file.

## File Filtering Keys

# These are all globs and perhaps a bit arcane.
#
# The file browser, if it has a file, checks that file against the first key with a value in this order: `excludeFilesInBrowser`, `excludeInBrowser`, `excludeFiles`, `exclude`. If neither match, it then does the same with include keys, and if one match, it is included.
#
# The default include key is `*` (so no hidden files, although see the default `.tm_properties` which include `.htaccess` and `.tm_properties`). The default exclude key is the empty string (nothing matches).

# * `exclude`
# * `excludeFiles`
# * `excludeDirectories`
# * `excludeInBrowser`
# * `excludeInFolderSearch`
# * `excludeInFileChooser`
# * `excludeFilesInBrowser`
# * `excludeDirectoriesInBrowser`

# * `include`
# * `includeFiles`
# * `includeDirectories`
# * `includeInBrowser`
# * `includeInFileChooser`
# * `includeFilesInBrowser`
# * `includeDirectoriesInBrowser`
# * `includeFilesInFileChooser`

class Settings(object):
    def __init__(self, selector, section, config):
        self.selector = selector
        self.section = section
        self.config = config

    def get(self, key, default=None):
        return self.config.get(self.section, key, fallback=default, raw=True)

class ContextSettings(object):
    def __init__(self, settings):
        self.settings = settings

    def _first(self, key, default=None):
        for settings in self.settings:
            attr = settings.get(key, None)
            if attr is not None:
                return attr
        return default

## I/O
for attr in [ "binary", "encoding", "fileType", "useBOM", "lineEndings" ]:
    setattr(ContextSettings, attr, property(lambda self: self._first(attr)))

## Display
for attr in [ "theme", "fontName", "fontSize", "showInvisibles", "spellChecking" ]:
    setattr(ContextSettings, attr, property(lambda self: self._first(attr)))
    
## Projects
for attr in [ "projectDirectory", "windowTitle" ]:
    setattr(ContextSettings, attr, property(lambda self: self._first(attr)))

## Other
for attr in [ "scopeAttributes" ]:
    setattr(ContextSettings, attr, property(lambda self: self._first(attr)))

## File Filtering Keys
for attr in [ "exclude", "excludeFiles", "excludeDirectories", "excludeInBrowser",
    "excludeInFolderSearch", "excludeInFileChooser", "excludeFilesInBrowser",
    "excludeDirectoriesInBrowser", "include", "includeFiles", "includeDirectories",
    "includeInBrowser","includeInFileChooser", "includeFilesInBrowser",
    "includeDirectoriesInBrowser", "includeFilesInFileChooser" ]:
    setattr(ContextSettings, attr, property(lambda self: self._first(attr)))

class Properties(object):
    def __init__(self):
        self.settings = []

    def contextSettings(self, leftScope = None, rightScope = None):
        return ContextSettings([])
        
    def add(self, selector, section, config):
        self.settings.insert(0, Settings(selector, section, config))

    @staticmethod
    def buildSettings(settings):
        return ContextSettings(settings)
