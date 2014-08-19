#!/usr/bin/env python

import os

from prymatex.qt import QtCore, QtGui
from prymatex.qt.helpers import get_std_icon

from prymatex.utils import text
from prymatex.utils import six

from .media import load_media, default_media_mapper
from .stylesheets import load_stylesheets
from .sequences import ContextSequence

_fileIconProvider = QtGui.QFileIconProvider()

class Resource(dict):
    def __init__(self, name, path):
        self._name = name
        self._path = path
        self._mapper = default_media_mapper
        self._from_theme = QtGui.QIcon.fromTheme

    def name(self):
        return self._name

    def path(self):
        return self._path

    def find_source(self, name, sections = None):
        if sections is not None:
            sections = sections if isinstance(sections, (list, tuple)) else (sections, )
        else:
            sections = list(self.keys())
        for section in sections:
            if section in self and name in self[section]:
                return self[section].get(name)
    
    def get_image(self, index):
        path = self.find_section(index, ["Images", "Icons"])
        if path is not None:
            return QtGui.QPixmap(path)
        else:
            #Standard Icon
            return get_std_icon(index).pixmap(32)
        return QtGui.QPixmap()

    def get_icon(self, index):
        if index in self._mapper:
            index = self._mapper[index]
        if isinstance(index, six.string_types):
            if os.path.exists(index) and os.path.isabs(index):
                return _fileIconProvider.icon(QtCore.QFileInfo(index))
    	
            std = get_std_icon(index)
            if not std.isNull():
                return std
    
            path = self.find_source(index, ["Icons", "External"])
            if path is not None:
                return QtGui.QIcon(path)
            
            return self._from_theme(index)
        elif isinstance(index, six.integer_types):
            return _fileIconProvider.icon(index)
        return QtGui.QIcon()
    
    def get_sequence(self, context, name, default = None, description = None):
        description = description or text.camelcase_to_text(name)
        return ContextSequence(self, context, name, default, description)
    
    def set_theme(self, name):
        self._mapper = self.find_source(name, ["Mapping"]) or default_media_mapper
        theme = self.find_source(name, ["Themes"])
        if theme:
            if theme.type == "pix":
                # Pixmap
                QtGui.QIcon.setThemeName(theme.name)
                self._from_theme = QtGui.QIcon._fromTheme
            elif theme.type == "glyph":
                # Glyph
                glyph = self.find_source(name, ["Glyphs"])
                self._from_theme = glyph.icon

class ResourceProvider(object):
    def __init__(self, resources):
        self.resources = resources

    def sources(self):
        return self.resources[:]
                
    def get_image(self, index, fallback = None):
        fallback = fallback or QtGui.QPixmap()
        for res in self.resources:
            image = res.get_icon(index)
            if not image.isNull():
                return image
        return fallback
    
    def get_icon(self, index, fallback = None):
        fallback = fallback or QtGui.QIcon()
        for res in self.resources:
            icon = res.get_icon(index)
            if not icon.isNull():
                return icon
        return fallback

    def get_sequence(self, context, name, default = None, description = None):
        sequence = QtGui.QKeySequence()
        for res in self.resources:
            sequence = res.get_sequence(context, name, default, description)
            if not sequence.isEmpty():
                return sequence
        return sequence

    def _section(self, name):
        section = {}
        for res in reversed(self.resources):
            section.update(res[name])
        return section
        
    def get_themes(self):
        return self._section("Themes")

    def set_theme(self, name):
        for res in self.resources:
            res.set_theme(name)

    def get_stylesheets(self):
        return self._section("StyleSheets")

class ResourceManager(object):
    def __init__(self, **kwargs):
        super(ResourceManager, self).__init__(**kwargs)
        self.resources = {}
        self.providers = {}
        
    def add_source(self, name, path):
        res = Resource(name, path)
        res.update(load_media(path))
        res.update(load_stylesheets(path))
        self.resources[name] = res

    def get_provider(self, sources):
        if sources not in self.providers:
            resources = [ self.resources[name] for name in sources ]
            self.providers[sources] = ResourceProvider(resources)
        return self.providers[sources]

    def providerForClass(self, klass):
        sources = getattr(klass, "RESOURCES", tuple(self.resources.keys()) )
        return self.get_provider(sources)

    def install_icon_handler(self):
        QtGui.QIcon._fromTheme = QtGui.QIcon.fromTheme
        QtGui.QIcon.fromTheme = self.icon_from_theme

    def icon_from_theme(self, index):
        for res in self.resources.values():
            icon = res.get_icon(index)
            if not icon.isNull():
                return icon
        return QtGui.QIcon()
