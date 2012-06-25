#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore

from prymatex.gui.codeeditor.dockers import PMXCodeBookmarksDock, PMXCodeSymbolsDock
from prymatex.gui.codeeditor.editor import CodeEditor
from prymatex.gui.codeeditor import helpers, addons, sidebar
from prymatex.gui.codeeditor.status import PMXCodeEditorStatus
from prymatex.gui.codeeditor.overlay import PMXEditorMessageOverlay, PMXMiniMapOverlay

def registerPlugin(manager):
    manager.registerEditor(CodeEditor)
    manager.registerStatusBar(PMXCodeEditorStatus)
    manager.registerDocker(PMXCodeSymbolsDock)
    manager.registerDocker(PMXCodeBookmarksDock)
    
    #manager.registerOverlay(CodeEditor, PMXMiniMapOverlay)
    manager.registerOverlay(CodeEditor, PMXEditorMessageOverlay)
    
    manager.registerKeyHelper(CodeEditor, helpers.KeyEquivalentHelper)
    manager.registerKeyHelper(CodeEditor, helpers.SmartTypingPairsHelper)
    manager.registerKeyHelper(CodeEditor, helpers.TabTriggerHelper)
    manager.registerKeyHelper(CodeEditor, helpers.TabIndentHelper)
    manager.registerKeyHelper(CodeEditor, helpers.CompleterHelper)
    manager.registerKeyHelper(CodeEditor, helpers.BacktabUnindentHelper)
    manager.registerKeyHelper(CodeEditor, helpers.BackspaceUnindentHelper)
    manager.registerKeyHelper(CodeEditor, helpers.BackspaceRemoveBracesHelper)
    manager.registerKeyHelper(CodeEditor, helpers.DeleteRemoveBracesHelper)
    manager.registerKeyHelper(CodeEditor, helpers.DeleteUnindentHelper)
    manager.registerKeyHelper(CodeEditor, helpers.MoveCursorToHomeHelper)
    manager.registerKeyHelper(CodeEditor, helpers.SmartIndentHelper)
    manager.registerKeyHelper(CodeEditor, helpers.OverwriteHelper)
    manager.registerKeyHelper(CodeEditor, helpers.MultiCursorHelper)

    manager.registerKeyHelper(CodeEditor, helpers.PrintEditorStatusHelper)
    
    manager.registerAddon(CodeEditor, addons.CompleterAddon)
    manager.registerAddon(CodeEditor, addons.SmartUnindentAddon)
    manager.registerAddon(CodeEditor, addons.SpellCheckerAddon)
    manager.registerAddon(CodeEditor, addons.HighlightCurrentSelectionAddon)

    manager.registerAddon(CodeEditor, sidebar.BookmarkSideBarAddon)
    manager.registerAddon(CodeEditor, sidebar.LineNumberSideBarAddon)
    manager.registerAddon(CodeEditor, sidebar.FoldingSideBarAddon)
