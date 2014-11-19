#!/usr/bin/env python

#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

# List of Settings

## I/O

## Display


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
    def __init__(self, selector, section, configs):
        self.selector = selector
        self.section = section
        self.configs = configs
    
    def _remove_quotes(self, value):
        return value[1:-1] if value and value[0] in ("'", '"') and value[0] == value[-1] else value

    def get_str(self, key, default=None):
        value = default
        for config in self.configs[::-1]:
            value = config.get(self.section, key, fallback=value, raw=True)
        return self._remove_quotes(value)

    def get_bool(self, key, default=None):
        value = default
        for config in self.configs[::-1]:
            value = config.getboolean(self.section, key, fallback=value, raw=True)
        return value

    def get_int(self, key, default=None):
        value = default
        for config in self.configs[::-1]:
            value = config.getint(self.section, key, fallback=value, raw=True)
        return value

    def shellVariables(self):
        variables = []
        for config in self.configs[::-1]:
            for name in config[self.section]:
                if name.isupper():
                    value = self._remove_quotes(config[self.section][name])
                    variables.append((name, value))
        return variables

class ContextSettings(object):
    def __init__(self, settings):
        self.settings = settings

    def _first(self, key, default=None, value_type=str):
        for settings in self.settings:
            value = getattr(settings, "get_%s" % value_type.__name__)(key, default=None)
            if value:
                return value
        return default

    ## I/O
    #* `binary` — If set for a file, file browser will open it with external program
    # when double clicked. Mainly makes sense when targetting specific globs.
    binary = property(lambda self: self._first("binary", value_type=bool))
    
    # * `encoding` — Set to the file’s encoding. This will be used during save but
    # is also fallback during load (when file is not UTF-8). Load encodinng heuristic
    # is likely going to change.    
    encoding = property(lambda self: self._first("encoding"))
    
    # * `fileType` — The file type given as scope, e.g. `text.plain`.
    fileType = property(lambda self: self._first("fileType"))

    # * `useBOM` — Used during save to add BOM (for those who insist on putting BOMs
    # in their UTF-8 files).
    useBOM = property(lambda self: self._first("useBOM"))
    lineEndings = property(lambda self: self._first("lineEndings"))

    ## Display
    # * `theme` — UUID of theme, presently unused but will be back, and should allow
    # name of theme as well (use _View → Themes_ to change theme — remember to install
    # the Themes bundle).
    theme = property(lambda self: self._first("theme"))
    fontName = property(lambda self: self._first("fontName"))
    fontSize = property(lambda self: self._first("fontSize", value_type=int))
    showInvisibles = property(lambda self: self._first("showInvisibles", value_type=bool))
    spellChecking = property(lambda self: self._first("spellChecking", value_type=bool))

    # * `softTabs`, `tabSize` — Presently can only be changed this way, but there
    # should be some memory added to Avian.    
    softTabs = property(lambda self: self._first("softTabs", value_type=bool))
    tabSize = property(lambda self: self._first("tabSize", value_type=int))

    ## Projects
    projectDirectory = property(lambda self: self._first("projectDirectory"))
    windowTitle = property(lambda self: self._first("windowTitle"))
    
    ## Other
    scopeAttributes = property(lambda self: self._first("scopeAttributes"))
    
    ## File Filtering Keys
    exclude = property(lambda self: self._first("exclude"))
    excludeFiles = property(lambda self: self._first("excludeFiles"))
    excludeDirectories = property(lambda self: self._first("excludeDirectories"))
    excludeInBrowser = property(lambda self: self._first("excludeInBrowser"))
    excludeInFolderSearch = property(lambda self: self._first("excludeInFolderSearch"))
    excludeInFileChooser = property(lambda self: self._first("excludeInFileChooser"))
    excludeFilesInBrowser = property(lambda self: self._first("excludeFilesInBrowser"))
    excludeDirectoriesInBrowser = property(lambda self: self._first("excludeDirectoriesInBrowser"))
    
    include = property(lambda self: self._first("include"))
    includeFiles = property(lambda self: self._first("includeFiles"))
    includeDirectories = property(lambda self: self._first("includeDirectories"))
    includeInBrowser = property(lambda self: self._first("includeInBrowser"))
    includeInFileChooser = property(lambda self: self._first("includeInFileChooser"))
    includeFilesInBrowser = property(lambda self: self._first("includeFilesInBrowser"))
    includeDirectoriesInBrowser = property(lambda self: self._first("includeDirectoriesInBrowser"))
    includeFilesInFileChooser = property(lambda self: self._first("includeFilesInFileChooser"))

    # Shell Variables
    @property
    def shellVariables(self):
        shellVariables = []
        for settings in self.settings:
            shellVariables.extend(settings.shellVariables())
        return shellVariables

class Properties(object):
    def __init__(self):
        self.settings = []
    
    def add(self, selector, section, config):
        self.settings.insert(0, Settings(selector, section, config))

    @staticmethod
    def buildSettings(settings):
        return ContextSettings(settings)
