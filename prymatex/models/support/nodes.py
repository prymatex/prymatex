#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.qt.helpers import (keyequivalent_to_keysequence,
    keysequence_to_keyequivalent, rgba2color, color2rgba, qapplication)

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
        self._icon = None

    def bundleItem(self):
        return self.__bundleItem

    def uuid(self):
        return self.__bundleItem.uuidAsText()

    def __hash__(self):
        return hash(self.uuid())

    def keySequence(self):
        if hasattr(self.__bundleItem, "keyEquivalent") and isinstance(self.__bundleItem.keyEquivalent, six.string_types):
            return keyequivalent_to_keysequence(self.__bundleItem.keyEquivalent)
    
    def setIcon(self, icon):
        self._icon = icon

    def icon(self):
        return self._icon
        #return resources.get_icon("bundle-item-%s" % self.type())
    
    def trigger(self):
        trigger = []
        if self.__bundleItem.tabTrigger != None:
            trigger.append("%s⇥" % (self.__bundleItem.tabTrigger))
        if self.__bundleItem.keyEquivalent != None:
            trigger.append("%s" % self.keySequence().toString())
        return ", ".join(trigger)
    
    def buildBundleAccelerator(self):
        name = self.nodeName()
        for index, char in enumerate(name):
            if char in self.BANNED_ACCEL:
                continue
            char = char.lower()
            if not char in self.USED:
                self.USED.append(char)
                return name[0:index] + '&' + name[index:]
        return name
    
    def buildMenuTextEntry(self, mnemonic = True):
        text = self.nodeName()
        if mnemonic:
            text += "\t%s" % (self.trigger())
        return text.replace('&', '&&')
    
    def triggerItemAction(self, parent = None):
        """
        Build and return de QAction related to this bundle item.
        if bundle item haven't action is created whit the given parent, otherwise return None
        """
        if parent is not None:
            receiver = lambda checked, item = self: item.manager.bundleItemTriggered.emit(item)
            self._action = self.buildTriggerItemAction(parent, receiver)
            #Que la accion referencia a su nodo
            self._action.bundleTreeNode = self
            return self._action
        elif hasattr(self, "_action"):
            return self._action
    
    def buildTriggerItemAction(self, parent, receiver):
        action = QtWidgets.QAction(self.icon(), self.buildMenuTextEntry(), parent)
        action.triggered.connect(receiver)
        return action
    
    def update(self, dataHash):
        if 'keySequence' in dataHash and isinstance(dataHash['keySequence'], QtGui.QKeySequence):
            dataHash['keyEquivalent'] = keysequence_to_keyequivalent(dataHash['keySequence'])
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
    def styleItem(self):
        return self.__styleItem

    def uuid(self):
        return self.__styleItem.uuidAsText()

    # ----------- Style decorator -----------
    @property
    def scopeSelector(self):
        return self.__styleItem.scopeSelector

    def load(self, *args, **kwargs):
        return self.__styleItem.load(*args, **kwargs)

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
