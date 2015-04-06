#!/usr/bin/env python

#-*- encoding: utf-8 -*-
import re
import codecs
    
from prymatex.qt import QtCore, QtGui
from prymatex.utils.fnmatch import translate as fntranslate

from . import regexp

class Settings(object):
    WELL_KNOWN_SETTINGS = ['binary', 'encoding', 'fileType', 'useBOM', 'softTabs',
        'lineEndings', 'theme', 'fontName', 'fontSize', 'showInvisibles', 'tabSize',
        'spellChecking', 'projectDirectory', 'windowTitle', 'scopeAttributes', 
        'wrapColumn', 'softWrap']
    def __init__(self, name, properties):
        self.name = selector = name
        self.properties = properties
        if selector[0] in ("'", '"') and selector[0] == selector[-1]:
            selector = selector[1:-1]
        self.pattern = re.compile(fntranslate(selector))
        self.selector = self.properties.manager.selectorFactory(selector)

    def _remove_quotes(self, value):
        return value[1:-1] if value and value[0] in ("'", '"') and value[0] == value[-1] else value

    def sections(self):
        for config in self.properties.configs:
            section = self.name \
                if self.name in config.sections() \
                else 'DEFAULT'
            yield config.directory, config[section]

    def get_snippet(self, key, default=None):
        variables = { key: '' }
        for directory, section in self.sections():
            value = section.get(key, fallback=None)
            if value is not None:
                value = self._remove_quotes(value)
                variables["CWD"] = directory
                variables.update(dict(
                    ((item[0], self._remove_quotes(item[1])) \
                        for item in section.items() \
                        if item[0] not in self.WELL_KNOWN_SETTINGS \
                            and not item[0].isupper() \
                            and item[0] != key)
                ))
                variables[key] = regexp.Snippet(value).substitute(variables)
        return variables.get(key)
        
    def get_str(self, key, default=None):
        value = default
        for directory, section in self.sections():
            value = section.get(key, fallback=value)
        return self._remove_quotes(value)

    def get_bool(self, key, default=None):
        value = default
        for directory, section in self.sections():
            value = section.getboolean(key, fallback=value)
        return value

    def get_int(self, key, default=None):
        value = default
        for directory, section in self.sections():
            value = section.getint(key, fallback=value)
        return value

    def get_variables(self, environment):
        variables = []
        env = environment.copy()
        for directory, section in self.sections():
            env["CWD"] = directory
            variables.extend(
                [ ( item[0], 
                    regexp.Snippet(
                        self._remove_quotes(item[1])
                    ).substitute(env)) \
                    for item in section.items() if item[0].isupper() ]
            )
        return variables

class ContextSettings(object):
    def __init__(self, settings):
        self.settings = settings

    def _first(self, key, default=None, value_type='str'):
        for settings in self.settings:
            value = getattr(settings, "get_%s" % value_type)(key, default=None)
            if value:
                return value
        return default

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
    exclude = property(lambda self: self._first("exclude", value_type='snippet'))
    excludeFiles = property(lambda self: self._first("excludeFiles", value_type='snippet'))
    excludeDirectories = property(lambda self: self._first("excludeDirectories", value_type='snippet'))
    excludeInBrowser = property(lambda self: self._first("excludeInBrowser", value_type='snippet'))
    excludeInFolderSearch = property(lambda self: self._first("excludeInFolderSearch", value_type='snippet'))
    excludeInFileChooser = property(lambda self: self._first("excludeInFileChooser", value_type='snippet'))
    excludeFilesInBrowser = property(lambda self: self._first("excludeFilesInBrowser", value_type='snippet'))
    excludeDirectoriesInBrowser = property(lambda self: self._first("excludeDirectoriesInBrowser", value_type='snippet'))
    
    include = property(lambda self: self._first("include", value_type='snippet'))
    includeFiles = property(lambda self: self._first("includeFiles", value_type='snippet'))
    includeDirectories = property(lambda self: self._first("includeDirectories", value_type='snippet'))
    includeInBrowser = property(lambda self: self._first("includeInBrowser", value_type='snippet'))
    includeInFileChooser = property(lambda self: self._first("includeInFileChooser", value_type='snippet'))
    includeFilesInBrowser = property(lambda self: self._first("includeFilesInBrowser", value_type='snippet'))
    includeDirectoriesInBrowser = property(lambda self: self._first("includeDirectoriesInBrowser", value_type='snippet'))
    includeFilesInFileChooser = property(lambda self: self._first("includeFilesInFileChooser", value_type='snippet'))

    ## File Browsing
    fileBrowserGlob = property(lambda self: self._first("fileBrowserGlob", value_type='snippet'))
    fileChooserGlob = property(lambda self: self._first("fileChooserGlob", value_type='snippet'))

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
    
    def append(self, selector, section, configs):
        self.settings.append(Settings(selector, section, configs))

    def buildSettings(self, path, context):
        settings = []
        for s in self.settings:
            if s.pattern.search(path) or s.selector.does_match(context):
                settings.append(s)
        return ContextSettings(settings)
    
    def load(self, configs):
        self.configs = configs
        sections = set()
        for parser in configs:
            sections.update(parser.sections())
        self.settings = [ Settings(section.strip(), self) for section in sections ]
