#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from prymatex.qt import QtGui, QtCore
from prymatex.qt.helpers import keyequivalent_to_keysequence, keysequence_to_keyequivalent, rgba2color, color2rgba

from prymatex import resources

from prymatex.models.trees import TreeNodeBase

from prymatex.utils import six

from prymatex.support.bundleitem.theme import DEFAULT_THEME_SETTINGS

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
        self.STYLES_CACHE = {}

    # ----------- Bundle Item attrs assessors -----------
    def __getattr__(self, name):
        return getattr(self.__bundleItem, name)

    def __eq__(self, other):
        return self.uuid == other.uuid
        
    def __hash__(self):
        return hash(self.uuid)
    
    def bundleItem(self):
        return self.__bundleItem

    # ----------- Bundle Item decoration -----------
    def keySequence(self):
        if hasattr(self.__bundleItem, "keyEquivalent") and isinstance(self.__bundleItem.keyEquivalent, six.string_types):
            return keyequivalent_to_keysequence(self.__bundleItem.keyEquivalent)
    
    def keyCode(self):
        if hasattr(self.__bundleItem, "keyEquivalent") and isinstance(self.__bundleItem.keyEquivalent, six.string_types):
            return keyequivalent_to_keysequence(self.__bundleItem.keyEquivalent)
    
    def icon(self):
        return resources.get_icon("bundle-item-%s" % self.type())
    
    def trigger(self):
        trigger = []
        if self.tabTrigger != None:
            trigger.append("%s⇥" % (self.tabTrigger))
        if self.keyEquivalent != None:
            trigger.append("%s" % self.keySequence().toString())
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
            text += "\t%s" % (self.trigger())
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
        action = QtGui.QAction(self.icon(), self.buildMenuTextEntry(), parent)
        parent.connect(action, QtCore.SIGNAL('triggered()'), receiver)
        return action
    
    def update(self, dataHash):
        if 'keySequence' in dataHash and isinstance(dataHash['keySequence'], QtGui.QKeySequence):
            dataHash['keyEquivalent'] = keysequence_to_keyequivalent(int(dataHash['keySequence']))
        if 'settings' in dataHash and isinstance(dataHash['settings'], dict):
            settings = {}
            for key, value in dataHash['settings'].items():
                if isinstance(value, QtGui.QColor):
                    value = color2rgba(value)
                if key == 'fontStyle':
                    settings[key] = " ".join(value)
                settings[key] = value
            dataHash['settings'] = settings
        self.__bundleItem.update(dataHash)

    def dataHash(self):
        dataHash = self.dump(allKeys = True)
        dataHash["keySequence"] = self.keySequence()
        return dataHash

    # ----------- Theme decoration -----------
    def clearCache(self):
        self.STYLES_CACHE = {}

    def getStyle(self, scopePath = None):
        if scopePath in self.STYLES_CACHE:
            return self.STYLES_CACHE[scopePath]
        base = dict([(key_value[0], rgba2color(key_value[1])) for key_value in DEFAULT_THEME_SETTINGS.items() if key_value[1].startswith('#')])

        styles = []
        for style in self.__bundleItem.settings:
            rank = []
            if style.scopeSelector.does_match(scopePath, rank):
                styles.append((rank.pop(), style))
        styles.sort(key = lambda t: t[0])
        for style in styles:
            base.update(style[1].settings())
        self.STYLES_CACHE[scopePath] = base
        return base

    def isEditorNeeded(self):
        return self.isTextInputNeeded() or self.producingOutputText()

    def isTextInputNeeded(self):
        if self.__bundleItem.type() == "command":
            return self.__bundleItem.input not in [ "none" ]
        return True

    def producingOutputText(self):
        # TODO Esta mal este nombre, porque puede producir salida en nuevos documentos pero no requerir entrada
        output = True
        if self.__bundleItem.type() == "command":
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
# Themes Styles Row
#====================================================
class ThemeStyleTableRow(object):
    """Theme and Style decorator"""
    def __init__(self, styleItem):
        self.__styleItem = styleItem
        self.__settings = None             # Settings cache
        
    # ----------- Item attrs assessors -----------
    def __getattr__(self, name):
        return getattr(self.__styleItem, name)

    def styleItem(self):
        return self.__styleItem

    # ----------- Item decoration -----------
    def settings(self):
        if self.__settings is None:
            # Build cache
            self.__settings = {}
            for key, value in self.__styleItem.settings().items():
                if value.startswith('#'):
                    self.__settings[key] = rgba2color(value)
                if key == 'fontStyle':
                    self.__settings[key] = value.split()
        return self.__settings
    
    def update(self, dataHash):
        self.__settings = None              # Clean cache
        settings = {}
        for key, value in dataHash.get('settings', {}).items():
            if isinstance(value, QtGui.QColor):
                value = color2rgba(value)
            if key == 'fontStyle':
                settings[key] = " ".join(value)
        dataHash['settings'] = settings
        self.__styleItem.update(dataHash)
