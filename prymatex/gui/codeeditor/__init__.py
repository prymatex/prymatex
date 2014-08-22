#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .dockers import CodeEditorBookmarksDock, CodeEditorSymbolsDock
from .editor import CodeEditor
from .helpers import (CodeEditorKeyHelper, KeyEquivalentHelper, SmartTypingPairsHelper,
    TabTriggerHelper, TabIndentHelper, BacktabUnindentHelper, BackspaceUnindentHelper,
    BackspaceRemoveBracesHelper, DeleteRemoveBracesHelper, DeleteUnindentHelper,
    MoveCursorToHomeHelper, SmartIndentHelper, OverwriteHelper, PrintEditorStatusHelper)
from .addons import (CodeEditorAddon, SmartUnindentAddon, SpellCheckerAddon,
    HighlightCurrentSelectionAddon)
from .sidebar import (SideBarWidgetAddon, BookmarkSideBarAddon, LineNumberSideBarAddon,
    FoldingSideBarAddon, SelectionSideBarAddon)
from .minimap import (MiniMapAddon)
from .modes import (CodeEditorMultiCursorMode, CodeEditorSnippetMode)
from .status import CodeEditorStatus
from .completer import CompletionBaseModel

def registerPlugin(manager, descriptor):
    manager.registerComponent(CodeEditor, default = True)
    manager.registerComponent(CodeEditorStatus)
    manager.registerComponent(CodeEditorSymbolsDock)
    manager.registerComponent(CodeEditorBookmarksDock)

    manager.registerComponent(KeyEquivalentHelper, CodeEditor)
    manager.registerComponent(SmartTypingPairsHelper, CodeEditor)
    manager.registerComponent(TabTriggerHelper, CodeEditor)
    manager.registerComponent(TabIndentHelper, CodeEditor)
    manager.registerComponent(BacktabUnindentHelper, CodeEditor)
    manager.registerComponent(BackspaceUnindentHelper, CodeEditor)
    manager.registerComponent(BackspaceRemoveBracesHelper, CodeEditor)
    manager.registerComponent(DeleteRemoveBracesHelper, CodeEditor)
    manager.registerComponent(DeleteUnindentHelper, CodeEditor)
    manager.registerComponent(MoveCursorToHomeHelper, CodeEditor)
    manager.registerComponent(SmartIndentHelper, CodeEditor)
    manager.registerComponent(OverwriteHelper, CodeEditor)
    manager.registerComponent(PrintEditorStatusHelper, CodeEditor)

    # ---------------- Modes
    manager.registerComponent(CodeEditorMultiCursorMode, CodeEditor)
    manager.registerComponent(CodeEditorSnippetMode, CodeEditor)

    # ---------------- Addons
    manager.registerComponent(SmartUnindentAddon, CodeEditor)
    #manager.registerComponent(SpellCheckerAddon, CodeEditor)
    manager.registerComponent(HighlightCurrentSelectionAddon, CodeEditor)

    # ---------------- Sidebars
    manager.registerComponent(MiniMapAddon, CodeEditor)
    manager.registerComponent(BookmarkSideBarAddon, CodeEditor)
    manager.registerComponent(LineNumberSideBarAddon, CodeEditor)
    manager.registerComponent(FoldingSideBarAddon, CodeEditor)
    manager.registerComponent(SelectionSideBarAddon, CodeEditor)
