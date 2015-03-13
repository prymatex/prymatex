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

__plugin__.registerComponent(CodeEditor, default=True)
__plugin__.registerComponent(CodeEditorStatus)
__plugin__.registerComponent(CodeEditorSymbolsDock)
__plugin__.registerComponent(CodeEditorBookmarksDock)

    # ---------------- Modes
__plugin__.registerComponent(CodeEditorEditMode, CodeEditor) # First is default mode
__plugin__.registerComponent(CodeEditorMultiCursorMode, CodeEditor)
__plugin__.registerComponent(CodeEditorSnippetMode, CodeEditor)
__plugin__.registerComponent(CodeEditorComplitionMode, CodeEditor)

    # ---------------- Addons
    #manager.registerComponent(SmartUnindentAddon, CodeEditor)
    #manager.registerComponent(SpellCheckerAddon, CodeEditor)
__plugin__.registerComponent(HighlightCurrentSelectionAddon, CodeEditor)

    # ---------------- Sidebars
__plugin__.registerComponent(MiniMapAddon, CodeEditor)
__plugin__.registerComponent(BookmarkSideBarAddon, CodeEditor)
__plugin__.registerComponent(LineNumberSideBarAddon, CodeEditor)
__plugin__.registerComponent(FoldingSideBarAddon, CodeEditor)
__plugin__.registerComponent(SelectionSideBarAddon, CodeEditor)
