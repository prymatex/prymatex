#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import configparser

from prymatex.qt import QtCore, QtGui

from prymatex.core import PrymatexComponent
from prymatex.core import config

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

class Properties(object):
    def __init__(self, selector, dataHash):
        print(selector)
        self.selector = selector
        self.dataHash = dataHash

class PropertiesMaster(object):
    def __init__(self, properties):
        self.properties = properties

class PropertyManager(PrymatexComponent, QtCore.QObject):
    def __init__(self, **kwargs):
        super(PropertyManager, self).__init__(**kwargs)
        self._properties = {}
    
    def _fill_parser(self, parser, path):
        properties_path = os.path.join(path, config.PMX_PROPERTIES_NAME)
        if os.path.isfile(properties_path):
            with open(properties_path) as props:
                content = props.read()
                if content[0] != "[":
                    content = "[%s]\n%s" % (configparser.DEFAULTSECT, content)
                parser.read_string(content)

    def _load_parser(self, path):
        parser = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        parser.optionxform = str
        while True:
            self._fill_parser(parser, path)
            if path in (os.sep, config.USER_HOME_PATH):
                break
            path = os.path.dirname(path)
        if path != config.USER_HOME_PATH:
            self._fill_parser(parser, config.USER_HOME_PATH)
        return parser

    def _build_properites(self, path):
        parser = self._load_parser(path)
        return PropertiesMaster(
            [ Properties(section, parser[section]) \
                for section in parser.sections() \
                if section != configparser.DEFAULTSECT ]
        )

    def properties(self, path):
        path = os.path.isfile(path) and os.path.dirname(path) or path
        if path not in self._properties:
            self._properties[path] = self._build_properites(path)
        return self._properties[path]
