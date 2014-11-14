#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .dockers import CodeEditorBookmarksDock, CodeEditorSymbolsDock
from .editor import CodeEditor
from .addons import (CodeEditorAddon, SmartUnindentAddon, SpellCheckerAddon,
    HighlightCurrentSelectionAddon)
from .sidebar import (BookmarkSideBarAddon, LineNumberSideBarAddon,
    FoldingSideBarAddon, SelectionSideBarAddon)
from .minimap import (MiniMapAddon)
from .modes import (CodeEditorEditMode, CodeEditorMultiCursorMode,
    CodeEditorSnippetMode, CodeEditorComplitionMode)
from .status import CodeEditorStatus

def registerPlugin(manager, descriptor):
    manager.registerComponent(CodeEditor, default = True)
    manager.registerComponent(CodeEditorStatus)
    manager.registerComponent(CodeEditorSymbolsDock)
    manager.registerComponent(CodeEditorBookmarksDock)

    # ---------------- Modes
    manager.registerComponent(CodeEditorEditMode, CodeEditor) # First is default mode
    #manager.registerComponent(CodeEditorMultiCursorMode, CodeEditor)
    #manager.registerComponent(CodeEditorSnippetMode, CodeEditor)
    #manager.registerComponent(CodeEditorComplitionMode, CodeEditor)

    # ---------------- Addons
    #manager.registerComponent(SmartUnindentAddon, CodeEditor)
    #manager.registerComponent(SpellCheckerAddon, CodeEditor)
    manager.registerComponent(HighlightCurrentSelectionAddon, CodeEditor)

    # ---------------- Sidebars
    #manager.registerComponent(MiniMapAddon, CodeEditor)
    manager.registerComponent(BookmarkSideBarAddon, CodeEditor)
    manager.registerComponent(LineNumberSideBarAddon, CodeEditor)
    manager.registerComponent(FoldingSideBarAddon, CodeEditor)
    manager.registerComponent(SelectionSideBarAddon, CodeEditor)
