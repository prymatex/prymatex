#!/usr/bin/env python

#-*- encoding: utf-8 -*-
import re
import os
import codecs
    
from prymatex.qt import QtCore, QtGui
from prymatex.utils import fnmatch

from . import regexp
from . import scope

class Settings(object):
    WELL_KNOWN_SETTINGS = ['binary', 'encoding', 'fileType', 'useBOM', 'softTabs',
        'lineEndings', 'theme', 'fontName', 'fontSize', 'showInvisibles', 'tabSize',
        'spellChecking', 'projectDirectory', 'windowTitle', 'scopeAttributes', 
        'wrapColumn', 'softWrap']
    def __init__(self, name, config):
        self.name = name
        self.config = config
        value = name.strip()
        if value[0] in ("'", '"') and value[0] == value[-1]:
            value = value[1:-1]
        self.pattern = value
        self.selector = scope.Selector(value)

    def _remove_quotes(self, value):
        return value[1:-1] if value and value[0] in ("'", '"') and value[0] == value[-1] else value

    def get_snippet(self, key, default=None):
        variables = { key: '' }
        value = self.config[self.name].get(key, fallback=default)
        if value is not None:
            value = self._remove_quotes(value)
            variables["CWD"] = self.config.source.name
            variables.update({ item[0]: self._remove_quotes(item[1]) \
                    for item in self.config[self.name].items() \
                    if item[0] not in self.WELL_KNOWN_SETTINGS \
                        and not item[0].isupper() \
                        and item[0] != key
            })
            variables[key] = regexp.Snippet(value).substitute(variables)
        return variables.get(key)

    def get_str(self, key, default=None):
        return self._remove_quotes(
            self.config[self.name].get(key, fallback=default)
        )

    def get_bool(self, key, default=None):
        return self.config[self.name].getboolean(key, fallback=default)

    def get_int(self, key, default=None):
        return self.config[self.name].getint(key, fallback=default)

    def get_variables(self, environment):
        variables = []
        env = environment.copy()
        env["CWD"] = self.config.source.name
        variables.extend(
            [ ( item[0], 
                regexp.Snippet(
                    self._remove_quotes(item[1])
                ).substitute(env)) \
                for item in self.config[self.name].items() if item[0].isupper() ]
        )
        return variables

class ContextSettings(object):
    BROWSER = {
        'excludes': {
            'files': [ "excludeFilesInBrowser", "excludeInBrowser", 
                "excludeFiles", "exclude" ],
            'directories': [ "excludeDirectoriesInBrowser", "excludeInBrowser",
                "excludeDirectories", "exclude" ]
        },
        'includes': {
            'files': [ "includeFilesInBrowser", "includeInBrowser",
                "includeFiles", "include" ],
            'directories': [ "includeDirectoriesInBrowser", "includeInBrowser",
                "includeDirectories", "include" ]
        }
    }

    def __init__(self, settings):
        self.settings = settings

    def _first(self, key, default=None, value_type='str'):
        for settings in self.settings:
            value = getattr(settings, "get_%s" % value_type)(key, default=None)
            if value:
                return value
        return default

    # TODO: el merge
    _merge = _first
        
    ### List of Settings
    ## I/O
    #* `binary` — If set for a file, file browser will open it with external program
    # when double clicked. Mainly makes sense when targetting specific globs.
    binary = property(lambda self: self._first("binary", value_type='bool'))
    
    # * `encoding` — Set to the file’s encoding. This will be used during save but
    # is also fallback during load (when file is not UTF-8). Load encodinng heuristic
    # is likely going to change.    
    encoding = property(lambda self: self._first("encoding"))
    
    # * `fileType` — The file type given as scope, e.g. `text.plain`.
    fileType = property(lambda self: self._first("fileType"))

    # * `useBOM` — Used during save to add BOM (for those who insist on putting BOMs
    # in their UTF-8 files).
    useBOM = property(lambda self: self._first("useBOM"))
    @property
    def lineEndings(self):
        value = self._first("lineEndings")
        return value and codecs.getdecoder("unicode_escape")(value)[0]

    ## Display
    # * `theme` — UUID of theme, presently unused but will be back, and should allow
    # name of theme as well (use _View → Themes_ to change theme — remember to install
    # the Themes bundle).
    theme = property(lambda self: self._first("theme"))
    fontName = property(lambda self: self._first("fontName"))
    fontSize = property(lambda self: self._first("fontSize", value_type='int'))
    showInvisibles = property(lambda self: self._first("showInvisibles", value_type='bool'))
    spellChecking = property(lambda self: self._first("spellChecking", value_type='bool'))
    softWrap = property(lambda self: self._first("softWrap", value_type='bool'))
    wrapColumn = property(lambda self: self._first("wrapColumn"))

    # * `softTabs`, `tabSize` — Presently can only be changed this way, but there
    # should be some memory added to Avian.    
    softTabs = property(lambda self: self._first("softTabs", value_type='bool'))
    tabSize = property(lambda self: self._first("tabSize", value_type='int'))

    ## Projects
    projectDirectory = property(lambda self: self._first("projectDirectory", value_type='snippet'))
    windowTitle = property(lambda self: self._first("windowTitle", value_type='snippet'))
    
    ## Other
    scopeAttributes = property(lambda self: self._first("scopeAttributes"))
    
    ## File Filtes
    # These are all globs and perhaps a bit arcane. (Note that the glob syntax
    # is documented in the built-in help system.)
    # The file browser, if it has a file, checks that file against the first
    # key with a value in this order: excludeFilesInBrowser, excludeInBrowser,
    # excludeFiles, exclude. If neither match, it then does the same with
    # include keys, and if one match, it is included.
    # The default include key is * (so no hidden files, although see the default
    # .tm_properties which include .htaccess and .tm_properties). The default
    # exclude key is the empty string (nothing matches).
    exclude = property(lambda self: self._merge("exclude", value_type='snippet'))
    excludeFiles = property(lambda self: self._merge("excludeFiles", value_type='snippet'))
    excludeDirectories = property(lambda self: self._merge("excludeDirectories", value_type='snippet'))
    excludeInBrowser = property(lambda self: self._merge("excludeInBrowser", value_type='snippet'))
    excludeInFolderSearch = property(lambda self: self._merge("excludeInFolderSearch", value_type='snippet'))
    excludeInFileChooser = property(lambda self: self._merge("excludeInFileChooser", value_type='snippet'))
    excludeFilesInBrowser = property(lambda self: self._merge("excludeFilesInBrowser", value_type='snippet'))
    excludeDirectoriesInBrowser = property(lambda self: self._merge("excludeDirectoriesInBrowser", value_type='snippet'))
    
    include = property(lambda self: self._merge("include", value_type='snippet'))
    includeFiles = property(lambda self: self._merge("includeFiles", value_type='snippet'))
    includeDirectories = property(lambda self: self._merge("includeDirectories", value_type='snippet'))
    includeInBrowser = property(lambda self: self._merge("includeInBrowser", value_type='snippet'))
    includeInFileChooser = property(lambda self: self._merge("includeInFileChooser", value_type='snippet'))
    includeFilesInBrowser = property(lambda self: self._merge("includeFilesInBrowser", value_type='snippet'))
    includeDirectoriesInBrowser = property(lambda self: self._merge("includeDirectoriesInBrowser", value_type='snippet'))
    includeFilesInFileChooser = property(lambda self: self._merge("includeFilesInFileChooser", value_type='snippet'))

    ## File Browsing
    fileBrowserGlob = property(lambda self: self._merge("fileBrowserGlob", default="*", value_type='snippet'))
    fileChooserGlob = property(lambda self: self._merge("fileChooserGlob", default="*", value_type='snippet'))

    def pathInBrowser(self, path):
        key = os.path.isdir(path) and "directories" or "files"
        excludes = [ pat for pat in 
            [ getattr(self, exclude) for exclude in self.BROWSER['excludes'][key] ]
            if pat is not None
        ]
        if any((fnmatch.fnmatch(path, pat) for pat in excludes)):
            return False
        includes = [ pat for pat in 
            [ getattr(self, include) for include in self.BROWSER['includes'][key] ]
            if pat is not None
        ]
        if any((fnmatch.fnmatch(path, pat) for pat in includes)):
            return True
        return True
                
    def shellVariables(self, environment):
        shellVariables = []
        for settings in self.settings:
            shellVariables = settings.get_variables(environment)
            if shellVariables:
                break
        return shellVariables

class Properties(object):
    def __init__(self, manager):
        self.settings = []
        self.configs = []
        self.manager = manager

    def buildSettings(self, path, context):
        settings = []
        for s in self.settings:
            rank = []
            if s.name == "DEFAULT" and s.config.source.exists:
                settings.append((0, s))
            elif s.pattern and fnmatch.fnmatch(path, s.pattern):
                settings.append((1, s))
            elif s.selector and s.selector.does_match(context, rank):
                settings.append((rank.pop(), s))
        settings.sort(key=lambda t: t[0], reverse=True)
        #print([(s[0], s[1].name, s[1].config.source.name) for s in settings])
        return ContextSettings([s[1] for s in settings])
    
    def load(self, configs):
        self.configs = configs
        self.settings = []
        for config in configs:
            self.settings += [ 
                Settings(section, config) for section in config.sections() + ["DEFAULT"] 
            ]
