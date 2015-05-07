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

__prymatex__.registerComponent(CodeEditor, default=True)
__prymatex__.registerComponent(CodeEditorStatus)
__prymatex__.registerComponent(CodeEditorSymbolsDock)
__prymatex__.registerComponent(CodeEditorBookmarksDock)

    # ---------------- Modes
__prymatex__.registerComponent(CodeEditorEditMode, CodeEditor) # First is default mode
#__prymatex__.registerComponent(CodeEditorMultiCursorMode, CodeEditor)
__prymatex__.registerComponent(CodeEditorSnippetMode, CodeEditor)
#__prymatex__.registerComponent(CodeEditorComplitionMode, CodeEditor)

# ---------------- Addons
#__prymatex__.registerComponent(SmartUnindentAddon, CodeEditor)
#__prymatex__.registerComponent(SpellCheckerAddon, CodeEditor)
__prymatex__.registerComponent(HighlightCurrentSelectionAddon, CodeEditor)

    # ---------------- Sidebars
__prymatex__.registerComponent(MiniMapAddon, CodeEditor)
__prymatex__.registerComponent(BookmarkSideBarAddon, CodeEditor)
__prymatex__.registerComponent(LineNumberSideBarAddon, CodeEditor)
__prymatex__.registerComponent(FoldingSideBarAddon, CodeEditor)
__prymatex__.registerComponent(SelectionSideBarAddon, CodeEditor)
