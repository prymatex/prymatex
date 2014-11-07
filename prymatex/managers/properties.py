#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import re
import configparser

from prymatex.qt import QtCore, QtGui

from prymatex.core import PrymatexComponent
from prymatex.core import config

from prymatex.support import scope
from prymatex.support.properties import *

from prymatex.utils.fnmatch import translate

class PropertyManager(PrymatexComponent, QtCore.QObject):
    def __init__(self, **kwargs):
        super(PropertyManager, self).__init__(**kwargs)
        self._parsers = {}
        self._properties = {}
    
    def _fill_parser(self, parser, path):
        properties_path = os.path.join(path, config.PMX_PROPERTIES_NAME)
        if os.path.isfile(properties_path):
            with open(properties_path) as props:
                content = props.read()
                if content[0] != "[":
                    content = "[%s]\n%s" % (configparser.DEFAULTSECT, content)
                parser.read_string(content)

    def _load_parser(self, directory):
        if directory not in self._parsers:
            path = directory
            parser = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
            parser.optionxform = str
            while True:
                self._fill_parser(parser, path)
                if path in (os.sep, config.USER_HOME_PATH):
                    break
                path = os.path.dirname(path)
            if path != config.USER_HOME_PATH:
                self._fill_parser(parser, config.USER_HOME_PATH)
            self._parsers[directory] = parser
        return self._parsers[directory]

    def _build_properites(self, path):
        directory = path if os.path.isdir(path) else os.path.dirname(path)
        parser = self._load_parser(directory)
        properties = [ Properties(scope.Selector(), parser.defaults()) ]
        for section in parser.sections():
            options = parser[section]
            selector = section.strip()
            if selector[0] in ("'", '"') and selector[0] == selector[-1]:
                selector = selector[1:-1]
            pattern = re.compile(translate(selector))
            selector = scope.Selector(selector)
            if pattern.search(path) or selector:
                properties.append(Properties(selector, options))
        return PropertiesMaster(properties)

    def properties(self, path):
        if path not in self._properties:
            self._properties[path] = self._build_properites(path)
        return self._properties[path]
