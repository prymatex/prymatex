#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore

from prymatex.gui.codeeditor.dockers import PMXCodeBookmarksDock, PMXCodeSymbolsDock
from prymatex.gui.codeeditor.editor import PMXCodeEditor
from prymatex.gui.codeeditor import helpers, addons, sidebar
from prymatex.gui.codeeditor.status import PMXCodeEditorStatus
from prymatex.gui.codeeditor.overlay import PMXEditorMessageOverlay, PMXMiniMapOverlay

def registerPlugin(manager):
    manager.registerEditor(PMXCodeEditor)
    manager.registerStatusBar(PMXCodeEditorStatus)
    manager.registerDocker(PMXCodeSymbolsDock)
    manager.registerDocker(PMXCodeBookmarksDock)
    
    #manager.registerOverlay(PMXCodeEditor, PMXMiniMapOverlay)
    manager.registerOverlay(PMXCodeEditor, PMXEditorMessageOverlay)
    
    manager.registerKeyHelper(PMXCodeEditor, helpers.KeyEquivalentHelper)
    manager.registerKeyHelper(PMXCodeEditor, helpers.SmartTypingPairsHelper)
    manager.registerKeyHelper(PMXCodeEditor, helpers.TabTriggerHelper)
    manager.registerKeyHelper(PMXCodeEditor, helpers.TabIndentHelper)
    manager.registerKeyHelper(PMXCodeEditor, helpers.CompleterHelper)
    manager.registerKeyHelper(PMXCodeEditor, helpers.BacktabUnindentHelper)
    manager.registerKeyHelper(PMXCodeEditor, helpers.BackspaceUnindentHelper)
    manager.registerKeyHelper(PMXCodeEditor, helpers.BackspaceRemoveBracesHelper)
    manager.registerKeyHelper(PMXCodeEditor, helpers.MoveCursorToHomeHelper)
    manager.registerKeyHelper(PMXCodeEditor, helpers.SmartIndentHelper)
    manager.registerKeyHelper(PMXCodeEditor, helpers.OverwriteHelper)
    manager.registerKeyHelper(PMXCodeEditor, helpers.MultiCursorHelper)
    manager.registerKeyHelper(PMXCodeEditor, helpers.DeleteRemoveBracesHelper)
    manager.registerKeyHelper(PMXCodeEditor, helpers.PrintEditorStatusHelper)
    
    manager.registerAddon(PMXCodeEditor, addons.CompleterAddon)
    manager.registerAddon(PMXCodeEditor, addons.SmartUnindentAddon)
    manager.registerAddon(PMXCodeEditor, addons.SpellCheckerAddon)
    #manager.registerAddon(PMXCodeEditor, sidebar.ExtraSelectionSideBarAddon)
    manager.registerAddon(PMXCodeEditor, sidebar.BookmarkSideBarAddon)
    manager.registerAddon(PMXCodeEditor, sidebar.LineNumberSideBarAddon)
    manager.registerAddon(PMXCodeEditor, sidebar.FoldingSideBarAddon)
