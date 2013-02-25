#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
from ConfigParser import ConfigParser

from PyQt4 import QtGui

from colortrans import SHORT2RGB_DICT


class ColorScheme(object):
    SCHEMES = []
    CONFIG_KEYS = [ 'Background', 'BackgroundIntense',
                    'Color0', 'Color0Intense',
                    'Color1', 'Color1Intense',
                    'Color2', 'Color2Intense',
                    'Color3', 'Color3Intense',
                    'Color4', 'Color4Intense',
                    'Color5', 'Color5Intense',
                    'Color6', 'Color6Intense', 
                    'Color7', 'Color7Intense', 
                    'Foreground', 'ForegroundIntense']
    
    def __init__(self, name, settings = {}):
        self.name = name
        self.colormap = dict(map(lambda (key, rgb): (key, QtGui.QColor(rgb)), settings.iteritems()))


    def mapIndex(self, index, intense):
        return index + 12 if intense else index + 2


    def background(self, intense = False):
        return self.colormap[intense and 11 or 1]


    def setBackground(self, color, intense = False):
        self.colormap[intense and 11 or 1] = color
    
    
    def foreground(self, intense = False):
        return self.colormap[intense and 10 or 0]


    def setForeground(self, color, intense = False):
        self.colormap[intense and 10 or 0] = color


    def color(self, index, intense = False):
        if isinstance(index, int):
            lindex = self.mapIndex(index, intense)
            if lindex in self.colormap:
                return self.colormap[lindex]
            #is not local, go global colors
            if intense and 0 <= index <= 7:
                index += 8
            return QtGui.QColor("#" + SHORT2RGB_DICT[index])


    def setColor(self, index, color, intense = False):
        self.colormap[self.mapIndex(index, intense)] = color


    @classmethod
    def default(cls):
        default = ColorScheme("default")
        default.setBackground(QtGui.QColor("#000000"))
        default.setBackground(QtGui.QColor("#000000"), intense = True)
        default.setForeground(QtGui.QColor("#FFFFFF"))
        default.setForeground(QtGui.QColor("#FFFFFF"), intense = True)
        return default


    @classmethod
    def scheme(cls, name):
        schemes = filter(lambda scheme: scheme.name == name, cls.SCHEMES)
        if schemes:
            return schemes.pop()
        return cls.SCHEMES[0]


    @classmethod
    def loadSchemes(cls, schemesPath):
        cls.SCHEMES.append(cls.default())
        for fileName in glob.glob(pathname=os.path.join(schemesPath, "*.colorscheme")):
            config = ConfigParser()
            config.read(fileName)
            general = dict(config.items("General"))
            scheme = ColorScheme(general["description"])
            for name in cls.CONFIG_KEYS:
                index = -1
                color = config.get(name, "Color")
                if color.startswith("#"):
                    color = QtGui.QColor(color)
                elif color.index(",") != -1:
                    rgb = "".join(map(lambda v: "%02x" % int(v), color.split(",")))
                    color = QtGui.QColor("#" + rgb)
                elif len(color) in [6, 8]:
                    color = QtGui.QColor("#" + color)
                else:
                    color = QtGui.QColor()
                intense = name.rfind("Intense")
                if intense != -1:
                    name = name[:intense]
                if name.startswith("Color"):
                    name, index = name[:-1], int(name[-1])
                setter = getattr(scheme, "set%s" % name)
                if index != -1:
                    setter(index, color, intense != -1)
                else:
                    setter(color, intense != -1)
            cls.SCHEMES.append(scheme)
