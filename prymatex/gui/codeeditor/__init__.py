#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .dockers import CodeEditorBookmarksDock, CodeEditorSymbolsDock
from .editor import CodeEditor
from . import helpers, addons, sidebar, minimap, modes
from .status import CodeEditorStatus

def registerPlugin(manager):
    manager.registerComponent(CodeEditor)
    manager.registerComponent(CodeEditorStatus)
    manager.registerComponent(CodeEditorSymbolsDock)
    manager.registerComponent(CodeEditorBookmarksDock)
    
    manager.registerComponent(helpers.KeyEquivalentHelper, CodeEditor)
    manager.registerComponent(helpers.SmartTypingPairsHelper, CodeEditor)
    manager.registerComponent(helpers.TabTriggerHelper, CodeEditor)
    manager.registerComponent(helpers.TabIndentHelper, CodeEditor)
    manager.registerComponent(helpers.BacktabUnindentHelper, CodeEditor)
    manager.registerComponent(helpers.BackspaceUnindentHelper, CodeEditor)
    manager.registerComponent(helpers.BackspaceRemoveBracesHelper, CodeEditor)
    manager.registerComponent(helpers.DeleteRemoveBracesHelper, CodeEditor)
    manager.registerComponent(helpers.DeleteUnindentHelper, CodeEditor)
    manager.registerComponent(helpers.MoveCursorToHomeHelper, CodeEditor)
    manager.registerComponent(helpers.SmartIndentHelper, CodeEditor)
    manager.registerComponent(helpers.OverwriteHelper, CodeEditor)
    manager.registerComponent(helpers.MultiCursorHelper, CodeEditor)
    
    manager.registerComponent(helpers.PrintEditorStatusHelper, CodeEditor)

    # ---------------- Modes
    # manager.registerComponent(modes.CodeEditorTestMode, CodeEditor)
    
    # ---------------- Addons
    manager.registerComponent(addons.SmartUnindentAddon, CodeEditor)
    manager.registerComponent(addons.SpellCheckerAddon, CodeEditor)
    manager.registerComponent(addons.HighlightCurrentSelectionAddon, CodeEditor)

    # ---------------- Sidebars
    manager.registerComponent(minimap.MiniMapAddon, CodeEditor)
    manager.registerComponent(sidebar.BookmarkSideBarAddon, CodeEditor)
    manager.registerComponent(sidebar.LineNumberSideBarAddon, CodeEditor)
    manager.registerComponent(sidebar.FoldingSideBarAddon, CodeEditor)
    manager.registerComponent(sidebar.SelectionSideBarAddon, CodeEditor)
