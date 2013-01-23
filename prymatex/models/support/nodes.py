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
# Theme Table Row
#====================================================
class ThemeTableRow(object):
    """Theme and Style decorator"""
    def __init__(self, themeItem):
        self.__themeItem = themeItem
        self.STYLES_CACHE = {}

    # ---------------------------- Decorator
    def __getattr__(self, name):
        return getattr(self.__themeItem, name)


    def themeItem(self):
        return self.__themeItem


    @property
    def settings(self):
        settings = dict(map(lambda (key, value): (key, rgba2color(value)), filter(lambda (key, value): value.startswith('#'), self.__themeItem.settings.iteritems())))
        
        # Fix some color keys
        settings.setdefault('gutter', settings['background'])
        settings.setdefault('gutterForeground', settings['foreground'])
        
        # Fonts
        settings['fontStyle'] = self.__themeItem.settings['fontStyle'].split() if 'fontStyle' in self.__themeItem.settings else []
        return settings

    
    def update(self, dataHash):
        if 'settings' in dataHash:
            settings = dict(map(lambda (key, value): (key, color2rgba(value)), dataHash['settings'].iteritems()))
            if 'fontStyle' in dataHash['settings']:
                settings['fontStyle'] = " ".join(dataHash['settings']['fontStyle'])
            dataHash['settings'] = settings
        self.__themeItem.update(dataHash)

    
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
            rank = []
            if style.selector.does_match(scope, rank):
                styles.append((sum(rank), style))
        styles.sort(key = lambda t: t[0])
        for score, style in styles:
            base.update(style.settings)
        self.STYLES_CACHE[scope] = base
        return base


#====================================================
# Themes Styles Row
#====================================================
class ThemeStyleTableRow(object):
    """Theme and Style decorator"""
    def __init__(self, styleItem):
        self.__styleItem = styleItem


    # ---------------------------- Decorator
    def __getattr__(self, name):
        return getattr(self.__styleItem, name)


    def styleItem(self):
        return self.__styleItem


    @property
    def settings(self):
        settings = dict(map(lambda (key, value): (key, rgba2color(value)), filter(lambda (key, value): value.startswith('#'), self.__styleItem.settings.iteritems())))
        
        # Fonts
        settings['fontStyle'] = self.__styleItem.settings['fontStyle'].split() if 'fontStyle' in self.__styleItem.settings else []
        return settings

    
    def update(self, dataHash):
        if 'settings' in dataHash:
            settings = dict(map(lambda (key, value): (key, color2rgba(value)), dataHash['settings'].iteritems()))
            if 'fontStyle' in dataHash['settings']:
                settings['fontStyle'] = " ".join(dataHash['settings']['fontStyle'])
            dataHash['settings'] = settings
        self.__styleItem.update(dataHash)
