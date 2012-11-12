#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore
from prymatex.qt.helpers import keyequivalent2keysequence, keysequence2keyequivalent, rgba2color, color2rgba

from prymatex import resources

from prymatex.models.trees import TreeNodeBase

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

    def __getattr__(self, name):
        # Quitar esta cosa fea
        return getattr(self.__bundleItem, name)

    def bundleItem(self):
        return self.__bundleItem

    # ----------- Item decoration -----------
    @property
    def keyEquivalent(self):
        if self.__bundleItem.keyEquivalent is not None:
            return keyequivalent2keysequence(self.__bundleItem.keyEquivalent)
    
    @property
    def icon(self):
        return resources.getIcon("bundle-item-%s" % self.TYPE)
    
    @property
    def trigger(self):
        trigger = []
        if self.tabTrigger != None:
            trigger.append(u"%s⇥" % (self.tabTrigger))
        if self.keyEquivalent != None:
            trigger.append(u"%s" % QtGui.QKeySequence(self.keyEquivalent).toString())
        return ", ".join(trigger)
    
    def buildBundleAccelerator(self):
        name = unicode(self.name)
        for index, char in enumerate(name):
            if char in self.BANNED_ACCEL:
                continue
            char = char.lower()
            if not char in self.USED:
                self.USED.append(char)
                return name[0:index] + '&' + name[index:]
        return name
    
    def buildMenuTextEntry(self, mnemonic = True):
        text = unicode(self.name)
        if mnemonic:
            text += u"\t%s" % (self.trigger)
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
        if 'keyEquivalent' in dataHash:
            dataHash['keyEquivalent'] = keysequence2keyequivalent(dataHash['keyEquivalent'])
        self.__bundleItem.update(dataHash)

    def isEditorNeeded(self):
        return self.isTextInputNeeded() or self.producingOutputText()

    def isTextInputNeeded(self):
        if self.__bundleItem.TYPE == "command":
            return self.__bundleItem.input not in [ "none" ]
        return True

    def producingOutputText(self):
        if self.__bundleItem.TYPE == "command":
            return self.__bundleItem.output not in [ "discard", "showAsHTML", "showAsTooltip", "createNewDocument", "openAsNewDocument"]
        return True

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
    def __init__(self, style, scores = None):
        self.__style = style
        self.scores = scores
        self.STYLES_CACHE = {}
    
    def __getattr__(self, name):
        # Quitar esta cosa fea
        return getattr(self.__style, name)

    def style(self):
        return self.__style

    @property
    def settings(self):
        settings = {}
        for color_key in ['foreground', 'background', 'selection', 'invisibles', 'lineHighlight', 'caret', 'gutter']:
            if color_key in self.__style.settings and self.__style.settings[color_key]:
                color = rgba2color(self.__style.settings[color_key])
                settings[color_key] = color
        settings['fontStyle'] = self.__style.settings['fontStyle'].split() if 'fontStyle' in self.__style.settings else []
        return settings
    
    def update(self, dataHash):
        if 'settings' in dataHash:
            settings = {}
            for key in dataHash['settings'].keys():
                if key in ['foreground', 'background', 'selection', 'invisibles', 'lineHighlight', 'caret', 'gutter']:
                    settings[key] = color2rgba(dataHash['settings'][key])
            if 'fontStyle' in dataHash['settings']:
                settings['fontStyle'] = " ".join(dataHash['settings']['fontStyle'])
            dataHash['settings'] = settings
        self.__style.update(dataHash)
    
    def clearCache(self):
        self.STYLES_CACHE = {}

    def getStyle(self, scope = None):
        if scope in self.STYLES_CACHE:
            return self.STYLES_CACHE[scope]
        base = {}
        base.update(self.settings)
        if scope == None:
            return base
        styles = []
        for style in self.styles:
            if style.scope != None:
                score = self.scores.score(style.scope, scope)
                if score != 0:
                    styles.append((score, style))
        styles.sort(key = lambda t: t[0])
        for score, style in styles:
            base.update(style.settings)
        self.STYLES_CACHE[scope] = base
        return base
