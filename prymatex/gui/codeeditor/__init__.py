# -*- coding: utf-8 -*-
#!/usr/bin/env python

from PyQt4 import QtCore

from prymatex.gui.codeeditor.dockers import PMXCodeBookmarksDock, PMXCodeSymbolsDock
from prymatex.gui.codeeditor.editor import PMXCodeEditor
from prymatex.gui.codeeditor import helpers
from prymatex.gui.codeeditor.status import PMXCodeEditorStatus

def setup(manager):
    manager.registerEditor(PMXCodeEditor)
    manager.registerDocker(PMXCodeBookmarksDock)
    manager.registerDocker(PMXCodeSymbolsDock)
    manager.registerStatusBar(PMXCodeEditorStatus)
    
    manager.registerKeyHelper(PMXCodeEditor, helpers.KeyEquivalentHelper)
    manager.registerKeyHelper(PMXCodeEditor, helpers.SmartTypingPairsHelper)
    manager.registerKeyHelper(PMXCodeEditor, helpers.SmartUnindentHelper)
    manager.registerKeyHelper(PMXCodeEditor, helpers.TabTriggerHelper)
    manager.registerKeyHelper(PMXCodeEditor, helpers.TabIndentHelper)
    manager.registerKeyHelper(PMXCodeEditor, helpers.BacktabUnindentHelper)
    manager.registerKeyHelper(PMXCodeEditor, helpers.CompleterHelper)
    manager.registerKeyHelper(PMXCodeEditor, helpers.BackspaceUnindentHelper)
    manager.registerKeyHelper(PMXCodeEditor, helpers.MoveCursorToHomeHelper)
    manager.registerKeyHelper(PMXCodeEditor, helpers.SmartIndentHelper)
    manager.registerKeyHelper(PMXCodeEditor, helpers.OverwriteHelper)
    manager.registerKeyHelper(PMXCodeEditor, helpers.MultiCursorHelper)
    #manager.loadResources(__file__)