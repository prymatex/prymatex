#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from prymatex.qt import QtGui, QtCore
from prymatex.qt.helpers import keyequivalent2keysequence, keysequence2keyequivalent, rgba2color, color2rgba

from prymatex import resources

from prymatex.models.trees import TreeNodeBase

from prymatex.utils import six

#====================================================
# Bundle Tree Node
#====================================================
class BundleItemTreeNode(TreeNodeBase):
    """Bundle tree node and bundle item decorator"""
    USED = []
    BANNED_ACCEL = ' \t'
    
    def __init__(self, bundleItem, nodeParent = None):
        TreeNodeBase.__init__(self, bundleItem.name, nodeParent)
        self.__bundleItem = bundleItem

    # ----------- Bundle Item attrs assessors -----------
    def __getattr__(self, name):
        return getattr(self.__bundleItem, name)

    def bundleItem(self):
        return self.__bundleItem

    # ----------- Bundle Item decoration -----------
    @property
    def keyEquivalent(self):
        if isinstance(self.__bundleItem.keyEquivalent, six.string_types):
            return keyequivalent2keysequence(self.__bundleItem.keyEquivalent)
    
    @property
    def icon(self):
        return resources.getIcon("bundle-item-%s" % self.TYPE)
    
    @property
    def trigger(self):
        trigger = []
        if self.tabTrigger != None:
            trigger.append("%s⇥" % (self.tabTrigger))
        if self.keyEquivalent != None:
            trigger.append("%s" % QtGui.QKeySequence(self.keyEquivalent).toString())
        return ", ".join(trigger)
    
    def buildBundleAccelerator(self):
        name = self.name
        for index, char in enumerate(name):
            if char in self.BANNED_ACCEL:
                continue
            char = char.lower()
            if not char in self.USED:
                self.USED.append(char)
                return name[0:index] + '&' + name[index:]
        return name
    
    def buildMenuTextEntry(self, mnemonic = True):
        text = self.name
        if mnemonic:
            text += "\t%s" % (self.trigger)
        return text.replace('&', '&&')
    
    def triggerItemAction(self, parent = None):
        """
        Build and return de QAction related to this bundle item.
        if bundle item haven't action is created whit the given parent, otherwise return None
        """
        if parent is not None:
            receiver = lambda item = self: item.manager.bundleItemTriggered.emit(item)
            self._action = self.buildTriggerItemAction(parent, receiver)
            #Que la accion referencia a su nodo
            self._action.bundleTreeNode = self
            return self._action
        elif hasattr(self, "_action"):
            return self._action
    
    def buildTriggerItemAction(self, parent, receiver):
        action = QtGui.QAction(self.icon, self.buildMenuTextEntry(), parent)
        parent.connect(action, QtCore.SIGNAL('triggered()'), receiver)
        return action
    
    def update(self, dataHash):
        if 'keyEquivalent' in dataHash and isinstance(dataHash['keyEquivalent'], six.integer_types):
            dataHash['keyEquivalent'] = keysequence2keyequivalent(dataHash['keyEquivalent'])
        self.__bundleItem.update(dataHash)
    
    def isEditorNeeded(self):
        return self.isTextInputNeeded() or self.producingOutputText()

    def isTextInputNeeded(self):
        if self.__bundleItem.TYPE == "command":
            return self.__bundleItem.input not in [ "none" ]
        return True

    def producingOutputText(self):
        # TODO Esta mal este nombre, porque puede producir salida en nuevos documentos pero no requerir entrada
        output = True
        if self.__bundleItem.TYPE == "command":
            output = output and self.__bundleItem.output not in [ "discard", "showAsTooltip" ] and\
                self.__bundleItem.output not in [ "showAsHTML" ] and\
                self.__bundleItem.output not in [ "createNewDocument", "openAsNewDocument" ] and\
                self.__bundleItem.outputLocation not in [ "newWindow", "toolTip" ]
        return output

#===============================================
# Bundle Menu Node
#===============================================
class BundleItemMenuTreeNode(TreeNodeBase):
    ITEM = 0
    SUBMENU = 1
    SEPARATOR = 2
    def __init__(self, name, nodeType, data = None, parent = None):
        TreeNodeBase.__init__(self, name, parent)
        self.data = data
        self.nodeType = nodeType

#====================================================
# Theme Table Row
#====================================================
class ThemeTableRow(object):
    """Theme and Style decorator"""
    def __init__(self, themeItem):
        self.__themeItem = themeItem
        self.STYLES_CACHE = {}

    # ----------- Theme attrs assessors -----------
    def __getattr__(self, name):
        return getattr(self.__themeItem, name)

    def themeItem(self):
        return self.__themeItem

    # ----------- Theme decoration -----------
    def settings(self):
        settings = dict([(key_value4[0], rgba2color(key_value4[1])) for key_value4 in [key_value for key_value in iter(self.__themeItem.settings().items()) if key_value[1].startswith('#')]])
        
        # Fix some color keys
        settings.setdefault('gutter', settings['background'])
        settings.setdefault('gutterForeground', settings['foreground'])
        
        # Fonts
        settings['fontStyle'] = self.__themeItem.settings()['fontStyle'].split() if 'fontStyle' in self.__themeItem.settings() else []
        return settings

    def update(self, dataHash):
        if 'settings' in dataHash:
            fontStyle = dataHash['settings'].pop('fontStyle', None)
            settings = dict([(key_value2[0], color2rgba(key_value2[1])) for key_value2 in dataHash['settings'].items()])
            if fontStyle is not None:
                settings['fontStyle'] = " ".join(fontStyle)
            dataHash['settings'] = settings
        self.__themeItem.update(dataHash)
    
    def clearCache(self):
        self.STYLES_CACHE = {}

    def getStyle(self, scopePath = None):
        if scopePath in self.STYLES_CACHE:
            return self.STYLES_CACHE[scopePath]
        base = {}
        base.update(self.settings())
        if scopePath is not None:
            styles = []
            for style in self.styles:
                rank = []
                if style.scopeSelector.does_match(scopePath, rank):
                    styles.append((rank.pop(), style))
            styles.sort(key = lambda t: t[0])
            for style in styles:
                base.update(style[1].settings())
        self.STYLES_CACHE[scopePath] = base
        return base

#====================================================
# Themes Styles Row
#====================================================
class ThemeStyleTableRow(object):
    """Theme and Style decorator"""
    def __init__(self, styleItem):
        self.__styleItem = styleItem

    # ----------- Item attrs assessors -----------
    def __getattr__(self, name):
        return getattr(self.__styleItem, name)

    def styleItem(self):
        return self.__styleItem

    # ----------- Item decoration -----------
    def settings(self):
        settings = dict([(key_value5[0], rgba2color(key_value5[1])) for key_value5 in [key_value1 for key_value1 in self.__styleItem.settings().items() if key_value1[1].startswith('#')]])
        
        # Fonts
        settings['fontStyle'] = self.__styleItem.settings()['fontStyle'].split() if 'fontStyle' in self.__styleItem.settings() else []
        return settings
    
    def update(self, dataHash):
        if 'settings' in dataHash:
            fontStyle = dataHash['settings'].pop('fontStyle', None)
            settings = dict([(key_value2[0], color2rgba(key_value2[1])) for key_value2 in dataHash['settings'].items()])
            if fontStyle is not None:
                settings['fontStyle'] = " ".join(fontStyle)
            dataHash['settings'] = settings
        self.__styleItem.update(dataHash)
