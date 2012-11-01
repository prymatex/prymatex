#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore
from prymatex.qt.helpers import keyequivalent2keysequence, keysequence2keyequivalent

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
