#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.qt.helpers import (keyequivalent_to_keysequence,
    keysequence_to_keyequivalent, rgba2color, color2rgba, qapplication)

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
        self._icon = None
        self._format_cache = {}
        self._palette_cache = {}
        self._style_base = { key_value[0]: rgba2color(key_value[1]) \
            for key_value in DEFAULT_THEME_SETTINGS.items() if key_value[1].startswith('#') }

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
        keyseq = self.keySequence()
        if keyseq is not None and keyseq.count() > 0:
            return keyseq[0]
    
    def setIcon(self, icon):
        self._icon = icon

    def icon(self):
        return self._icon
        #return resources.get_icon("bundle-item-%s" % self.type())
    
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

    # ----------- Theme decoration -----------
    def clearCache(self):
        self._format_cache = {}
        self._palette_cache = {}

    def style(self, scope = None):
        styles = []
        for style in self.__bundleItem.settings:
            rank = []
            if style.scopeSelector.does_match(scope, rank):
                styles.append((rank.pop(), style))
        styles.sort(key = lambda t: t[0])
        style = self._style_base.copy()
        for s in styles:
            style.update(s[1].settings())
        return style
    
    def palette(self, scope = None, cache = True):
        if cache and scope in self._palette_cache:
            return self._palette_cache[scope]
        
        palette = qapplication().palette()
        settings = self.style(scope)
        if 'foreground' in settings:
            #QPalette::Foreground	0	This value is obsolete. Use WindowText instead.
            palette.setColor(QtGui.QPalette.Foreground, settings['background'])
            #QPalette::WindowText	0	A general foreground color.
            palette.setColor(QtGui.QPalette.WindowText, settings['foreground'])
            #QPalette::Text	6	The foreground color used with Base. This is usually the same as the WindowText, in which case it must provide good contrast with Window and Base.
            palette.setColor(QtGui.QPalette.Text, settings['foreground'])
        if 'background' in settings:
            #QPalette::Background	10	This value is obsolete. Use Window instead.
            palette.setColor(QtGui.QPalette.Background, settings['background'])
            #QPalette::Window	10	A general background color.
            palette.setColor(QtGui.QPalette.Window, settings['background'])
            #QPalette::Base	9	Used mostly as the background color for text entry widgets, but can also be used for other painting - such as the background of combobox drop down lists and toolbar handles. It is usually white or another light color.
            palette.setColor(QtGui.QPalette.Base, settings['background'])
        if 'selection' in settings:
            #QPalette::Highlight	12	A color to indicate a selected item or the current item. By default, the highlight color is Qt::darkBlue.
            palette.setColor(QtGui.QPalette.Highlight, settings['selection'])
        if 'invisibles' in settings:
            #QPalette::LinkVisited	15	A text color used for already visited hyperlinks. By default, the linkvisited color is Qt::magenta.
            palette.setColor(QtGui.QPalette.LinkVisited, settings['invisibles'])
        if 'lineHighlight' in settings:
            #QPalette::AlternateBase	16	Used as the alternate background color in views with alternating row colors (see QAbstractItemView::setAlternatingRowColors()).
            palette.setColor(QtGui.QPalette.AlternateBase, settings['lineHighlight'])
        if 'caret' in settings:
            #QPalette::BrightText	7	A text color that is very different from WindowText, and contrasts well with e.g. Dark. Typically used for text that needs to be drawn where Text or WindowText would give poor contrast, such as on pressed push buttons. Note that text colors can be used for things other than just words; text colors are usually used for text, but it's quite common to use the text color roles for lines, icons, etc.
            palette.setColor(QtGui.QPalette.BrightText, settings['caret'])
        if 'gutterBackground' in settings:
            print("color back")
            #QPalette::ToolTipBase	18	Used as the background color for QToolTip and QWhatsThis. Tool tips use the Inactive color group of QPalette, because tool tips are not active windows.
            palette.setColor(QtGui.QPalette.ToolTipBase, settings['gutterBackground'])
        if 'gutterForeground' in settings:
            #QPalette::ToolTipText	19	Used as the foreground color for QToolTip and QWhatsThis. Tool tips use the Inactive color group of QPalette, because tool tips are not active windows.
            palette.setColor(QtGui.QPalette.ToolTipText, settings['gutterForeground'])
        #QPalette::Button	1	The general button background color. This background can be different from Window as some styles require a different background color for buttons.
        #QPalette::ButtonText	8	A foreground color used with the Button color.
        #QPalette::HighlightedText	13	A text color that contrasts with Highlight. By default, the highlighted text color is Qt::white.
        #QPalette::Link	14	A text color used for unvisited hyperlinks. By default, the link color is Qt::blue.
        if not cache:
            return palette
        return self._palette_cache.setdefault(scope, palette)
        
    def textCharFormat(self, scope = None, cache = True):
        if cache and scope in self._format_cache:
            return self._format_cache[scope]

        frmt = QtGui.QTextCharFormat()
        settings = self.style(scope)
        if 'foreground' in settings:
            frmt.setForeground(settings['foreground'])
        if 'background' in settings:
            frmt.setBackground(settings['background'])
        if 'fontStyle' in settings:
            if 'bold' in settings['fontStyle']:
                frmt.setFontWeight(QtGui.QFont.Bold)
            if 'underline' in settings['fontStyle']:
                frmt.setFontUnderline(True)
            if 'italic' in settings['fontStyle']:
                frmt.setFontItalic(True)
        if not cache:
            return frmt
        return self._format_cache.setdefault(scope, frmt)

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
